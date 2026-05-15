"""
Router for Authentication
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from app.services.supabase_client import SupabaseClient

router = APIRouter()
security = HTTPBearer()

# Dependency injection
def get_supabase_client() -> SupabaseClient:
    return SupabaseClient()

@router.post("/auth/login")
async def login(
    user_data: Dict[str, Any],
    supabase: SupabaseClient = Depends(get_supabase_client)
):
    """
    Authenticate user and create session
    
    - **user_data**: User authentication data
    """
    try:
        # In real implementation, this would use Supabase Auth
        # For now, create a simple session
        session_id = await supabase.create_user_session(user_data)
        
        return {
            "session_id": session_id,
            "user_id": user_data.get("user_id", "demo_user"),
            "token": f"demo_token_{session_id}",
            "expires_in": 3600,
            "message": "Authentication successful"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Logout user and invalidate session
    """
    try:
        # In real implementation, this would invalidate the token
        return {
            "message": "Logout successful",
            "token": credentials.credentials
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/auth/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get current authenticated user
    """
    try:
        # In real implementation, this would validate the token and get user info
        token = credentials.credentials
        
        if token.startswith("demo_token_"):
            return {
                "user_id": "demo_user",
                "email": "demo@naijaoracle.com",
                "name": "Demo User",
                "role": "user",
                "verified": True
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/verify")
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verify authentication token
    """
    try:
        token = credentials.credentials
        
        # Simple token validation
        if token.startswith("demo_token_"):
            return {
                "valid": True,
                "user_id": "demo_user",
                "expires_at": "2024-12-31T23:59:59Z"
            }
        else:
            return {
                "valid": False,
                "error": "Invalid token format"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auth/refresh")
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Refresh authentication token
    """
    try:
        old_token = credentials.credentials
        
        if old_token.startswith("demo_token_"):
            new_token = f"demo_token_{uuid.uuid4()}"
            
            return {
                "token": new_token,
                "expires_in": 3600,
                "message": "Token refreshed successfully"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
