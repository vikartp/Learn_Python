# FastAPI App Monitoring Guide

This guide covers how to run the provided FastAPI repository and how to integrate Prometheus and Grafana for monitoring into any FastAPI application.

## 🏃 Running the `Fast-Api-example` Repo

You have two main options to run the application: using Docker or running it locally.

### Option 1: Quick Start with Docker (Recommended)
This is the fastest way, as it spins up the FastAPI backend, PostgreSQL database, and Vue frontend automatically.

1. Ensure you have Docker and Docker Compose installed.
2. Navigate to the root directory of the repo (`c:\Space\workspaces\Learn-Python\Fast-Api-example`).
3. Run the following command:
   ```bash
   docker-compose up -d --build
   ```
4. Access the application:
   - **Frontend**: http://localhost:5173
   - **API Docs (Swagger)**: http://localhost:8002/docs
   - **API Backend**: http://localhost:8002

### Option 2: Local Installation
If you prefer running the backend manually:

1. **Backend Setup**:
   Navigate to the `src` folder, create a virtual environment, and install dependencies:
   ```bash
   cd src
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database Configuration**:
   Ensure you have a local PostgreSQL server running. Create an `.env` file inside `src/` (copy from `src/app/.env-example` if available) and update the `DATABASE_URL`:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   SECRET_KEY=your-secret-key
   ```

3. **Run Migrations**:
   Run Alembic to create the database tables:
   ```bash
   alembic upgrade head
   ```

4. **Start the API**:
   You can use the provided bash script or run `uvicorn` directly:
   ```bash
   ./run.sh
   # OR
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 📊 Integrating Prometheus and Grafana into Any App

Monitoring is crucial for observing app performance, spotting bottlenecks, and alerting on failures. 

- **Prometheus** is a time-series database that *scrapes* (pulls) metrics from your application at defined intervals.
- **Grafana** is a visualization tool that reads the data stored in Prometheus to create beautiful, informative dashboards.

### Step-by-Step Integration for a FastAPI App

#### 1. Instrument the Application
First, your app needs to expose a `/metrics` endpoint that Prometheus can scrape. For FastAPI, we use the `prometheus-fastapi-instrumentator` package.

**Install the library:**
```bash
pip install prometheus-fastapi-instrumentator
```

**Update your `main.py`:**
```python
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Add this after creating your FastAPI app instance
Instrumentator().instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"Hello": "World"}
```
> [!NOTE]
> `instrument(app)` hooks into FastAPI's request lifecycle to track metrics (latency, request counts). `expose(app)` creates the `/metrics` route.

#### 2. Configure Prometheus
Prometheus needs to know *where* to scrape data from. Create a configuration file named `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s # How often to scrape targets

scrape_configs:
  - job_name: 'fastapi-app'
    static_configs:
      - targets: ['host.docker.internal:8000'] # Point this to your FastAPI app's host and port
```

#### 3. Run Prometheus
You can easily spin up Prometheus using Docker, mounting your configuration file:

```bash
docker run -d -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```
*Prometheus will now be available at `http://localhost:9090`.*

#### 4. Run Grafana
Run Grafana using Docker to visualize the metrics:

```bash
docker run -d -p 3000:3000 grafana/grafana
```
*Access Grafana at `http://localhost:3000` (default login is `admin` / `admin`).*

#### 5. Connect and Visualize
1. In Grafana, go to **Connections > Data sources**.
2. Add a new **Prometheus** data source.
3. Set the HTTP URL to your Prometheus instance (e.g., `http://host.docker.internal:9090`).
4. Click **Save & Test**.
5. Go to **Dashboards**, create a new dashboard, and add panels querying Prometheus metrics (like `http_requests_total`).

---

## 🧠 Architecture Mindmap (For Interviews & Revision)

Use this mindmap to clearly explain the flow of telemetry data during an interview.

```mermaid
mindmap
  root((Monitoring Stack))
    Application (FastAPI)
      prometheus-fastapi-instrumentator
      Exposes /metrics endpoint
      Tracks Request Count, Latency, Errors
    Prometheus
      Time-Series Database
      Scrapes data periodically (Pull Model)
      prometheus.yml configures targets
      Stores metrics (e.g., CPU, HTTP requests)
    Grafana
      Data Visualization
      Connects to Prometheus Data Source
      Creates Dashboards & Alerts
      Queries data using PromQL
    Docker (Deployment)
      Containerizes all services
      Simplifies networking between App, Prometheus, Grafana
```

### 🗣️ Interview Talking Points:
- **"Why pull over push?"**: Prometheus pulls metrics from the app. This means if the app crashes, it just fails to scrape, without the app wasting resources trying to push to a dead monitoring server.
- **"What is PromQL?"**: It's the query language used in Grafana to filter and aggregate Prometheus data.
- **"Why both?"**: Prometheus is great at storing time-series data efficiently, but Grafana excels at visualizing it securely with custom alerts.
