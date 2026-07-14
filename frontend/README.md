# React Dashboard — Brent Oil Change Point Analysis

Interactive dashboard for exploring Brent oil prices, market events, and Bayesian change point results.

## Features

- Historical price chart with date range filters
- Event highlight lines by category (Conflict, OPEC, Economic, Geopolitical)
- Click-to-drill-down event impact metrics (pre/post price, volatility)
- Change point results panel with event association table
- Responsive layout for desktop, tablet, and mobile

## Setup

```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at `http://localhost:3000` and proxies API requests to Flask on port 5000.

## Build for production

```bash
npm run build
npm run preview
```

## Tech stack

- React 18 + Vite
- Recharts
- Flask API backend
