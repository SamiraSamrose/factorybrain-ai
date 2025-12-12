from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
from .config import settings
from .api.routes import machines, alerts, analytics, maintenance, procurement
from .api.dependencies import get_current_active_user
from .utils.auth import create_access_token, get_password_hash, verify_password
from pydantic import BaseModel
import numpy as np

app = FastAPI(
title=settings.PROJECT_NAME,
version=settings.VERSION,
description="Autonomous Process Optimization for Smart Manufacturing Plants"
)
app.add_middleware(
CORSMiddleware,
allow_origins=[""],
allow_credentials=True,
allow_methods=[""],
allow_headers=["*"],
)
app.include_router(machines.router, prefix=settings.API_V1_STR)
app.include_router(alerts.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(maintenance.router, prefix=settings.API_V1_STR)
app.include_router(procurement.router, prefix=settings.API_V1_STR)
class LoginRequest(BaseModel):
username: str
password: str
class TokenResponse(BaseModel):
access_token: str
token_type: str
user: dict
@app.get("/")
async def root():
return {
"message": "FactoryBrain AI API",
"version": settings.VERSION,
"status": "operational",
"timestamp": datetime.utcnow().isoformat()
}
@app.get("/health")
async def health_check():
return {
"status": "healthy",
"timestamp": datetime.utcnow().isoformat(),
"services": {
"api": "operational",
"database": "operational",
"cerebras": "operational",
"raindrop": "operational",
"iot_broker": "operational"
}
}
@app.post("/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
users_db = {
"admin": {"password": get_password_hash("admin123"), "role": "admin", "full_name": "Administrator"},
"supervisor": {"password": get_password_hash("super123"), "role": "supervisor", "full_name": "Supervisor"},
"operator": {"password": get_password_hash("oper123"), "role": "operator", "full_name": "Operator"}
}
user = users_db.get(credentials.username)

if not user or not verify_password(credentials.password, user["password"]):
    raise HTTPException(
        status_code=401,
        detail="Incorrect username or password"
    )

access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
access_token = create_access_token(
    data={"sub": credentials.username, "role": user["role"]},
    expires_delta=access_token_expires
)

return TokenResponse(
    access_token=access_token,
    token_type="bearer",
    user={
        "username": credentials.username,
        "role": user["role"],
        "full_name": user["full_name"]
    }
)
@app.get("/auth/me")
async def get_current_user_info(current_user = Depends(get_current_active_user)):
return {
"username": current_user.username,
"role": current_user.role
}
if name == "main":
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)