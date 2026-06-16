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
  const [error, setError] = useState("");

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

  async function run(action) {
    try {
      setError("");
      await action();
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    run(async () => refresh());
  }, []);

  return (
    <>
      {error && <div className="toast">{error}</div>}
      <Dashboard
        orders={orders}
        workers={workers}
        onCreateOrder={(payload) => run(() => api.createOrder(payload))}
        onCreateWorker={(payload) => run(() => api.createWorker(payload))}
        onClaim={(orderId, workerId) => run(() => api.claimOrder(orderId, workerId))}
        onAssign={(orderId, workerId) => run(() => api.assignOrder(orderId, workerId))}
        onProgress={(orderId, payload) => run(() => api.addProgress(orderId, payload))}
        onReview={(orderId, payload) => run(() => api.createReview(orderId, payload))}
      />
    </>
  );
}
