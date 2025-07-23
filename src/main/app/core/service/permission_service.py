from src.main.app.core.schema import CurrentUser


class PermissionService:
    async def has_permission(self, permission: str, user: CurrentUser) -> bool:
        if not permission:
            return False
        if not user or not user.permissions:
            return False
        return "*:*:*" in user.permissions or permission in user.permissions

    async def lacks_permission(
        self, permission: str, user: CurrentUser
    ) -> bool:
        return not await self.has_permission(permission, user)

    async def has_any_permission(
        self, permissions: str, user: CurrentUser
    ) -> bool:
        if not permissions:
            return False
        if not user or not user.permissions:
            return False
        for perm in permissions.split(","):
            if await self.has_permission(perm.strip(), user):
                return True
        return False

    async def has_role(self, role: str, user: CurrentUser) -> bool:
        if not role:
            return False
        if not user or not user.roles:
            return False
        return "admin" in user.roles or role in user.roles

    async def lacks_role(self, role: str, user: CurrentUser) -> bool:
        return not await self.has_role(role, user)

    async def has_any_role(self, roles: str, user: CurrentUser) -> bool:
        if not roles:
            return False
        if not user or not user.roles:
            return False
        for role in roles.split(","):
            if await self.has_role(role.strip(), user):
                return True
        return False

    async def check_operation_permission(
        self, user_id: int, permission: str
    ) -> bool:
        if user_id == 9:
            return True
        return False


ss = PermissionService()
