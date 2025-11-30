from fastapi import Depends, HTTPException, status
from app.core.security import get_current_user  # if you have this already
from app.models.user import UserRole

def admin_required(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return current_user
