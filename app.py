import matplotlib
matplotlib.use('Agg')  # Force non-GUI backend before any other matplotlib import

import os
import logging
import time
from logging.handlers import RotatingFileHandler
from flask import Flask, Response, request
from dashboard import dashboard_blueprint
from utils import timestamp_to_str  # Import our custom filter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

# --- Prometheus metrics ---
REQUEST_COUNT = Counter("quakewatch_request_count", "Number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("quakewatch_request_latency_seconds", "Request latency", ["endpoint"])

def create_app():
    app = Flask(__name__)

    # -------------------------
    # Logging Configuration
    # -------------------------
    if not os.path.exists('logs'):
        os.makedirs('logs')

    error_handler = RotatingFileHandler('logs/error.log', maxBytes=1000000, backupCount=3)
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(error_formatter)
    app.logger.addHandler(error_handler)

    usage_handler = RotatingFileHandler('logs/access.log', maxBytes=1000000, backupCount=3)
    usage_handler.setLevel(logging.INFO)
    usage_formatter = logging.Formatter('%(asctime)s - %(message)s')
    usage_handler.setFormatter(usage_formatter)
    usage_logger = logging.getLogger('usage')
    usage_logger.addHandler(usage_handler)
    usage_logger.setLevel(logging.INFO)

    @app.before_request
    def before_request():
        request.start_time = time.time()
        usage_logger.info(f"{request.remote_addr} - {request.method} {request.url}")

    @app.after_request
    def after_request(response):
        resp_time = time.time() - request.start_time
        REQUEST_COUNT.labels(request.method, request.path).inc()
        REQUEST_LATENCY.labels(request.path).observe(resp_time)
        return response

    # -------------------------
    # Prometheus Metrics Endpoint
    # -------------------------
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    # Register blueprint
    app.register_blueprint(dashboard_blueprint)

    # Register custom Jinja2 filter
    app.jinja_env.filters['timestamp_to_str'] = timestamp_to_str

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
