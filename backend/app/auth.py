import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.config import settings

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    token = credentials.credentials

    # Call supabase auth.getUser
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{settings.SUPABASE_URL}/auth/v1/user",
            headers={
                "Authorization": f"Bearer {token}",
                "apikey": settings.SUPABASE_ANON_KEY,
            }
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return resp.json()
