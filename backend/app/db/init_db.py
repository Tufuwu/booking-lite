from sqlalchemy.ext.asyncio import AsyncSession

from . import models
from app.core import security
from app.crud import permissions, roles, users


async def init_roles(db: AsyncSession):
    role_names = ["admin", "staff", "guest"]

    for name in role_names:
        existing = await roles.get_by_name(db, name)
        if not existing:
            db.add(models.Role(name=name))

    await db.commit()


async def init_permissions(db: AsyncSession):
    permissions_data = [
        {"name": "View rooms", "code": "room:view"},
        {"name": "Create rooms", "code": "room:create"},
        {"name": "Delete rooms", "code": "room:delete"},
        {"name": "Create orders", "code": "order:create"},
        {"name": "View orders", "code": "order:view"},
        {"name": "Read order", "code": "order:read"},
        {"name": "List orders", "code": "order:list"},
        {"name": "Update order", "code": "order:update"},
        {"name": "Cancel order", "code": "order:cancel"},
        {"name": "Refund order", "code": "order:refund"},
        {"name": "View users", "code": "user:view"},
        {"name": "Create users", "code": "user:create"},
    ]

    for perm in permissions_data:
        existing = await permissions.get_by_code(db, perm["code"])
        if not existing:
            db.add(models.Permission(name=perm["name"], code=perm["code"]))

    await db.commit()


async def init_role_permissions(db: AsyncSession):
    admin_role = await roles.get_by_name(db, "admin")
    staff_role = await roles.get_by_name(db, "staff")
    guest_role = await roles.get_by_name(db, "guest")

    all_permissions = await permissions.get_all(db)

    role_permission_map = {
        "admin": [p.code for p in all_permissions],
        "staff": [
            "room:view",
            "order:view",
            "order:read",
            "order:list",
            "order:create",
            "order:update",
            "order:refund",
        ],
        "guest": [
            "room:view",
            "order:create",
            "order:read",
            "order:list",
        ],
    }

    for role, perm_codes in role_permission_map.items():
        role_obj = {
            "admin": admin_role,
            "staff": staff_role,
            "guest": guest_role,
        }[role]

        for code in perm_codes:
            perm = await permissions.get_by_code(db, code)
            if perm and perm not in role_obj.permissions:
                role_obj.permissions.append(perm)

    await db.commit()


async def init_admin_user(db: AsyncSession):
    existing = await users.get_by_user_name(db, "admin")
    if existing:
        return

    admin_role = await roles.get_by_name(db, "admin")
    if not admin_role:
        raise RuntimeError("Admin role not initialized")

    admin_user = models.User(
        name="admin",
        phone_number="0000000000",
        identity_number="000000000000000000",
        hashed_password=security.hash_password("123"),
        role_id=admin_role.id,
    )

    await users.create_user(db, admin_user)
    await db.commit()


async def init_db(db: AsyncSession):
    await init_roles(db)
    await init_permissions(db)
    await init_role_permissions(db)
    await init_admin_user(db)
