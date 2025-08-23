"""
Hybrid Dependency Injection Demo

This example demonstrates the hybrid approach to dependency injection,
showing both centralized and domain-specific organization.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

# =============================================================================
# APPROACH 1: CENTRALIZED DEPENDENCIES (Good for small to medium apps)
# =============================================================================

# All dependencies in one file: app/dependencies.py
from app.dependencies import (
    get_task_controller,
    get_user_controller,
    get_dashboard_service,
    get_rate_limited_controller
)

# Simple route using centralized dependencies
router_simple = APIRouter(prefix="/simple", tags=["simple"])

@router_simple.get("/tasks")
async def get_tasks_simple(
    controller = Depends(get_task_controller)
):
    """Simple route using centralized dependencies."""
    return await controller.get_all_tasks()


# =============================================================================
# APPROACH 2: DOMAIN-SPECIFIC DEPENDENCIES (Good for large apps)
# =============================================================================

# Domain-specific dependencies
from app.dependencies.domains.task import get_task_controller as get_task_controller_domain
from app.dependencies.domains.user import get_user_controller as get_user_controller_domain

router_domain = APIRouter(prefix="/domain", tags=["domain"])

@router_domain.get("/tasks")
async def get_tasks_domain(
    controller = Depends(get_task_controller_domain)
):
    """Route using domain-specific dependencies."""
    return await controller.get_all_tasks()


# =============================================================================
# APPROACH 3: HYBRID APPROACH (Best of both worlds)
# =============================================================================

# Use centralized for simple cases, domain-specific for complex ones
router_hybrid = APIRouter(prefix="/hybrid", tags=["hybrid"])

@router_hybrid.get("/tasks")
async def get_tasks_hybrid(
    # Simple dependency - use centralized
    controller = Depends(get_task_controller)
):
    """Simple dependency using centralized approach."""
    return await controller.get_all_tasks()


@router_hybrid.get("/users/{user_id}/dashboard")
async def get_user_dashboard_hybrid(
    user_id: int,
    # Complex dependency - use domain-specific
    dashboard_service = Depends(get_dashboard_service)
):
    """Complex dependency using domain-specific approach."""
    return await dashboard_service.get_user_dashboard(user_id)


# =============================================================================
# COMPLEX SCENARIOS DEMONSTRATION
# =============================================================================

# Scenario 1: Service with multiple dependencies
@router_hybrid.post("/users")
async def create_user_complex(
    user_data: dict,
    # This service depends on multiple other services
    user_controller = Depends(get_user_controller)
):
    """
    Complex service dependency.
    
    UserService depends on:
    - UserRepository
    - TaskService
    - NotificationService
    - EmailService
    
    All managed in one place!
    """
    return await user_controller.create_user(user_data)


# Scenario 2: Conditional dependencies
@router_hybrid.get("/tasks/cached")
async def get_tasks_cached(
    # This will be None if caching is disabled
    caching_service = Depends(get_caching_service),
    controller = Depends(get_task_controller)
):
    """
    Conditional dependency example.
    
    CachingService is only created if cache_enabled=True in settings.
    """
    if caching_service:
        # Use cached version
        return await caching_service.get_cached_tasks()
    else:
        # Use direct database query
        return await controller.get_all_tasks()


# Scenario 3: Cross-cutting concerns
@router_hybrid.get("/tasks/rate-limited")
async def get_tasks_rate_limited(
    # This wraps the original controller with rate limiting
    rate_limited_controller = Depends(get_rate_limited_controller)
):
    """
    Cross-cutting concern example.
    
    RateLimitedTaskController wraps TaskController with rate limiting
    without modifying the original controller.
    """
    return await rate_limited_controller.get_all_tasks()


# Scenario 4: Environment-specific dependencies
@router_hybrid.get("/health")
async def health_check(
    # This is only available in production
    monitoring_client = Depends(get_monitoring_client)
):
    """
    Environment-specific dependency example.
    
    MonitoringClient is only created in production environment.
    """
    health_status = {"status": "healthy"}
    
    if monitoring_client:
        # Send metrics to monitoring service
        await monitoring_client.send_health_metric(health_status)
    
    return health_status


# =============================================================================
# TESTING EXAMPLES
# =============================================================================

def test_simple_dependency():
    """Test simple dependency injection."""
    from unittest.mock import Mock
    
    # Mock the dependency
    mock_controller = Mock()
    mock_controller.get_all_tasks.return_value = [{"id": 1, "title": "Test"}]
    
    # Test the endpoint
    with patch('app.dependencies.get_task_controller', return_value=mock_controller):
        result = get_tasks_simple(mock_controller)
        assert result == [{"id": 1, "title": "Test"}]


def test_complex_dependency():
    """Test complex dependency injection."""
    from unittest.mock import Mock, patch
    
    # Mock all dependencies
    mock_user_repo = Mock()
    mock_task_service = Mock()
    mock_notification_service = Mock()
    mock_email_service = Mock()
    
    # Test the endpoint
    with patch.multiple('app.dependencies',
                       get_user_repository=Mock(return_value=mock_user_repo),
                       get_task_service=Mock(return_value=mock_task_service),
                       get_notification_service=Mock(return_value=mock_notification_service),
                       get_email_service=Mock(return_value=mock_email_service)):
        # The dependency injection system handles all the wiring automatically!
        pass


# =============================================================================
# BENEFITS OF HYBRID APPROACH
# =============================================================================

"""
Benefits of the Hybrid Dependency Injection Approach:

1. **Centralized Management**: All dependencies in one place for easy discovery
2. **Clear Organization**: Dependencies grouped by domain and type
3. **Scalability**: Can start with centralized and move to domain-specific as needed
4. **Complex Dependencies**: Easy to handle services with multiple dependencies
5. **Testing**: Simple to mock and test individual components
6. **Cross-cutting Concerns**: Easy to add decorators and wrappers
7. **Conditional Dependencies**: Support for environment-specific services
8. **Maintainability**: Clear separation of concerns and easy refactoring

Example Usage Patterns:

- Small apps: Use centralized dependencies (app/dependencies.py)
- Medium apps: Use centralized with clear organization
- Large apps: Use domain-specific dependencies (app/dependencies/domains/)
- Enterprise apps: Use hybrid approach with both patterns

The key is choosing the right approach for your application size and complexity!
"""
