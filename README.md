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
kubectl apply -f Phase2-QuakeWatch/pod.yaml
kubectl get pods
kubectl logs quakewatch-pod
kubectl port-forward quakewatch-pod 5000:5000
# Test at http://localhost:5000, then Ctrl+C to stop
 ```

2. **Deploy Application with Deployment**
```bash
kubectl apply -f Phase2-QuakeWatch/deployment.yaml
kubectl get deployments
kubectl get pods
```

3. **Expose with Service**
```bash
kubectl apply -f Phase2-QuakeWatch/service.yaml
kubectl get services
minikube service quakewatch-service
```

4. **Configure Auto-scaling**
```bash
minikube addons enable metrics-server
kubectl apply -f Phase2-QuakeWatch/hpa.yaml
kubectl get hpa
```

5. **Add Configuration**
```bash
kubectl apply -f Phase2-QuakeWatch/configmap.yaml
kubectl apply -f Phase2-QuakeWatch/secret.yaml
kubectl get configmaps
kubectl get secrets

# Update deployment with configs
kubectl apply -f Phase2-QuakeWatch/deployment.yaml
```

6. **Setup CronJob**
```bash
kubectl apply -f Phase2-QuakeWatch/cronjob.yaml
kubectl get cronjobs
```


7. **Add Health Probes**
```bash
kubectl apply -f Phase2-QuakeWatch/deployment.yaml
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
# Create Helm chart
helm create quakewatch-chart
cd quakewatch-chart

# Edit values.yaml and templates as needed
# Package the chart
helm package .
```

### Publish to Repository
```bash
# Create repository directory
mkdir helm-repo
cp quakewatch-0.1.0.tgz helm-repo/

# Generate index
cd helm-repo
helm repo index . --url https://mayameis.github.io/QuakeWatch/helm-repo

# Push to GitHub Pages
git add helm-repo/
git commit -m "Add Helm repository"
git push origin main
```


### Install from Repository
```bash
# Add repository
helm repo add my-quakewatch https://mayameis.github.io/QuakeWatch/helm-repo
helm repo update

# Search and install
helm search repo my-quakewatch
helm install my-app my-quakewatch/quakewatch
```

## Version Control with Git

### Branching Strategy
```bash
# Create develop branch
git checkout -b develop

# Create feature branch
git checkout -b feature/add-tests

# Merge feature to develop
git checkout develop
git merge feature/add-tests

# Create hotfix
git checkout -b hotfix/fix-version
```

### Conflict Resolution
```bash
# When conflict occurs
git merge hotfix/fix-version
# Edit conflicted files
git add .
git commit -m "Resolve merge conflict"
```

### Pull Request Workflow
```bash
# Push branch
git push origin develop

# Create PR on GitHub UI
# Review and merge PR
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
# Check GitHub Actions
[View Pipeline Status](https://github.com/MAYAMEIS/QuakeWatch/actions)


### Verification Commands
```bash
# Check Helm repository
curl https://mayameis.github.io/QuakeWatch/helm-repo/index.yaml

# List all branches
git branch -a

# View pipeline logs
# Go to Actions tab in GitHub
```