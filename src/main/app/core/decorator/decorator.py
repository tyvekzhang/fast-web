from functools import wraps

from fastapi import HTTPException

from src.main.app.core.service.permission_service import ss

permission_service = ss


def require_access(menu_path: str, permission_code: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            user_id = request.state.user_id

            # 先验证菜单权限
            if not await permission_service.check_menu_access(
                user_id, menu_path
            ):
                raise HTTPException(status_code=403, detail="No menu access")

            # 如果有操作权限要求，再验证操作权限
            if (
                permission_code
                and not await permission_service.check_operation_permission(
                    user_id, permission_code
                )
            ):
                raise HTTPException(
                    status_code=403, detail="No operation permission"
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
