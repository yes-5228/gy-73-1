export default function SectionHeader({ eyebrow, title, actions }) {
  return (
    <div className="section-header">
      <div>
        <p>{eyebrow}</p>
        <h2>{title}</h2>
      </div>
      {actions}
    </div>
  );
}
