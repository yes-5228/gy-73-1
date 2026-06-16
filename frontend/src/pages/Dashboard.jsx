import SectionHeader from "../components/SectionHeader.jsx";
import OrderBoard from "../features/orders/OrderBoard.jsx";
import OrderForm from "../features/orders/OrderForm.jsx";
import ReviewPanel from "../features/reviews/ReviewPanel.jsx";
import TrackingPanel from "../features/tracking/TrackingPanel.jsx";
import WorkerPanel from "../features/workers/WorkerPanel.jsx";

export default function Dashboard({
  orders,
  workers,
  onCreateOrder,
  onCreateWorker,
  onClaim,
  onAssign,
  onProgress,
  onReview,
}) {
  const stats = [
    ["待处理订单", orders.filter((order) => order.status !== "completed").length],
    ["服务中", orders.filter((order) => order.status === "in_progress").length],
    ["师傅数量", workers.length],
    ["已完成", orders.filter((order) => order.status === "completed").length],
  ];

  return (
    <main>
      <section className="hero">
        <div>
          <p>搬家公司调度系统</p>
          <h1>预约、抢单、派单、跟踪和评价一体化工作台</h1>
        </div>
        <div className="stats-strip">
          {stats.map(([label, value]) => (
            <div key={label}>
              <strong>{value}</strong>
              <span>{label}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="content">
        <SectionHeader eyebrow="Dispatch Center" title="调度总览" />
        <div className="layout-grid">
          <OrderForm onCreate={onCreateOrder} />
          <WorkerPanel workers={workers} onCreate={onCreateWorker} />
          <OrderBoard orders={orders} workers={workers} onClaim={onClaim} onAssign={onAssign} />
          <div className="side-stack">
            <TrackingPanel orders={orders} onProgress={onProgress} />
            <ReviewPanel orders={orders} onReview={onReview} />
          </div>
        </div>
      </section>
    </main>
  );
}
