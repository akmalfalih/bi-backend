from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy import func, and_, distinct, cast, Float
from app.core.database import get_db
from app.services.security import get_current_user
from app.models.t_tbs_dalam import TTbsDalam
from app.models.t_trans_lintas_keluar import TTransLintasKeluar
from app.models.t_trans_pemasaran import TTransPemasaran
# from app.models.m_lokasi import MLokasi

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

# Filter berdasarkan periode tanggal
def get_date_filters(start_date: date | None, end_date: date | None):
    """Mengatur default tanggal (bulan berjalan) jika filter tidak diberikan."""
    today = datetime.today()
    start_of_month = date(today.year, today.month, 1)
    start = start_date or start_of_month
    end = end_date or today.date()
    return start, end


@router.get("/summary")
def get_production_summary(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db)
):
    # --- default ke bulan berjalan ---
    today = date.today()
    if not start_date:
        start_date = today.replace(day=1)
    if not end_date:
        end_date = today

    # PRODUKSI TBS
    tbs_query = (
        db.query(
            func.sum(TTbsDalam.Total).label("total_produksi"),
            func.count(distinct(TTbsDalam.TglTransaksiOne)).label("jumlah_hari")
        )
        .filter(TTbsDalam.TglTransaksiOne >= start_date)
        .filter(TTbsDalam.TglTransaksiOne <= end_date)
    )

    tbs_result = tbs_query.first()
    total_tbs = tbs_result.total_produksi or 0
    hari_tbs = tbs_result.jumlah_hari or 1
    rata_tbs_per_hari = total_tbs / hari_tbs

    # PEMASARAN CPO
    cpo_query = (
        db.query(
            func.sum(TTransPemasaran.TotalTmb).label("total_terjual"),
            func.avg(cast(TTransPemasaran.FFA, Float)).label("rata_rata_ffa"),
            func.max(cast(TTransPemasaran.FFA, Float)).label("max_ffa"),
            func.min(cast(TTransPemasaran.FFA, Float)).label("min_ffa")
        )
        .filter(TTransPemasaran.NamaProduk == "CPO")
        .filter(TTransPemasaran.TglTmb1 >= start_date)
        .filter(TTransPemasaran.TglTmb1 <= end_date)
    )

    cpo_result = cpo_query.first()

    # --- Response ---
    return {
        "message": "Production & CPO summary retrieved successfully",
        "period": {
            "start_date": str(start_date),
            "end_date": str(end_date)
        },
        "data": {
            "tbs": {
                "total_panen": total_tbs,
                "rata_rata_per_hari": rata_tbs_per_hari,

            },
            "cpo": {
                "total_terjual": cpo_result.total_terjual or 0,
                "rata_rata_ffa": cpo_result.rata_rata_ffa or 0,
                "max_ffa": cpo_result.max_ffa or 0,
                "min_ffa": cpo_result.min_ffa or 0
            }
        }
    }


@router.get("/activities")
def get_dashboard_activities(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Menampilkan kombinasi aktifitas terbaru dari TBS Dalam, Lintas Keluar, dan Pemasaran"""
    from sqlalchemy import desc

    tbs_activities = (
        db.query(TTbsDalam.NoTransaksi, TTbsDalam.NamaProduk, TTbsDalam.Total, TTbsDalam.TglTransaksiOne)
        .order_by(desc(TTbsDalam.TglTransaksiOne))
        .limit(10)
        .all()
    )
    lintas_activities = (
        db.query(TTransLintasKeluar.NoTransaksi, TTransLintasKeluar.NamaProduk, TTransLintasKeluar.Total, TTransLintasKeluar.TglTmb1)
        .order_by(desc(TTransLintasKeluar.TglTmb1))
        .limit(5)
        .all()
    )
    pemasaran_activities = (
        db.query(TTransPemasaran.NoTransaksi, TTransPemasaran.NamaProduk, TTransPemasaran.TotalTmb, TTransPemasaran.TglTmb1)
        .order_by(desc(TTransPemasaran.TglTmb1))
        .limit(5)
        .all()
    )

    combined = []
    for trx in tbs_activities:
        combined.append({
            "source": "TBS Dalam",
            "no_transaksi": trx.NoTransaksi,
            "produk": trx.NamaProduk,
            "total": trx.Total,
            "tanggal": str(trx.TglTransaksiOne)
        })
    for trx in lintas_activities:
        combined.append({
            "source": "Lintas Keluar",
            "no_transaksi": trx.NoTransaksi,
            "produk": trx.NamaProduk,
            "total": trx.Total,
            "tanggal": str(trx.TglTmb1)
        })
    for trx in pemasaran_activities:
        combined.append({
            "source": "Pemasaran",
            "no_transaksi": trx.NoTransaksi,
            "produk": trx.NamaProduk,
            "total": trx.TotalTmb,
            "tanggal": str(trx.TglTmb1)
        })

    # Sort all activities descending by date
    combined = sorted(combined, key=lambda x: x["tanggal"], reverse=True)

    return {
        "message": "Recent activities retrieved successfully",
        "data": combined[:20],
    }

@router.get("/production/trend", summary="Get TBS production trend")
def get_production_trend(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    nama_kebun: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Menampilkan tren produksi TBS berdasarkan tanggal (digunakan untuk line chart).
    Bisa difilter berdasarkan tanggal, kebun, dan lokasi timbang.
    """
    start, end = get_date_filters(start_date, end_date)

    query = (
        db.query(
            func.date(TTbsDalam.TglTransaksiOne).label("tanggal"),
            func.sum(TTbsDalam.Total).label("total")
        )
        .filter(
            and_(
                TTbsDalam.TglTransaksiOne >= start,
                TTbsDalam.TglTransaksiOne <= end,
            )
        )
    )

    if nama_kebun:
        query = query.filter(TTbsDalam.NamaKebun == nama_kebun)

    results = query.group_by(func.date(TTbsDalam.TglTransaksiOne)).order_by("tanggal").all()

    data = [{"tanggal": str(r.tanggal), "total": float(r.total)} for r in results]

    return {
        "message": "Production trend retrieved successfully",
        "filters": {
            "start_date": str(start),
            "end_date": str(end),
            "nama_kebun": nama_kebun,
        },
        "data": data,
    }

@router.get("/production/by-location")
def get_production_by_kebun(db: Session = Depends(get_db)):
    """
    Menampilkan total tonase produksi TBS per asal kebun (NamaKebun)
    berdasarkan transaksi bulan berjalan.
    """
    today = date.today()
    start_of_month = today.replace(day=1)

    results = (
        db.query(
            TTbsDalam.NamaKebun.label("nama_kebun"),
            func.sum(TTbsDalam.Total).label("total"),
        )
        .filter(TTbsDalam.TglTransaksiOne >= start_of_month)
        .group_by(TTbsDalam.NamaKebun)
        .order_by(func.sum(TTbsDalam.Total).desc())
        .all()
    )

    data = [
        {"nama_kebun": r.nama_kebun or "Tidak Diketahui", "total": float(r.total or 0)}
        for r in results
    ]

    return {
        "message": "Production by kebun retrieved successfully",
        "period": {"start_date": str(start_of_month), "end_date": str(today)},
        "data": data,
    }

@router.get("/production/composition")
def get_production_composition(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    nama_kebun: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Menampilkan proporsi produksi TBS berdasarkan NamaKebun (pie chart).
    Bisa difilter berdasarkan tanggal dan lokasi timbang.
    """
    start, end = get_date_filters(start_date, end_date)

    query = (
        db.query(
            TTbsDalam.NamaKebun,
            func.sum(TTbsDalam.Total).label("total")
        )
        .filter(
            and_(
                TTbsDalam.TglTransaksiOne >= start,
                TTbsDalam.TglTransaksiOne <= end,
            )
        )
    )

    if nama_kebun:
        query = query.filter(TTbsDalam.NamaKebun == nama_kebun)

    results = query.group_by(TTbsDalam.NamaKebun).all()
    total_all = sum(float(r.total) for r in results)

    data = [
        {
            "nama_kebun": r.NamaKebun,
            "total": float(r.total),
            "persentase": round((float(r.total) / total_all * 100), 2) if total_all > 0 else 0,
        }
        for r in results
    ]

    return {
        "message": "Production composition retrieved successfully",
        "filters": {
            "start_date": str(start),
            "end_date": str(end),
            "nama_kebun": nama_kebun,
        },
        "data": data,
    }
