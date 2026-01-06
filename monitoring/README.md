# Monitoring Setup

This directory contains configuration files for Prometheus and Grafana monitoring.

## Structure

```
monitoring/
├── prometheus/
│   └── prometheus.yml          # Prometheus configuration
├── grafana/
│   ├── provisioning/
│   │   ├── datasources/        # Auto-configure Prometheus datasource
│   │   └── dashboards/          # Auto-load dashboards
│   └── dashboards/              # Custom Grafana dashboards (JSON files)
└── README.md
```

## Usage

1. Start all services with docker-compose:
   ```bash
   docker-compose up -d
   ```

2. Access services:
   - **Grafana**: http://localhost:3001 (admin/admin)
   - **Prometheus**: http://localhost:9090
   - **Backend API**: http://localhost:8000
   - **Frontend**: http://localhost

## Adding Metrics to FastAPI

To expose metrics from your FastAPI backend, you can use `prometheus-fastapi-instrumentator`:

```python
from prometheus_fastapi_instrumentator import Instrumentator

# In app/main.py
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)
```

Then add to `requirements.txt`:
```
prometheus-fastapi-instrumentator==6.1.0
```

## Custom Dashboards

Place Grafana dashboard JSON files in `monitoring/grafana/dashboards/` and they will be automatically loaded.

