import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { CATEGORY_COLORS, formatDate } from "../utils";

export default function PriceChart({ prices, events, changePoints, selectedEvent, onEventSelect }) {
  const changePointDates = changePoints.flatMap((cp) => [
    cp.tau_summary?.tau_median_date,
    cp.tau_summary?.tau_hdi_lower_date,
    cp.tau_summary?.tau_hdi_upper_date,
  ].filter(Boolean));

  return (
    <div className="card chart-card">
      <div className="card-header">
        <h2>Brent Oil Price History</h2>
        <p>Click an event below to highlight its impact window on the chart.</p>
      </div>
      <ResponsiveContainer width="100%" height={420}>
        <LineChart data={prices} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e8edf2" />
          <XAxis
            dataKey="date"
            tickFormatter={(value) => value.slice(0, 7)}
            minTickGap={40}
            stroke="#6b7c93"
          />
          <YAxis
            domain={["auto", "auto"]}
            tickFormatter={(value) => `$${value}`}
            stroke="#6b7c93"
          />
          <Tooltip
            formatter={(value) => [`$${Number(value).toFixed(2)}`, "Price"]}
            labelFormatter={(label) => formatDate(label)}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="price"
            name="Brent Price"
            stroke="#1a3a5c"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
          />
          {events.map((event) => (
            <ReferenceLine
              key={event.event_id}
              x={event.date}
              stroke={CATEGORY_COLORS[event.category] || "#95a5a6"}
              strokeDasharray={selectedEvent?.event_id === event.event_id ? "0" : "4 4"}
              strokeWidth={selectedEvent?.event_id === event.event_id ? 3 : 1}
              strokeOpacity={selectedEvent && selectedEvent.event_id !== event.event_id ? 0.25 : 0.9}
            />
          ))}
          {changePointDates.map((date, index) => (
            <ReferenceLine
              key={`${date}-${index}`}
              x={date}
              stroke="#16a085"
              strokeDasharray="6 3"
              strokeOpacity={0.5}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
