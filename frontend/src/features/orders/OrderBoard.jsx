import { ClipboardList, Truck } from "lucide-react";

import StatusBadge from "../../components/StatusBadge.jsx";

export default function OrderBoard({ orders, workers, onClaim, onAssign }) {
  return (
    <div className="panel">
      <div className="panel-title">
        <ClipboardList size={20} />
        <h3>订单池与派单</h3>
      </div>
      <div className="order-list">
        {orders.map((order) => (
          <article className="order-card" key={order.id}>
            <div className="order-card-head">
              <div>
                <h4>{order.customer_name}</h4>
                <p>{order.move_date} {order.move_time}</p>
              </div>
              <StatusBadge status={order.status} label={order.status_label} />
            </div>
            <div className="route">
              <span>{order.origin}</span>
              <Truck size={16} />
              <span>{order.destination}</span>
            </div>
            <p className="muted">物品：{order.items || "未填写"}</p>
            <div className="assignment">
              <span>抢单师傅：{order.claimed_by?.name || "暂无"}</span>
              <span>派单师傅：{order.assigned_to?.name || "暂无"}</span>
            </div>
            <div className="button-row">
              <select
                aria-label="选择抢单师傅"
                defaultValue=""
                onChange={(e) => e.target.value && onClaim(order.id, Number(e.target.value))}
                disabled={order.status !== "pending"}
              >
                <option value="">师傅抢单</option>
                {workers.map((worker) => (
                  <option value={worker.id} key={worker.id}>{worker.name}</option>
                ))}
              </select>
              <select
                aria-label="选择派单师傅"
                defaultValue=""
                onChange={(e) => e.target.value && onAssign(order.id, Number(e.target.value))}
                disabled={order.status === "completed" || order.status === "in_progress"}
              >
                <option value="">平台派单</option>
                {workers.map((worker) => (
                  <option value={worker.id} key={worker.id}>{worker.name}</option>
                ))}
              </select>
            </div>
          </article>
        ))}
        {orders.length === 0 && <p className="empty">暂无订单</p>}
      </div>
    </div>
  );
}
