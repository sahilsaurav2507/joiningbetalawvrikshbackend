"""
API routes for LawVriksh Backend API.
"""

from .auth import router as auth_router
from .user import router as user_router

# Import other routers if they exist
try:
    from .creator import router as creator_router
except ImportError:
    creator_router = None

try:
    from .feedback import router as feedback_router
except ImportError:
    feedback_router = None

try:
    from .admin import router as admin_router
except ImportError:
    admin_router = None

__all__ = [
    "auth_router",
    "user_router", 
    "creator_router",
    "feedback_router",
    "admin_router"
] 