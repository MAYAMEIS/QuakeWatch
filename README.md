![Screenshot of QuakeWatch](static/experts-logo.svg)

# QuakeWatch

**QuakeWatch** is a Flask-based web application designed to display real-time and historical earthquake data. It visualizes earthquake statistics with interactive graphs and provides detailed information sourced from the USGS Earthquake API. Built using an object‑oriented design and modular structure, QuakeWatch separates templates, utility functions, and route definitions, making it both scalable and maintainable. The application is also containerized with Docker for easy deployment.

## Features

  - **Real-Time & Historical Data:** Fetches earthquake data from the USGS API.
  - **Interactive Graphs:** Displays earthquake counts over various time periods (e.g., last 30 days, 5-year view) using Matplotlib.
  - **Top Earthquake Events:** Shows the top 5 worldwide earthquakes (last 30 days) by magnitude.
  - **Recent Earthquake Details:** Highlights the most recent earthquake event.
  - **RESTful Endpoints:** Provides endpoints for health checks, status, connectivity tests, and raw data.
  - **Clean UI:** Built with Bootstrap 5, featuring a professional navigation bar with a logo.
  - **Dockerized:** Easily containerized for streamlined deployment.

## Project Structure

```
QuakeWatch/
├── app.py                  # Application factory and entry point
├── dashboard.py            # Blueprint & route definitions using OOP style
├── utils.py                # Helper functions and custom Jinja2 filters
├── requirements.txt        # Python dependencies
├── static/
│   └── experts-logo.svg    # Logo file used in the UI
└── templates/              # Jinja2 HTML templates
    ├── base.html           # Base template with common layout and navigation
    ├── main_page.html      # Home page content
    └── graph_dashboard.html# Dashboard view with graphs and earthquake details
```

## Installation

### Locally


# ==========================================
# Phase 1: Docker Foundation
# ==========================================




1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/QuakeWatch.git
   cd QuakeWatch
   ```

   2. **Set Up a Virtual Environment (optional but recommended):**

      ```bash
      python -m venv venv
      source venv/bin/activate   # On Windows: venv\Scripts\activate
      ```

   3. **Install Dependencies:**

      ```bash
      pip install -r requirements.txt
      ```

## Running the Application Locally

1. **Start the Flask Application:**

   ```bash
   python app.py
   ```

   2. **Access the Application:**

      Open your browser and visit [http://127.0.0.1:5000](http://127.0.0.1:5000) to view the dashboard.


## Custom Jinja2 Filter

The project includes a custom filter `timestamp_to_str` that converts epoch timestamps to human-readable strings. This filter is registered during application initialization and is used in the templates to format earthquake event times.

## Known Issues

  - **SSL Warning:** You might see a warning regarding LibreSSL when using urllib3. This is informational and does not affect the functionality of the application.
  - **Matplotlib Backend:** The application forces Matplotlib to use the `Agg` backend for headless rendering. Ensure this setting is applied before any Matplotlib imports to avoid GUI-related errors.

## Clone & Setup
```bash
git clone https://github.com/EduardUsatchev/QuakeWatch.git
cd QuakeWatch
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Locally
```bash
python app.py
# Access: http://localhost:5000
```

## Build & Run Manually
```bash
docker build -t maya123/quakewatch:latest .
docker run -d -p 5000:5000 maya123/quakewatch:latest
```

## Docker Compose
```bash
docker-compose up --build -d
```

## Check Status
```bash
docker-compose ps
```

## Stop & Remove
```bash
docker-compose down
```

## Push to Docker Hub
```bash
docker login
docker push maya123/quakewatch:latest
```

## Pull from Docker Hub
```bash
docker pull maya123/quakewatch:latest
docker run -d -p 5000:5000 maya123/quakewatch:latest
```

## Access the App
```
http://localhost:5000kubectl get pods -n kube-system -o wide | findstr kubelet

```
   
# ==========================================
# Phase 2: Kubernetes Orchestration
# ==========================================

### Prerequisites
```bash
minikube start
kubectl get nodes
docker images
 ```

1. **Deploy Initial Pod**

```bash
kubectl apply -f pod.yaml
kubectl get pods
kubectl logs quakewatch-pod
kubectl port-forward quakewatch-pod 5000:5000
# Test at http://localhost:5000, then Ctrl+C to stop
 ```

2. **Deploy Application with Deployment**
```bash
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl get pods
```

3. **Expose with Service**
```bash
bashkubectl apply -f service.yaml
kubectl get services
minikube service quakewatch-service
```

4. **Configure Auto-scaling**
```bash
minikube addons enable metrics-server
kubectl apply -f hpa.yaml
kubectl get hpa
```

5. **Add Configuration**
```bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl get configmaps
kubectl get secrets

# Update deployment with configs
kubectl apply -f Phase2-QuakeWatch/deployment.yaml
```

6. **Setup CronJob**
```bash
kubectl apply -f cronjob.yaml
kubectl get cronjobs
```


7. **Add Health Probes**
```bash
kubectl apply -f deployment.yaml
kubectl get pods -w
```


### Verification Commands
```bash
kubectl get all
kubectl logs -l job-name=quakewatch-cronjob --tail=10
```

# ==========================================
# Phase 3: Automation - Package Management, Version Control & CI/CD
# ==========================================

## Package Management with Helm

### Create and Package Helm Chart
```bash
helm create quakewatch-chart
cd quakewatch-chart


helm package .
```

### Publish to Repository
```bash
mkdir helm-repo
cp quakewatch-0.1.0.tgz helm-repo/

cd helm-repo
helm repo index . --url https://mayameis.github.io/QuakeWatch/helm-repo

git add helm-repo/
git commit -m "Add Helm repository"
git push origin main
```


### Install from Repository
```bash
helm repo add my-quakewatch https://mayameis.github.io/QuakeWatch/helm-repo
helm repo update

helm search repo my-quakewatch
helm install my-app my-quakewatch/quakewatch
```

## Version Control with Git

### Branching Strategy
```bash
git checkout -b develop

git checkout -b feature/add-tests

git checkout develop
git merge feature/add-tests

git checkout -b hotfix/fix-version
```

### Conflict Resolution
```bash
git merge hotfix/fix-version
git add .
git commit -m "Resolve merge conflict"
```

### Pull Request Workflow
```bash
git push origin develop
```

## CI/CD Pipeline with GitHub Actions


### Pipeline Configuration (.github/workflows/ci-cd.yml)
```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

**Pipeline Stages**
- **Test** – Runs pylint on Python 3.8, 3.9, 3.10  
- **Build** – Builds Docker image  
- **Deploy** – Deployment placeholder  


### View Pipeline Status
Check GitHub Actions
[View Pipeline Status](https://github.com/MAYAMEIS/QuakeWatch/actions)


### Verification Commands
```bash
curl https://mayameis.github.io/QuakeWatch/helm-repo/index.yaml

git branch -a
```



# ==========================================
# Phase 4: GitOps & Monitoring
# ==========================================

## GitOps with ArgoCD

### ArgoCD Installation
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get pods -n argocd
```

### Access ArgoCD UI
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get password:
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Login: admin / <password>
# Visit: https://localhost:8080
```

### Configure Application
```bash
kubectl apply -f argocd-application.yaml
kubectl get application quakewatch -n argocd
```

**Expected Status:**
- Sync Status: `Synced` ✅
- Health Status: `Progressing` (normal - see troubleshooting)

### Auto-Sync Configuration
Auto-sync is enabled with:
- **Prune:** Auto-delete resources removed from Git
- **Self-Heal:** Auto-sync on manual cluster changes

Any push to GitHub automatically updates the cluster!

---

## Monitoring with Prometheus & Grafana

### Installation
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace

kubectl get pods -n monitoring
```

### ServiceMonitor Configuration
```bash
kubectl apply -f k8s-manifests/servicemonitor.yaml
kubectl get servicemonitor quakewatch-metrics -n default
```

**Verify Prometheus is scraping:**
```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Visit: http://localhost:9090/targets
# Search: "quakewatch" - Status should be UP
```

### PrometheusRule (Alerts)
```bash
kubectl apply -f k8s-manifests/prometheus-rules.yaml
kubectl get prometheusrule quakewatch-alerts -n monitoring
```

**4 Alert Rules Configured:**
1. **QuakewatchTestAlert** - Test alert (always firing)
2. **HighPodRestartCount** - Warns when restarts > 3
3. **HighCPUUsage** - Critical when CPU > 80%
4. **HighErrorRate** - Critical when restarts >= 5

**View Alerts:**
```bash
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Visit: http://localhost:9090/alerts
```

### Grafana Dashboard
```bash
# Get Grafana password:
kubectl get secret -n monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 -d

# Port forward:
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Login: admin / <password>
# Visit: http://localhost:3000
```

**Dashboard: "QuakeWatch Monitoring"**
- 8 panels with comprehensive metrics
- CPU/Memory usage
- Request rates and latency
- Pod health and restarts
- Active alerts

---

## Verification Commands

### Check ArgoCD Status
```bash
kubectl get application quakewatch -n argocd
kubectl get pods -n default | findstr quakewatch
```

### Check Monitoring Stack
```bash
kubectl get pods -n monitoring
kubectl get servicemonitor -n default
kubectl get prometheusrule -n monitoring | findstr quakewatch
```

### Test Application
```bash
kubectl port-forward svc/quakewatch-service 5000:80
# Visit: http://localhost:5000
```

---

## Troubleshooting

### ArgoCD Health: Progressing
**This is normal!** Status shows `Progressing` due to:
- LoadBalancer service in `<pending>` (Minikube limitation)
- CronJob creating pods every 5 minutes
- HPA dynamic scaling

✅ All resources are `Synced`  
✅ All pods are `Running`  
✅ Application fully functional

### Prometheus Targets Down
```bash
# Check ServiceMonitor
kubectl describe servicemonitor quakewatch-metrics -n default

# Verify /metrics endpoint
kubectl port-forward svc/quakewatch-service 5000:80
# Visit: http://localhost:5000/metrics
```

### Grafana No Data
```bash
# Test Prometheus data source in Grafana
# Configuration → Data Sources → Prometheus → Test

# Verify metrics in Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090
# Query: kube_pod_info{namespace="default"}
```

---
