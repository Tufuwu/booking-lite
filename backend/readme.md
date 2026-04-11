hotel-system/
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   ├── api/
│   │   ├── services/
│   │   ├── db/
│   │   ├── models/
│   │   └── schemas/
│   │
│   ├── requirements.txt
│   ├── .env
│   └── dockerfile
│
├── frontend/                 # 前端（Web）
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── api/              # 请求封装（axios/fetch）
│   │   ├── store/            # 状态管理
│   │   ├── router/
│   │   └── utils/
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── mobile/                   # 可选（React Native / Flutter）
│   ├── src/
│   └── ...
│
├── shared/                  # ⭐前后端共享（强烈推荐）
│   ├── types/               # TS类型 / OpenAPI生成
│   ├── constants/
│   └── validators/
│
├── infra/                   # 基础设施
│   ├── docker-compose.yml
│   ├── nginx.conf
│   └── redis.conf
│
└── README.md

app/
├── main.py                 # 入口
├── core/                   # 全局配置 & 安全
│   ├── config.py
│   ├── security.py        # JWT / 密码哈希
│   └── constants.py
│
├── db/
│   ├── redis.py           # Redis 连接
│   └── database.py        # (如果有 SQL)
│
├── models/                # ORM / 数据模型
│   ├── user.py
│   └── session.py         # (可选，逻辑模型)
│
├── schemas/               # Pydantic 模型
│   ├── user.py
│   ├── auth.py
│   └── token.py
│
├── services/              # 业务逻辑（核心）
│   ├── auth/
│   │   ├── session_service.py
│   │   ├── jwt_service.py
│   │   └── auth_service.py   # 统一入口（关键）
│   │
│   ├── user_service.py
│   └── booking_service.py
│
├── api/                   # 路由层
│   ├── deps.py            # 依赖注入（get_current_user）
│   │
│   ├── routes/
│   │   ├── web/           # 浏览器（Session）
│   │   │   ├── auth.py
│   │   │   └── user.py
│   │   │
│   │   ├── mobile/        # App（JWT）
│   │   │   ├── auth.py
│   │   │   └── user.py
│   │   │
│   │   └── admin/         # 后台
│   │       ├── auth.py
│   │       └── dashboard.py
│
├── middleware/            # 中间件
│   └── auth_middleware.py  #（可选）
│
└── utils/
    ├── time.py
    └── security.py



frontend/src/
├── pages/
│   ├── Home/
│   ├── RoomList/
│   ├── Booking/
│   ├── Login/
│   └── Admin/
│
├── components/
│   ├── RoomCard/
│   ├── Calendar/
│   └── Navbar/
│
├── api/
│   ├── http.ts         # axios封装
│   ├── auth.ts
│   ├── booking.ts
│
├── store/
│   ├── userStore.ts
│   └── bookingStore.ts