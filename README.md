# FastAPI, PostgreSQL, and WordPress on Kubernetes

This project contains a minimal FastAPI application that stores data in PostgreSQL and runs alongside a WordPress site. All components are containerized and intended to run on Kubernetes.

## FastAPI Application

The FastAPI app exposes two endpoints:

- `GET /items`: returns all items stored in PostgreSQL.
- `POST /items/{name}`: creates a new item with the given name.

The app uses `asyncpg` to connect to PostgreSQL. Database connection parameters are provided via environment variables.

### Building the FastAPI image

```bash
docker build -t fastapi-app:latest ./fastapi_app
```

### Running locally with Docker Compose (optional)

You can run the services locally using Docker Compose:

```yaml
version: '3'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
  fastapi:
    build: ./fastapi_app
    environment:
      POSTGRES_HOST: db
      POSTGRES_DB: appdb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "8000:8000"
```

Save the snippet above as `docker-compose.yml` and run `docker-compose up` to test locally.

## Kubernetes Deployment

Kubernetes manifests are available in the `k8s/` directory:

- `postgres.yaml` – PostgreSQL Deployment and Service
- `fastapi.yaml` – FastAPI Deployment and Service
- `wordpress.yaml` – WordPress and MySQL Deployments and Services

Apply them with `kubectl`:

```bash
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/fastapi.yaml
kubectl apply -f k8s/wordpress.yaml
```

Make sure your FastAPI image is accessible to the cluster (e.g. push it to a registry or use local cluster loading methods).

After the resources are created, you can access FastAPI via the `fastapi` service and WordPress via the `wordpress` service within the cluster.
