export const CATEGORY_COLORS = {
  Conflict: "#e74c3c",
  OPEC: "#3498db",
  Economic: "#f39c12",
  Geopolitical: "#9b59b6",
};

export const ANALYSIS_LABELS = {
  covid_2020: "COVID 2020",
  opec_price_war: "OPEC Price War",
  financial_crisis: "Financial Crisis",
  ukraine_war: "Ukraine War",
  gulf_war_era: "Gulf War",
};

export function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function formatAnalysisName(name) {
  return ANALYSIS_LABELS[name] || name.replaceAll("_", " ");
}
