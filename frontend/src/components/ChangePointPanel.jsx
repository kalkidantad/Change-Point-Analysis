import { formatAnalysisName, formatDate } from "../utils";

export default function ChangePointPanel({ changePoints, associations, selectedAnalysis, onAnalysisSelect }) {
  return (
    <div className="card">
      <div className="card-header">
        <h2>Change Point Results</h2>
        <p>Bayesian posterior estimates from PyMC models.</p>
      </div>

      <div className="change-point-grid">
        {changePoints.map((cp) => (
          <button
            key={cp.name}
            className={`cp-card ${selectedAnalysis === cp.name ? "active" : ""}`}
            onClick={() => onAnalysisSelect(cp.name)}
          >
            <h3>{formatAnalysisName(cp.name)}</h3>
            <p className="cp-date">{formatDate(cp.tau_summary.tau_median_date)}</p>
            <div className="cp-stats">
              <span>
                ${cp.price_impact.pre_period_mean_price} → ${cp.price_impact.post_period_mean_price}
              </span>
              <strong className={cp.price_impact.price_pct_change >= 0 ? "positive" : "negative"}>
                {cp.price_impact.price_pct_change > 0 ? "+" : ""}
                {cp.price_impact.price_pct_change}%
              </strong>
            </div>
            <small>P(μ₂ &gt; μ₁) = {(cp.impact_summary.prob_mu2_greater_mu1 * 100).toFixed(1)}%</small>
          </button>
        ))}
      </div>

      {selectedAnalysis && (
        <div className="association-table-wrap">
          <h3>Event Associations — {formatAnalysisName(selectedAnalysis)}</h3>
          <table>
            <thead>
              <tr>
                <th>Event</th>
                <th>Date</th>
                <th>Days from τ</th>
                <th>Within HDI</th>
              </tr>
            </thead>
            <tbody>
              {associations
                .filter((row) => row.analysis === selectedAnalysis)
                .map((row) => (
                  <tr key={`${row.analysis}-${row.event_id}`}>
                    <td>{row.event_name}</td>
                    <td>{formatDate(row.event_date)}</td>
                    <td>{row.days_from_change_point}</td>
                    <td>{row.within_hdi ? "Yes" : "No"}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
