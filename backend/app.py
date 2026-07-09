"""Flask API for Brent oil change point analysis dashboard."""

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.data_service import (
    get_change_points,
    get_event_associations,
    get_event_metrics,
    get_events,
    get_prices,
    get_summary,
)


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "brent-oil-dashboard-api"})

    @app.get("/api/summary")
    def summary():
        return jsonify(get_summary())

    @app.get("/api/prices")
    def prices():
        start = request.args.get("start")
        end = request.args.get("end")
        return jsonify({"data": get_prices(start=start, end=end), "count": len(get_prices(start, end))})

    @app.get("/api/events")
    def events():
        category = request.args.get("category")
        data = get_events(category=category)
        return jsonify({"data": data, "count": len(data)})

    @app.get("/api/change-points")
    def change_points():
        return jsonify({"data": get_change_points(), "count": len(get_change_points())})

    @app.get("/api/event-associations")
    def event_associations():
        analysis = request.args.get("analysis")
        data = get_event_associations(analysis=analysis)
        return jsonify({"data": data, "count": len(data)})

    @app.get("/api/events/<int:event_id>/metrics")
    def event_metrics(event_id: int):
        window_days = request.args.get("window_days", default=30, type=int)
        data = get_event_metrics(event_id=event_id, window_days=window_days)
        if not data:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(data)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
