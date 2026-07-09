import { CATEGORY_COLORS, formatDate } from "../utils";

export default function EventPanel({ events, selectedEvent, onEventSelect, eventMetrics }) {
  return (
    <div className="card">
      <div className="card-header">
        <h2>Market Events</h2>
        <p>15 curated geopolitical, OPEC, and economic events.</p>
      </div>
      <div className="event-list">
        {events.map((event) => (
          <button
            key={event.event_id}
            className={`event-item ${selectedEvent?.event_id === event.event_id ? "active" : ""}`}
            onClick={() => onEventSelect(event)}
          >
            <div className="event-top">
              <span
                className="category-badge"
                style={{ backgroundColor: CATEGORY_COLORS[event.category] || "#95a5a6" }}
              >
                {event.category}
              </span>
              <span className="event-date">{formatDate(event.date)}</span>
            </div>
            <strong>{event.event_name}</strong>
            <p>{event.description}</p>
          </button>
        ))}
      </div>

      {eventMetrics && (
        <div className="metrics-panel">
          <h3>Event Impact Metrics</h3>
          <div className="metrics-grid">
            <div>
              <span>Pre-event avg</span>
              <strong>${eventMetrics.pre_mean_price}</strong>
            </div>
            <div>
              <span>Post-event avg</span>
              <strong>${eventMetrics.post_mean_price}</strong>
            </div>
            <div>
              <span>Price change</span>
              <strong className={eventMetrics.pct_change >= 0 ? "positive" : "negative"}>
                {eventMetrics.pct_change > 0 ? "+" : ""}
                {eventMetrics.pct_change}%
              </strong>
            </div>
            <div>
              <span>Volatility (ann.)</span>
              <strong>{eventMetrics.annualized_volatility}%</strong>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
