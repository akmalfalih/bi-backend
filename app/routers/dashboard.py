# app/routers/dashboard.py
from fastapi import APIRouter, Depends
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def get_dashboard_summary(current_user: User = Depends(get_current_user)):
    """
    Endpoint dummy untuk menampilkan ringkasan statistik dashboard.
    Hanya bisa diakses oleh user yang sudah login (token valid).
    """
    data = {
        "total_users": 128,
        "total_transactions": 5420,
        "active_sessions": 17,
        "system_status": "Operational",
    }
    return {"message": "Dashboard summary retrieved successfully", "data": data}


@router.get("/activities")
def get_recent_activities(current_user: User = Depends(get_current_user)):
    """
    Endpoint dummy untuk menampilkan daftar aktivitas terbaru.
    """
    activities = [
        {"timestamp": "2025-10-14T09:00:00", "activity": "User A added new TBS entry"},
        {"timestamp": "2025-10-14T09:30:00", "activity": "User B updated transaction data"},
        {"timestamp": "2025-10-14T10:00:00", "activity": "User C viewed marketing report"},
        {"timestamp": "2025-10-14T10:15:00", "activity": "User D logged in"},
    ]
    return {"message": "Recent activities retrieved successfully", "data": activities}
