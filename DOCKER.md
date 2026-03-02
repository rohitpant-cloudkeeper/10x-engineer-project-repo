# Docker Setup Guide

This guide explains how to run the PromptLab application using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

### Development Mode (with hot reload)

Run both frontend and backend in development mode:

```bash
docker-compose up
```

This will start:
- Backend API at http://localhost:8000
- Frontend at http://localhost:5173

### Production Mode

Run both services in production mode:

```bash
docker-compose --profile production up
```

This will start:
- Backend API at http://localhost:8001 (4 workers)
- Frontend at http://localhost:3000 (Nginx)

## Individual Services

### Backend Only

Development:
```bash
docker-compose up backend
```

Production:
```bash
docker-compose --profile production up backend-prod
```

### Frontend Only

Development:
```bash
cd frontend
docker-compose up frontend-dev
```

Production:
```bash
cd frontend
docker-compose --profile production up frontend-prod
```

## Useful Commands

### Build images
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop services
```bash
# Stop all
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Run tests in container
```bash
# Backend tests
docker-compose exec backend pytest tests/ -v

# With coverage
docker-compose exec backend pytest tests/ --cov=app --cov-report=term-missing
```

### Access container shell
```bash
# Backend
docker-compose exec backend sh

# Frontend
docker-compose exec frontend sh
```

## Environment Variables

### Backend
- `PYTHONUNBUFFERED=1` - Disable Python output buffering

### Frontend
- `NODE_ENV` - Set to 'development' or 'production'
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## Port Mapping

| Service | Mode | Container Port | Host Port |
|---------|------|----------------|-----------|
| Backend | Dev | 8000 | 8000 |
| Backend | Prod | 8000 | 8001 |
| Frontend | Dev | 5173 | 5173 |
| Frontend | Prod | 80 | 3000 |

## Health Checks

All services include health checks:

- Backend: `GET /health`
- Frontend: `GET /health` (Nginx)

Check service health:
```bash
docker-compose ps
```

## Troubleshooting

### Port already in use
If ports are already in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "8080:8000"  # Change 8080 to any available port
```

### Frontend can't connect to backend
Ensure the `VITE_API_URL` environment variable points to the correct backend URL.

### Hot reload not working
Make sure volumes are properly mounted in `docker-compose.yml`.

### Build fails
Clear Docker cache and rebuild:
```bash
docker-compose build --no-cache
```

## Production Deployment

For production deployment:

1. Set appropriate environment variables
2. Use production profile: `docker-compose --profile production up -d`
3. Configure reverse proxy (Nginx/Traefik) for SSL/TLS
4. Set up proper logging and monitoring
5. Configure backup strategy for data persistence

## Network

All services run on the `promptlab-network` bridge network, allowing inter-service communication.

## Security Notes

- Backend runs as non-root user (appuser)
- Frontend uses Alpine-based images for smaller attack surface
- Security headers configured in Nginx
- No sensitive data in images (use environment variables)
