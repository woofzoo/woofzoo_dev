# Root and Health Check API Documentation

This document provides comprehensive curl commands for root and health check endpoints in the WoofZoo API.

## Base URL
Root endpoints are at `/` and health endpoints are at `/health`

## Authentication
These endpoints do not require authentication as they are public endpoints.

## Root and Health Endpoints

### 1. Root Endpoint

#### Get API information
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Welcome to WoofZoo API",
  "version": "1.0.0",
  "description": "A comprehensive pet management system API",
  "docs": "/docs",
  "redoc": "/redoc",
  "openapi": "/openapi.json"
}
```

### 2. Health Check

#### Basic health check
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0"
}
```

#### Detailed health check
```bash
curl -X GET "http://localhost:8000/health/detailed"
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "healthy",
      "response_time": "2.5ms"
    },
    "redis": {
      "status": "healthy",
      "response_time": "1.2ms"
    },
    "storage": {
      "status": "healthy",
      "response_time": "5.1ms"
    }
  },
  "system": {
    "uptime": "86400",
    "memory_usage": "45.2%",
    "cpu_usage": "12.8%"
  }
}
```

### 3. API Documentation

#### Get OpenAPI specification
```bash
curl -X GET "http://localhost:8000/openapi.json"
```

**Response:**
```json
{
  "openapi": "3.0.2",
  "info": {
    "title": "WoofZoo API",
    "description": "A comprehensive pet management system API",
    "version": "1.0.0"
  },
  "paths": {
    "/": {
      "get": {
        "summary": "Root",
        "description": "Get API information"
      }
    },
    "/health": {
      "get": {
        "summary": "Health Check",
        "description": "Check API health status"
      }
    }
  }
}
```

#### Get API documentation (Swagger UI)
```bash
curl -X GET "http://localhost:8000/docs"
```

**Response:**
HTML page with interactive API documentation

#### Get API documentation (ReDoc)
```bash
curl -X GET "http://localhost:8000/redoc"
```

**Response:**
HTML page with alternative API documentation

### 4. API Information

#### Get API version
```bash
curl -X GET "http://localhost:8000/api/version"
```

**Response:**
```json
{
  "version": "1.0.0",
  "build_date": "2024-01-01T12:00:00Z",
  "git_commit": "abc123def456",
  "environment": "development"
}
```

#### Get API status
```bash
curl -X GET "http://localhost:8000/api/status"
```

**Response:**
```json
{
  "status": "operational",
  "maintenance_mode": false,
  "last_maintenance": null,
  "next_maintenance": null,
  "uptime": "99.9%",
  "response_time": "45ms"
}
```

## Health Check Status Codes

### Healthy Status
- **Status**: `healthy`
- **HTTP Code**: `200 OK`
- **Description**: All services are functioning normally

### Unhealthy Status
- **Status**: `unhealthy`
- **HTTP Code**: `503 Service Unavailable`
- **Description**: One or more services are not functioning properly

### Degraded Status
- **Status**: `degraded`
- **HTTP Code**: `200 OK`
- **Description**: Services are functioning but with reduced performance

## Service Health Checks

### Database Health
```json
{
  "database": {
    "status": "healthy",
    "response_time": "2.5ms",
    "connections": 5,
    "max_connections": 20
  }
}
```

### Redis Health
```json
{
  "redis": {
    "status": "healthy",
    "response_time": "1.2ms",
    "memory_usage": "15.3%",
    "connected_clients": 3
  }
}
```

### Storage Health
```json
{
  "storage": {
    "status": "healthy",
    "response_time": "5.1ms",
    "available_space": "85.2%",
    "total_space": "100GB"
  }
}
```

## System Information

### System Metrics
```json
{
  "system": {
    "uptime": "86400",
    "memory_usage": "45.2%",
    "cpu_usage": "12.8%",
    "disk_usage": "67.3%",
    "load_average": [1.2, 1.1, 0.9]
  }
}
```

## Error Responses

### 503 Service Unavailable
```json
{
  "status": "unhealthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": {
      "status": "unhealthy",
      "error": "Connection timeout"
    }
  }
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "error": "Internal server error"
}
```

## Monitoring and Alerts

### Health Check Endpoints for Monitoring
- `/health` - Basic health check for load balancers
- `/health/detailed` - Detailed health check for monitoring systems

### Recommended Monitoring Frequency
- **Basic Health Check**: Every 30 seconds
- **Detailed Health Check**: Every 5 minutes
- **System Metrics**: Every minute

### Alert Thresholds
- **Response Time**: > 1000ms
- **Error Rate**: > 5%
- **Memory Usage**: > 90%
- **CPU Usage**: > 80%
- **Disk Usage**: > 90%

## Usage Examples

### Basic Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

### Detailed Health Check
```bash
curl -X GET "http://localhost:8000/health/detailed"
```

### API Information
```bash
curl -X GET "http://localhost:8000/"
```

### API Version
```bash
curl -X GET "http://localhost:8000/api/version"
```

### API Status
```bash
curl -X GET "http://localhost:8000/api/status"
```

## Integration Examples

### Load Balancer Health Check
```bash
# Configure load balancer to check this endpoint
curl -X GET "http://localhost:8000/health" \
  -H "Accept: application/json"
```

### Monitoring System Integration
```bash
# For monitoring systems like Prometheus, Nagios, etc.
curl -X GET "http://localhost:8000/health/detailed" \
  -H "Accept: application/json" \
  -w "Response Time: %{time_total}s\nHTTP Code: %{http_code}\n"
```

### CI/CD Pipeline Health Check
```bash
# For deployment verification
curl -X GET "http://localhost:8000/health" \
  -H "Accept: application/json" \
  --fail \
  --silent \
  --show-error
```

## Security Notes

- Root and health endpoints are public and do not require authentication
- Health endpoints may expose system information - use with caution in production
- Consider rate limiting for health check endpoints to prevent abuse
- Health check responses should not contain sensitive information
- Use HTTPS in production for all endpoints

## Best Practices

### Health Check Implementation
1. **Fast Response**: Health checks should respond quickly (< 100ms)
2. **Minimal Dependencies**: Avoid external service calls in basic health checks
3. **Graceful Degradation**: Return appropriate status codes for different failure modes
4. **Detailed Logging**: Log health check failures for debugging

### Monitoring Integration
1. **Multiple Endpoints**: Use different endpoints for different monitoring needs
2. **Custom Headers**: Include custom headers for monitoring system identification
3. **Response Validation**: Verify response format and status codes
4. **Alert Configuration**: Set up appropriate alerts based on health check results

### Production Considerations
1. **Caching**: Consider caching health check results for high-traffic systems
2. **Load Balancing**: Use health checks for load balancer configuration
3. **Auto-scaling**: Integrate health checks with auto-scaling policies
4. **Maintenance Windows**: Plan for maintenance mode during updates
