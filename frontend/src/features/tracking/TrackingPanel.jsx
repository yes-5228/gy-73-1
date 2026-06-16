import { MapPin } from "lucide-react";
import { useState } from "react";

const stages = [
  ["departed", "已出发"],
  ["loading", "装车中"],
  ["in_transit", "运输中"],
  ["unloading", "卸货中"],
  ["completed", "已完成"],
];

export default function TrackingPanel({ orders, onProgress }) {
  const activeOrders = orders.filter((order) => order.status !== "completed");
  const [orderId, setOrderId] = useState("");
  const [stage, setStage] = useState("departed");

  async function submit(event) {
    event.preventDefault();
    if (!orderId) return;
    const label = stages.find(([value]) => value === stage)?.[1] || stage;
    await onProgress(Number(orderId), { stage, message: `师傅更新进度：${label}` });
  }

  return (
    <div className="panel">
      <div className="panel-title">
        <MapPin size={20} />
        <h3>进度跟踪</h3>
      </div>
      <form className="inline-form" onSubmit={submit}>
        <select value={orderId} onChange={(e) => setOrderId(e.target.value)}>
          <option value="">选择订单</option>
          {activeOrders.map((order) => (
            <option value={order.id} key={order.id}>{order.customer_name} · {order.origin}</option>
          ))}
        </select>
        <select value={stage} onChange={(e) => setStage(e.target.value)}>
          {stages.map(([value, label]) => (
            <option value={value} key={value}>{label}</option>
          ))}
        </select>
        <button className="primary-button" type="submit">更新进度</button>
      </form>
      <div className="timeline">
        {orders.slice(0, 4).map((order) => (
          <div className="timeline-item" key={order.id}>
            <span />
            <div>
              <strong>{order.customer_name}</strong>
              <p>{order.status_label} · {order.assigned_to?.name || order.claimed_by?.name || "待安排"}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
