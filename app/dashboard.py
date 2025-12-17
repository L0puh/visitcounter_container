
from prometheus_client import Counter, Histogram, Gauge
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP Request latency',
    ['method', 'endpoint']
)

DB_ERRORS = Counter(
    'database_errors_total',
    'Total database errors',
    ['operation']
)

VISITS_TOTAL = Gauge(
    'visits_total',
    'Total number of visits'
)

APP_HEALTH = Gauge(
    'app_health',
    'Application health status (1=healthy, 0=unhealthy)'
)

