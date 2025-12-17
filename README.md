# Visit Counter Web Application with Monitoring

![media/preview.png](media/preview.png)

## Functionality 

- With every GET-request, a new timestamp is added to the database
- Displays the total number of visits
- Uses PostgreSQL for data storage
- Data persists between restarts
- Built-in monitoring with Prometheus metrics
- Health check endpoints (`/health`)
- Prometheus metrics endpoint (`/metrics`)
- Grafana dashboard for visualization

## Stack

- Python Flask application
- PostgreSQL database
- Docker
- Docker Compose
- Prometheus for metrics collection
- Grafana for metrics visualization

## Quick Start
```bash
git clone https://github.com/L0puh/visitcounter_container 
cd visit-counter
docker-compose up -d
```

## API Endpoints

| Endpoint | Method | Description | Example Response |
|----------|--------|-------------|------------------|
| **`/`** | GET | Main page with visit counter and UI | HTML page showing total visits |
| **`/health`** | GET | Application and database health status | `{"status": "healthy", "database": "connected"}` |
| **`/metrics`** | GET | Prometheus metrics (for monitoring) | Prometheus-formatted metrics data |

## Quick Access Commands

```bash
curl http://localhost:8000/              # Main page
curl http://localhost:8000/health        # Health check
curl http://localhost:8000/metrics       # Prometheus metrics
curl http://localhost:9090               # Prometheus UI
curl http://localhost:3000/api/health    # Grafana health check
