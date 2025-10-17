from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import func
from app.core.database import get_db
from app.services.security import get_current_user
from app.models.t_tbs_dalam import TTbsDalam
from app.models.t_trans_lintas_keluar import TTransLintasKeluar
from app.models.t_trans_pemasaran import TTransPemasaran
from app.models.m_lokasi import MLokasi

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get summarized production data for current month"""
    today = date.today()
    start_of_month = today.replace(day=1)

    # Total TBS dari kebun sendiri (TTbsDalam)
    total_tbs_dalam = (
        db.query(TTbsDalam)
        .filter(TTbsDalam.TglTransaksiOne >= start_of_month)
        .with_entities(func.sum(TTbsDalam.Total))
        .scalar()
    ) or 0

    # Total TBS lintas keluar (penjualan lintas)
    total_lintas_keluar = (
        db.query(TTransLintasKeluar)
        .filter(TTransLintasKeluar.TglTmb1 >= start_of_month)
        .with_entities(func.sum(TTransLintasKeluar.Total))
        .scalar()
    ) or 0

    # Total Pemasaran (hasil olahan CPO, Kernel, dll)
    total_pemasaran = (
        db.query(TTransPemasaran)
        .filter(TTransPemasaran.TglTmb1 >= start_of_month)
        .with_entities(func.sum(TTransPemasaran.TotalTmb))
        .scalar()
    ) or 0

    # Total transaksi (gabungan 3 tabel)
    total_transaksi = (
        db.query(TTbsDalam).filter(TTbsDalam.TglTransaksiOne >= start_of_month).count()
        + db.query(TTransLintasKeluar).filter(TTransLintasKeluar.TglTmb1 >= start_of_month).count()
        + db.query(TTransPemasaran).filter(TTransPemasaran.TglTmb1 >= start_of_month).count()
    )

    return {
        "message": "Dashboard summary retrieved successfully",
        "period": {
            "start_date": str(start_of_month),
            "end_date": str(today),
        },
        "data": {
            "total_tbs_dalam": total_tbs_dalam,
            "total_lintas_keluar": total_lintas_keluar,
            "total_pemasaran": total_pemasaran,
            "total_transaksi": total_transaksi,
        },
    }


@router.get("/activities")
def get_dashboard_activities(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Get recent combined activities from TBS Dalam, Lintas Keluar, and Pemasaran"""
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

@router.get("/production/tbs")
def get_tbs_production_daily(db=Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Get daily TBS production data (for current month)
    """
    today = date.today()
    start_of_month = today.replace(day=1)

    # Query total produksi per tanggal (bulan berjalan)
    results = (
        db.query(
            func.date(TTbsDalam.TglTransaksiOne).label("date"),
            func.sum(TTbsDalam.Total).label("total")
        )
        .filter(TTbsDalam.TglTransaksiOne >= start_of_month)
        .filter(TTbsDalam.TglTransaksiOne <= today)
        .group_by(func.date(TTbsDalam.TglTransaksiOne))
        .order_by(func.date(TTbsDalam.TglTransaksiOne))
        .all()
    )

    # Format hasil query ke JSON-friendly structure
    data = [
        {"date": r.date.strftime("%Y-%m-%d"), "total": float(r.total or 0)}
        for r in results
    ]

    return {
        "message": "Daily TBS production data retrieved successfully",
        "period": {"start_date": str(start_of_month), "end_date": str(today)},
        "data": data
    }

@router.get("/production/by-location")
def get_production_by_location(
    db: Session = Depends(get_db),
    include_empty: bool = Query(True, description="Include locations with zero production this month")):

    today = date.today()
    start_of_month = date(today.year, today.month, 1)

    # Base query with LEFT JOIN
    query = (
        db.query(
            MLokasi.id_lokasi,
            MLokasi.kode_lokasi,
            func.coalesce(func.sum(TTbsDalam.Total), 0).label("total")
        )
        .outerjoin(
            TTbsDalam,
            (TTbsDalam.id_lokasi == MLokasi.id_lokasi)
            & (TTbsDalam.TglTransaksiOne >= start_of_month)
            & (TTbsDalam.TglTransaksiOne <= today)
        )
        .group_by(MLokasi.id_lokasi, MLokasi.kode_lokasi)
        .order_by(MLokasi.id_lokasi)
    )

    results = query.all()

    response_data = [
        {"id_lokasi": r.id_lokasi, "kode_lokasi": r.kode_lokasi, "total": float(r.total or 0)}
        for r in results
    ]

    return {
        "message": "Production by location retrieved successfully",
        "period": {"start_date": start_of_month, "end_date": today},
        "data": response_data
    }
