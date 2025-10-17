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
def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Menampilkan ringkasan data produksi bulan berjalan:
    - Total TBS Dalam
    - Total Lintas Keluar
    - Total Pemasaran
    - Total Transaksi
    """
    today = date.today()
    start_of_month = today.replace(day=1)

    total_tbs_dalam = (
        db.query(func.sum(TTbsDalam.Total))
        .filter(TTbsDalam.TglTransaksiOne >= start_of_month)
        .scalar()
        or 0
    )

    total_lintas_keluar = (
        db.query(func.sum(TTransLintasKeluar.Total))
        .filter(TTransLintasKeluar.TglTmb1 >= start_of_month)
        .scalar()
        or 0
    )

    total_pemasaran = (
        db.query(func.sum(TTransPemasaran.TotalTmb))
        .filter(TTransPemasaran.TglTmb1 >= start_of_month)
        .scalar()
        or 0
    )

    total_transaksi = (
        db.query(func.count(TTbsDalam.NoTransaksi))
        .filter(TTbsDalam.TglTransaksiOne >= start_of_month)
        .scalar()
        or 0
    )

    return {
        "message": "Dashboard summary retrieved successfully",
        "period": {"start_date": str(start_of_month), "end_date": str(today)},
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

@router.get("/production/trend", summary="Get TBS production trend")
def get_production_trend(start_date: date | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)):
    """
    Get daily TBS production data (for current month)
    """
    today = date.today()
    start_of_month = today.replace(day=1)

    # Gunakan default bulan berjalan bila parameter kosong
    if not start_date or not end_date:
        start_date, end_date = start_of_month, today

    # Query optimized: total berat berdasarkan NamaKebun
    results = (
        db.query(
            TTbsDalam.TglTransaksiOne.label("tanggal"),
            func.sum(TTbsDalam.Total).label("total")
        )
        .filter(
            TTbsDalam.TglTransaksiOne >= start_date,
            TTbsDalam.TglTransaksiOne <= end_date
        )
        .group_by(TTbsDalam.TglTransaksiOne)
        .order_by(TTbsDalam.TglTransaksiOne)
        .all()
    )

    # Format hasil
    data = [
        {
            "tanggal": row.tanggal.strftime("%Y-%m-%d"),
            "total": float(row.total or 0)
        }
        for row in results
    ]

    return {
        "message": "TBS production trend retrieved successfully",
        "period": {"start_date": start_date, "end_date": end_date},
        "data": data
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
