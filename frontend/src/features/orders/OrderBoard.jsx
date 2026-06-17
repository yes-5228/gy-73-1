import { useState } from "react";
import { ClipboardList, Truck, X } from "lucide-react";

import StatusBadge from "../../components/StatusBadge.jsx";

export default function OrderBoard({ orders, workers, onClaim, onAssign, onCancel }) {
  const [cancellingOrder, setCancellingOrder] = useState(null);
  const [cancelReason, setCancelReason] = useState("");
  const [cancelledBy, setCancelledBy] = useState("dispatcher");
  const [cancelling, setCancelling] = useState(false);
  const [cancelError, setCancelError] = useState("");

  function openCancelDialog(order) {
    setCancellingOrder(order);
    setCancelReason("");
    setCancelledBy("dispatcher");
    setCancelError("");
  }

  function closeCancelDialog() {
    if (cancelling) return;
    setCancellingOrder(null);
    setCancelReason("");
    setCancelError("");
  }

  async function handleCancel() {
    if (!cancelReason.trim() || cancelling) return;
    setCancelling(true);
    setCancelError("");
    try {
      await onCancel(cancellingOrder.id, {
        cancel_reason: cancelReason.trim(),
        cancelled_by: cancelledBy,
      });
      closeCancelDialog();
    } catch (err) {
      setCancelError(err.message || "取消失败，请重试");
    } finally {
      setCancelling(false);
    }
  }

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
            {order.status === "cancelled" && (
              <p className="cancel-info">
                <strong>取消原因：</strong>{order.cancel_reason}
                <br />
                <strong>取消方：</strong>{order.cancelled_by_label}
              </p>
            )}
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
                disabled={order.status === "completed" || order.status === "in_progress" || order.status === "cancelled"}
              >
                <option value="">平台派单</option>
                {workers.map((worker) => (
                  <option value={worker.id} key={worker.id}>{worker.name}</option>
                ))}
              </select>
              {order.is_cancellable && (
                <button className="btn-cancel" onClick={() => openCancelDialog(order)}>
                  <X size={14} />
                  取消订单
                </button>
              )}
            </div>
          </article>
        ))}
        {orders.length === 0 && <p className="empty">暂无订单</p>}
      </div>

      {cancellingOrder && (
        <div className="modal-overlay" onClick={closeCancelDialog}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-head">
              <h3>取消订单</h3>
              <button className="modal-close" onClick={closeCancelDialog}>
                <X size={18} />
              </button>
            </div>
            <div className="modal-body">
              <p>确定要取消 <strong>{cancellingOrder.customer_name}</strong> 的订单吗？</p>
              {cancelError && <div className="form-error">{cancelError}</div>}
              <div className="form-group">
                <label>取消原因</label>
                <textarea
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value)}
                  placeholder="请填写取消原因..."
                  rows={3}
                  disabled={cancelling}
                />
              </div>
              <div className="form-group">
                <label>取消发起方</label>
                <select value={cancelledBy} onChange={(e) => setCancelledBy(e.target.value)} disabled={cancelling}>
                  <option value="dispatcher">调度员取消</option>
                  <option value="customer">客户取消</option>
                </select>
              </div>
            </div>
            <div className="modal-foot">
              <button className="btn-secondary" onClick={closeCancelDialog} disabled={cancelling}>取消</button>
              <button
                className="btn-danger"
                onClick={handleCancel}
                disabled={!cancelReason.trim() || cancelling}
              >
                {cancelling ? "取消中..." : "确认取消"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
