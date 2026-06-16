import { CalendarPlus } from "lucide-react";
import { useState } from "react";

const initialState = {
  customer_name: "",
  customer_phone: "",
  origin: "",
  destination: "",
  move_date: "",
  move_time: "09:00",
  items: "",
  note: "",
};

export default function OrderForm({ onCreate }) {
  const [form, setForm] = useState(initialState);
  const [submitting, setSubmitting] = useState(false);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    await onCreate(form);
    setForm(initialState);
    setSubmitting(false);
  }

  return (
    <form className="panel order-form" onSubmit={handleSubmit}>
      <div className="panel-title">
        <CalendarPlus size={20} />
        <h3>客户下单预约</h3>
      </div>
      <div className="form-grid">
        <label>
          客户姓名
          <input value={form.customer_name} onChange={(e) => update("customer_name", e.target.value)} required />
        </label>
        <label>
          联系电话
          <input value={form.customer_phone} onChange={(e) => update("customer_phone", e.target.value)} required />
        </label>
        <label>
          搬出地址
          <input value={form.origin} onChange={(e) => update("origin", e.target.value)} required />
        </label>
        <label>
          搬入地址
          <input value={form.destination} onChange={(e) => update("destination", e.target.value)} required />
        </label>
        <label>
          预约日期
          <input type="date" value={form.move_date} onChange={(e) => update("move_date", e.target.value)} required />
        </label>
        <label>
          预约时间
          <input type="time" value={form.move_time} onChange={(e) => update("move_time", e.target.value)} required />
        </label>
      </div>
      <label>
        物品清单
        <textarea value={form.items} onChange={(e) => update("items", e.target.value)} rows="3" />
      </label>
      <label>
        备注
        <textarea value={form.note} onChange={(e) => update("note", e.target.value)} rows="2" />
      </label>
      <button className="primary-button" type="submit" disabled={submitting}>
        提交预约
      </button>
    </form>
  );
}
