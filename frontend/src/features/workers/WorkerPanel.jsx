import { UserPlus, Users } from "lucide-react";
import { useState } from "react";

import StatusBadge from "../../components/StatusBadge.jsx";

const initialWorker = {
  name: "",
  phone: "",
  vehicle: "",
  service_area: "",
  rating: 5,
};

export default function WorkerPanel({ workers, onCreate }) {
  const [form, setForm] = useState(initialWorker);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    await onCreate(form);
    setForm(initialWorker);
  }

  return (
    <div className="panel">
      <div className="panel-title">
        <Users size={20} />
        <h3>师傅管理</h3>
      </div>
      <form className="worker-form" onSubmit={submit}>
        <input placeholder="姓名" value={form.name} onChange={(e) => update("name", e.target.value)} required />
        <input placeholder="电话" value={form.phone} onChange={(e) => update("phone", e.target.value)} required />
        <input placeholder="车辆" value={form.vehicle} onChange={(e) => update("vehicle", e.target.value)} required />
        <input placeholder="服务区域" value={form.service_area} onChange={(e) => update("service_area", e.target.value)} />
        <button className="icon-button" type="submit" title="新增师傅">
          <UserPlus size={18} />
        </button>
      </form>
      <div className="worker-list">
        {workers.map((worker) => (
          <div className="worker-row" key={worker.id}>
            <div>
              <strong>{worker.name}</strong>
              <p>{worker.vehicle} · {worker.service_area}</p>
            </div>
            <div className="worker-meta">
              <span>{worker.rating.toFixed(1)} 星</span>
              <StatusBadge status={worker.status} label={worker.status_label} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
