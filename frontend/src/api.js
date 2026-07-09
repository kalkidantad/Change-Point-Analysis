const API_BASE = import.meta.env.VITE_API_URL || "";

async function fetchJson(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }
  return response.json();
}

export const api = {
  getSummary: () => fetchJson("/api/summary"),
  getPrices: (start, end) => {
    const params = new URLSearchParams();
    if (start) params.set("start", start);
    if (end) params.set("end", end);
    const query = params.toString();
    return fetchJson(`/api/prices${query ? `?${query}` : ""}`);
  },
  getEvents: (category) => {
    const params = category ? `?category=${encodeURIComponent(category)}` : "";
    return fetchJson(`/api/events${params}`);
  },
  getChangePoints: () => fetchJson("/api/change-points"),
  getEventAssociations: (analysis) => {
    const params = analysis ? `?analysis=${encodeURIComponent(analysis)}` : "";
    return fetchJson(`/api/event-associations${params}`);
  },
  getEventMetrics: (eventId, windowDays = 30) =>
    fetchJson(`/api/events/${eventId}/metrics?window_days=${windowDays}`),
};
