"""
API routers for Naija Oracle
"""

from .simulate import router as simulate_router
from .recommend import router as recommend_router
from .personas import router as personas_router
from .auth import router as auth_router

__all__ = ["simulate_router", "recommend_router", "personas_router", "auth_router"]
