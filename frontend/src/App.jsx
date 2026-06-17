import { useEffect, useState } from "react";

import { api } from "./api/client.js";
import Dashboard from "./pages/Dashboard.jsx";

const seedWorkers = [
  { name: "张师傅", phone: "13800000001", vehicle: "4.2米厢货", service_area: "浦东新区", rating: 4.9 },
  { name: "李师傅", phone: "13800000002", vehicle: "金杯面包车", service_area: "徐汇区", rating: 4.8 },
];

export default function App() {
  const [orders, setOrders] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [toast, setToast] = useState(null);

  function showToast(message, type = "error") {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  }

  async function refresh() {
    const [orderData, workerData] = await Promise.all([api.listOrders(), api.listWorkers()]);
    setOrders(orderData.orders);
    setWorkers(workerData.workers);
    if (workerData.workers.length === 0) {
      await Promise.all(seedWorkers.map((worker) => api.createWorker(worker)));
      const seededWorkers = await api.listWorkers();
      setWorkers(seededWorkers.workers);
    }
  }

  async function run(action, successMessage) {
    try {
      setToast(null);
      await action();
      await refresh();
      if (successMessage) {
        showToast(successMessage, "success");
      }
      return true;
    } catch (err) {
      showToast(err.message, "error");
      throw err;
    }
  }

  useEffect(() => {
    run(async () => refresh());
  }, []);

  return (
    <>
      {toast && <div className={`toast toast-${toast.type}`}>{toast.message}</div>}
      <Dashboard
        orders={orders}
        workers={workers}
        onCreateOrder={(payload) => run(() => api.createOrder(payload), "订单创建成功")}
        onCreateWorker={(payload) => run(() => api.createWorker(payload), "师傅添加成功")}
        onClaim={(orderId, workerId) => run(() => api.claimOrder(orderId, workerId), "抢单成功")}
        onAssign={(orderId, workerId) => run(() => api.assignOrder(orderId, workerId), "派单成功")}
        onCancel={(orderId, payload) => run(() => api.cancelOrder(orderId, payload), "订单已取消")}
        onProgress={(orderId, payload) => run(() => api.addProgress(orderId, payload), "进度更新成功")}
        onReview={(orderId, payload) => run(() => api.createReview(orderId, payload), "评价提交成功")}
      />
    </>
  );
}
