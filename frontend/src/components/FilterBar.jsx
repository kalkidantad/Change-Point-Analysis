export default function FilterBar({
  startDate,
  endDate,
  category,
  onStartDateChange,
  onEndDateChange,
  onCategoryChange,
  onReset,
}) {
  return (
    <div className="filter-bar card">
      <div className="filter-group">
        <label htmlFor="start-date">Start Date</label>
        <input
          id="start-date"
          type="date"
          value={startDate}
          onChange={(e) => onStartDateChange(e.target.value)}
        />
      </div>
      <div className="filter-group">
        <label htmlFor="end-date">End Date</label>
        <input
          id="end-date"
          type="date"
          value={endDate}
          onChange={(e) => onEndDateChange(e.target.value)}
        />
      </div>
      <div className="filter-group">
        <label htmlFor="category">Event Category</label>
        <select id="category" value={category} onChange={(e) => onCategoryChange(e.target.value)}>
          <option value="">All categories</option>
          <option value="Conflict">Conflict</option>
          <option value="OPEC">OPEC</option>
          <option value="Economic">Economic</option>
          <option value="Geopolitical">Geopolitical</option>
        </select>
      </div>
      <button className="reset-btn" onClick={onReset}>
        Reset Filters
      </button>
    </div>
  );
}
