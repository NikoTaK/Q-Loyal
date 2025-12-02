# app/routes.py
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.supabase import supabase

router = APIRouter()

@router.get("/me")
async def me(user = Depends(get_current_user)):
    user_id = user["id"]

    # fetch from your users table
    db_user = (
        supabase.table("users")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )

    return {
        "auth_user": user,
        "db_user": db_user.data
    }


@router.post("/user/init")
async def init_user(user = Depends(get_current_user)):
    user_id = user["id"]
    email = user["email"]

    # check if exists
    existing = (
        supabase.table("users")
        .select("id")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )

    # maybe_single() returns None for no rows
    if existing is None or existing.data is None:
        # insert new row
        supabase.table("users").insert({
            "id": user_id,
            "email": email,
            "role": "customer"
        }).execute()

        return {"status": "created"}

    return {"status": "already_exists"}


