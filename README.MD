# 搬家公司调度系统

Django + React 实现的搬家公司调度工作台，覆盖客户下单预约、师傅抢单、平台派单、服务进度跟踪和完成后评价。

## 模块结构

```text
backend/
  move_dispatch/      Django 项目配置与根路由
  orders/             预约订单、抢单、派单接口
  workers/            师傅档案与接单状态
  tracking/           订单进度事件
  reviews/            服务完成后的客户评价
frontend/
  src/api/            API 客户端
  src/components/     通用 UI 组件
  src/features/       orders/workers/tracking/reviews 功能模块
  src/pages/          页面级组合
```

## 本地启动

后端：

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

前端：

```bash
cd frontend
npm install
npm run dev
```

访问 `http://127.0.0.1:5173`。

## Docker Compose 启动

```bash
npm --prefix frontend install
npm --prefix frontend run build
docker compose up --build
```

前端地址：`http://127.0.0.1:19073`

后端健康检查：`http://127.0.0.1:19073/api/health/`

Compose 模式下后端不直接暴露宿主机端口，前端 Nginx 会把 `/api/` 代理到内部 `backend:8000`，避免和本机已有 8000 端口服务冲突。

## 主要接口

- `GET /api/orders/`：订单列表
- `POST /api/orders/`：创建客户预约
- `POST /api/orders/{id}/claim/`：师傅抢单
- `POST /api/orders/{id}/assign/`：平台派单
- `POST /api/tracking/orders/{id}/events/`：更新服务进度
- `POST /api/reviews/orders/{id}/`：服务完成后评价
- `GET /api/workers/`：师傅列表

## 验证

项目完成时已执行：

```bash
python manage.py check
npm run build
```

同时使用 Django 测试客户端验证了健康检查、订单列表、师傅列表，以及“创建预约 -> 抢单 -> 派单 -> 完成进度 -> 提交评价”的完整业务链路。

说明：如果本机 `8000` 端口已被占用，本地后端可改用其他端口，例如：

```bash
python manage.py runserver 127.0.0.1:18033
```

然后启动前端时设置：

```bash
VITE_API_BASE=http://127.0.0.1:18033/api npm run dev
```
