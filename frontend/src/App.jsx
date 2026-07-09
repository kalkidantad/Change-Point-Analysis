import { useCallback, useEffect, useState } from "react";
import { api } from "./api";
import ChangePointPanel from "./components/ChangePointPanel";
import EventPanel from "./components/EventPanel";
import FilterBar from "./components/FilterBar";
import PriceChart from "./components/PriceChart";

const DEFAULT_START = "2014-01-01";
const DEFAULT_END = "2022-09-30";

export default function App() {
  const [summary, setSummary] = useState(null);
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [associations, setAssociations] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [eventMetrics, setEventMetrics] = useState(null);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [startDate, setStartDate] = useState(DEFAULT_START);
  const [endDate, setEndDate] = useState(DEFAULT_END);
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboardData = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [summaryRes, pricesRes, eventsRes, cpRes, assocRes] = await Promise.all([
        api.getSummary(),
        api.getPrices(startDate, endDate),
        api.getEvents(category || undefined),
        api.getChangePoints(),
        api.getEventAssociations(),
      ]);

      setSummary(summaryRes);
      setPrices(pricesRes.data);
      setEvents(eventsRes.data);
      setChangePoints(cpRes.data);
      setAssociations(assocRes.data);
      if (!selectedAnalysis && cpRes.data.length > 0) {
        setSelectedAnalysis(cpRes.data[0].name);
      }
    } catch (err) {
      setError(err.message || "Failed to load dashboard data.");
    } finally {
      setLoading(false);
    }
  }, [startDate, endDate, category, selectedAnalysis]);

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const handleEventSelect = async (event) => {
    setSelectedEvent(event);
    try {
      const metrics = await api.getEventMetrics(event.event_id);
      setEventMetrics(metrics);
      const eventDate = new Date(event.date);
      const start = new Date(eventDate);
      start.setMonth(start.getMonth() - 6);
      const end = new Date(eventDate);
      end.setMonth(end.getMonth() + 6);
      setStartDate(start.toISOString().slice(0, 10));
      setEndDate(end.toISOString().slice(0, 10));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleReset = () => {
    setStartDate(DEFAULT_START);
    setEndDate(DEFAULT_END);
    setCategory("");
    setSelectedEvent(null);
    setEventMetrics(null);
  };

  if (loading) {
    return <div className="loading-screen">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="error-screen">
        <h1>Dashboard unavailable</h1>
        <p>{error}</p>
        <p>Ensure the Flask API is running on port 5000.</p>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">Birhan Energies · Week 10 Challenge</p>
          <h1>Brent Oil Change Point Dashboard</h1>
          <p className="subtitle">
            Explore how geopolitical events, OPEC decisions, and economic shocks align with
            detected structural breaks in Brent crude oil prices.
          </p>
        </div>
        {summary && (
          <div className="hero-stats">
            <div>
              <span>Observations</span>
              <strong>{summary.total_observations.toLocaleString()}</strong>
            </div>
            <div>
              <span>Price Range</span>
              <strong>
                ${summary.price_stats.min} – ${summary.price_stats.max}
              </strong>
            </div>
            <div>
              <span>Annual Volatility</span>
              <strong>{summary.annualized_volatility}%</strong>
            </div>
            <div>
              <span>Change Point Models</span>
              <strong>{summary.num_change_point_analyses}</strong>
            </div>
          </div>
        )}
      </header>

      <main className="dashboard">
        <FilterBar
          startDate={startDate}
          endDate={endDate}
          category={category}
          onStartDateChange={setStartDate}
          onEndDateChange={setEndDate}
          onCategoryChange={setCategory}
          onReset={handleReset}
        />

        <PriceChart
          prices={prices}
          events={events}
          changePoints={changePoints}
          selectedEvent={selectedEvent}
          onEventSelect={handleEventSelect}
        />

        <section className="two-column">
          <EventPanel
            events={events}
            selectedEvent={selectedEvent}
            onEventSelect={handleEventSelect}
            eventMetrics={eventMetrics}
          />
          <ChangePointPanel
            changePoints={changePoints}
            associations={associations}
            selectedAnalysis={selectedAnalysis}
            onAnalysisSelect={setSelectedAnalysis}
          />
        </section>
      </main>
    </div>
  );
}
