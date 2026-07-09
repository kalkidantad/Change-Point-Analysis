# Flask API — Brent Oil Dashboard

REST API serving analysis results for the React dashboard.

## Endpoints

| Method | Endpoint | Description | Query Params |
|--------|----------|-------------|--------------|
| GET | `/api/health` | Health check | — |
| GET | `/api/summary` | Dataset summary stats | — |
| GET | `/api/prices` | Historical Brent prices | `start`, `end` (YYYY-MM-DD) |
| GET | `/api/events` | Curated market events | `category` |
| GET | `/api/change-points` | PyMC change point results | — |
| GET | `/api/event-associations` | Event–change point mapping | `analysis` |
| GET | `/api/events/<id>/metrics` | Pre/post event price metrics | `window_days` (default 30) |

## Run locally

```bash
# From project root
source venv/bin/activate
pip install -r requirements.txt
python -m backend.app
```

API runs at `http://localhost:5000`.

## Example

```bash
curl http://localhost:5000/api/summary
curl "http://localhost:5000/api/prices?start=2020-01-01&end=2020-12-31"
curl http://localhost:5000/api/change-points
```
