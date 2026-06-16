const toneMap = {
  pending: "blue",
  claimed: "amber",
  assigned: "violet",
  in_progress: "green",
  completed: "neutral",
  available: "green",
  busy: "amber",
  offline: "neutral",
};

export default function StatusBadge({ status, label }) {
  return <span className={`status status-${toneMap[status] || "neutral"}`}>{label || status}</span>;
}
