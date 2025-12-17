from flask import render_template, jsonify, request
import time
from dashboard import *

def setup_metrics(app):
    @app.before_request
    def before_request():
        if request.path != '/metrics':
            request.start_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(request, 'start_time') and request.path != '/metrics':
            latency = time.time() - request.start_time
            REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(latency)
            REQUEST_COUNT.labels(method=request.method, endpoint=request.path, status=response.status_code).inc()
        return response

def setup_routes(app, db):
    @app.route('/')
    def home():
        from flask import request
        try:
            data = db.add_visit()
            if data == None:
                DB_ERRORS.labels(operation="add_visit").inc()
                APP_HEALTH.set(0)
                return render_template('index.html',
                                     error="Database connection failed",
                                     total_visits=0,
                                     last_visit="N/A")

            VISITS_TOTAL.set(data["total"])
            APP_HEALTH.set(1)

            return render_template("index.html", 
                                   total_visits = data["total"],
                                   last_visit = data["last_time"],
                                   error = None)
            
        except Exception as e:
            DB_ERRORS.labels(operation="general").inc()
            APP_HEALTH.set(0)
            return render_template('index.html',
                                 error=str(e),
                                 total_visits=0,
                                 last_visit="N/A")

    @app.route('/health')
    def health():
        from flask import jsonify
        try:
            status = db.check_connection()
            if status:
                health_status = {
                    "status": "healthy",
                    "service": "visitor-app",
                    "database": "connected",
                    "timestamp": time.time()
                }
                APP_HEALTH.set(1)
                return jsonify(health_status), 200
            else:
                raise Exception("Database connection failed")
                
        except Exception as e:
            health_status = {
                "status": "unhealthy",
                "service": "visitor-app",
                "database": "disconnected",
                "error": str(e),
                "timestamp": time.time()
            }
            APP_HEALTH.set(0)
            return jsonify(health_status), 503

    @app.route('/metrics')
    def metrics():
        from prometheus_client import generate_latest
        return generate_latest(), 200, {'Content-Type': 'text/plain'}
