from funcs import *
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class SessionData(BaseModel):
    user_id: int
    session_token: str
    ip_address: str
    device_info: str
    browser_info: str

class CookieData(BaseModel):
    session_token: str
    cookie_value: str

class PreferencesData(BaseModel):
    user_id: int
    language: str
    theme: str
    notifications: bool

class BrowsingData(BaseModel):
    user_id: int
    page_visited: str
    duration_seconds: int

@app.post("/session")
async def create_session(data: SessionData):
    create_user_session(
        user_id=data.user_id,
        session_token=data.session_token,
        ip_address=data.ip_address,
        device_info=data.device_info,
        browser_info=data.browser_info
    )
    return {"message": "Session created successfully"}

@app.post("/cookie")
async def create_cookie(data: CookieData):
    set_user_cookie(data.session_token, data.cookie_value)
    return {"message": "Cookie set successfully"}

@app.post("/preferences")
async def set_preferences(data: PreferencesData):
    set_user_preferences(
        user_id=data.user_id,
        language=data.language,
        theme=data.theme,
        notifications=data.notifications
    )
    return {"message": "Preferences set successfully"}

@app.post("/history")
async def add_history(data: BrowsingData):
    add_browsing_history(
        user_id=data.user_id,
        page_visited=data.page_visited,
        duration_seconds=data.duration_seconds
    )
    return {"message": "Browsing history added successfully"}

@app.get("/preferences/{user_id}")
async def get_preferences(user_id: int):
    preferences = get_user_preferences(user_id)
    if not preferences:
        raise HTTPException(status_code=404, detail="User preferences not found")
    return preferences

@app.get("/history/{user_id}")
async def get_history(user_id: int):
    history = get_browsing_history(user_id)
    if not history:
        raise HTTPException(status_code=404, detail="Browsing history not found")
    return history
