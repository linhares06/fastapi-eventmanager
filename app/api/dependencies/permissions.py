from fastapi import Depends, HTTPException, status
from .security import get_current_user

from app.models.models import User


class PermissionChecker:

    def __init__(self, required_roles: list[int]) -> None:
        self.required_roles = required_roles

    def __call__(self, user: User = Depends(get_current_user)) -> bool:
        if user.role_id not in self.required_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='You don\'t have permission to access this resource'
            )
            
        return True