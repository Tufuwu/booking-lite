from sqlalchemy.ext.asyncio import AsyncSession
from . import models
from app.crud import roles, users,permissions
from app.core import security

async def init_roles(db: AsyncSession):
    role_names = ["admin", "staff", "guest"]

    for name in role_names:
        existing = await roles.get_by_name(db, name)
        if not existing:
            db.add(models.Role(name=name))

    await db.commit()


async def init_permissions(db: AsyncSession):
    permissions_data = [
        # room
        {"name": "查看房间", "code": "room:view"},
        {"name": "创建房间", "code": "room:create"},
        {"name": "删除房间", "code": "room:delete"},

        # order
        {"name": "创建订单", "code": "order:create"},
        {"name": "查看订单", "code": "order:view"},
        {"name": "取消订单", "code": "order:cancel"},

        # user
        {"name": "查看用户", "code": "user:view"},
        {"name": "创建用户", "code": "user:create"},
    ]

    for perm in permissions_data:
        existing = await permissions.get_by_code(db, perm["code"])
        if not existing:
            db.add(models.Permission(
                name=perm["name"],
                code=perm["code"]
            ))

    await db.commit()

async def init_role_permissions(db: AsyncSession):
    # 1. 获取角色
    admin_role = await roles.get_by_name(db, "admin")
    staff_role = await roles.get_by_name(db, "staff")
    guest_role = await roles.get_by_name(db, "guest")

    # 2. 获取所有权限
    all_permissions = await permissions.get_all(db)

    # 3. 构建权限映射
    role_permission_map = {
        "admin": [p.code for p in all_permissions],  # 全权限

        "staff": [
            "room:view",
            "order:view",
            "order:create",
        ],

        "guest": [
            "room:view",
            "order:create",
        ]
    }

    # 4. 分配权限
    for role, perm_codes in role_permission_map.items():
        role_obj = {
            "admin": admin_role,
            "staff": staff_role,
            "guest": guest_role
        }[role]

        for code in perm_codes:
            perm = await permissions.get_by_code(db, code)

            if perm not in role_obj.permissions:
                role_obj.permissions.append(perm)

    await db.commit()
async def init_admin_user(db: AsyncSession):
    # 1. 检查是否已存在管理员
    existing = await users.get_by_user_name(db, "admin")
    if existing:
        return

    # 2. 获取 admin 角色
    admin_role = await roles.get_by_name(db, "admin")
    if not admin_role:
        raise RuntimeError("Admin role 未初始化")

    # 3. 创建管理员用户（建议从环境变量取密码）
    hashed_password = security.hash_password("123")

    admin_user = models.User(
        name="admin",
        phone_number=0000000000,
        identity_number="000000000000000000",
        hashed_password=hashed_password,
        role_id=admin_role.id
    )

    await users.create_user(db, admin_user)
    await db.commit()


async def init_db(db: AsyncSession):
    await init_roles(db)

    await init_permissions(db)

    await init_role_permissions(db)

    await init_admin_user(db)
