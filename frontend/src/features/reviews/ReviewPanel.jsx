import { Star } from "lucide-react";
import { useState } from "react";

export default function ReviewPanel({ orders, onReview }) {
  const completedOrders = orders.filter((order) => order.status === "completed");
  const [orderId, setOrderId] = useState("");
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  async function submit(event) {
    event.preventDefault();
    if (!orderId) return;
    await onReview(Number(orderId), { rating: Number(rating), comment });
    setComment("");
  }

  return (
    <div className="panel">
      <div className="panel-title">
        <Star size={20} />
        <h3>完成评价</h3>
      </div>
      <form className="review-form" onSubmit={submit}>
        <select value={orderId} onChange={(e) => setOrderId(e.target.value)}>
          <option value="">选择已完成订单</option>
          {completedOrders.map((order) => (
            <option value={order.id} key={order.id}>{order.customer_name} · {order.destination}</option>
          ))}
        </select>
        <input type="number" min="1" max="5" value={rating} onChange={(e) => setRating(e.target.value)} />
        <textarea rows="3" placeholder="客户评价" value={comment} onChange={(e) => setComment(e.target.value)} />
        <button className="primary-button" type="submit">提交评价</button>
      </form>
    </div>
  );
}
