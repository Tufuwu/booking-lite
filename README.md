# Booking Lite

Booking Lite 是一个轻量级酒店预订系统，包含 FastAPI 后端和 Vue 前端。项目支持用户登录、房间管理、订单创建、订单状态流转、库存占用与释放，并已补充后端核心业务单元测试、GitHub Actions CI 和 Docker Compose 容器化部署配置。

## 技术栈

- 后端：FastAPI、SQLAlchemy Async、SQLite、Redis、Poetry
- 前端：Vue 3、Vite、TypeScript、Pinia、Vue Router、Axios
- 测试：Pytest
- 部署：Docker、Docker Compose、Nginx
- CI：GitHub Actions

## 项目结构

```text
booking-lite/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/             # 路由
│   │   ├── core/            # 权限、锁、安全相关逻辑
│   │   ├── crud/            # 数据访问封装
│   │   ├── db/              # 数据库、Redis、模型
│   │   ├── schemas/         # Pydantic 请求/响应模型
│   │   └── services/        # 核心业务逻辑
│   ├── tests/               # Pytest 单元测试
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                # Vue 前端
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── .github/workflows/ci.yml # GitHub Actions
├── docker-compose.yml
└── .env.example
```

## 环境要求

- Python 3.11
- Poetry 2.x
- Node.js 22
- Docker Desktop 或 Docker Engine
- Redis，本地开发时如需运行完整库存锁逻辑需要启动 Redis

## 本地开发

### 后端

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

后端默认使用本地 SQLite：

```text
sqlite+aiosqlite:///./hotel_booking.db
```

可通过环境变量覆盖：

```bash
DATABASE_URL=sqlite+aiosqlite:///./hotel_booking.db
REDIS_HOST=localhost
REDIS_PORT=6379
JWT_SECRET_KEY=replace-with-a-long-random-secret
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

健康检查：

```text
GET http://localhost:8000/health
```

### 前端

```bash
cd frontend
npm ci
npm run dev
```

开发环境前端默认访问：

```text
http://localhost:5173
```

Vite 已配置 `/api` 代理到本地后端 `http://127.0.0.1:8000`。

## 测试

后端核心业务测试覆盖订单状态流转、库存扣减、库存释放和库存冲突回滚。

```bash
cd backend
poetry run pytest tests
```

前端构建校验：

```bash
cd frontend
npm run build
```

## Docker 部署

复制环境变量示例并修改密钥：

```bash
copy .env.example .env
```

启动服务：

```bash
docker compose up --build
```

服务地址：

- 前端：`http://localhost:8080`
- 后端：`http://localhost:8000`
- 后端健康检查：`http://localhost:8000/health`

Compose 会启动三个服务：

- `frontend`：Nginx 托管 Vue 静态资源，并将 `/api` 反向代理到后端
- `backend`：FastAPI 应用
- `redis`：订单库存锁和缓存服务

SQLite 数据库文件挂载在 Docker volume `backend-data` 中，容器重建后数据仍会保留。

停止服务：

```bash
docker compose down
```

如需同时删除数据库 volume：

```bash
docker compose down -v
```

## GitHub Actions

项目已配置 CI：

```text
.github/workflows/ci.yml
```

在推送到 `main` / `master` 或创建 Pull Request 时会运行：

- 后端：安装 Poetry 依赖并执行 `poetry run pytest tests`
- 前端：执行 `npm ci` 和 `npm run build`

## 常见问题

### GitHub Actions 报 `ModuleNotFoundError`

Linux 环境区分文件名大小写。项目中的 schema 导入已统一使用实际文件名，例如：

```python
from .rooms import RoomCreate
```

新增 Python 模块时建议统一使用小写文件名。

### Docker 中 Redis 不能连接

容器内的 `localhost` 指向当前容器自身。部署时应通过环境变量使用 Compose 服务名：

```text
REDIS_HOST=redis
```

### 前端接口地址怎么配置

前端代码使用 `/api` 作为接口前缀。开发环境由 Vite 代理到后端；Docker 环境由 Nginx 将 `/api` 代理到 `backend:8000`。
