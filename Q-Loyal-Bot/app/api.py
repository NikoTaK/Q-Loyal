from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import app.database.requests as rq

api_app = FastAPI()

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.get("/api/user/{tg_id}")
async def get_user_info(tg_id: int):
    user = await rq.get_user(tg_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "full_name": user.full_name or user.username or "User",
        "qr_token": user.qr_token
    }