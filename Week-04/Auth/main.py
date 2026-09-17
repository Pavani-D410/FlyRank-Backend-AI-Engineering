from fastapi import FastAPI, HTTPException, Header, Depends, Response
from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from supabase import AuthApiError

from auth import supabase


app = FastAPI(title="FlyRank Auth API")
security = HTTPBearer()

# -------------------------
# Request Model
# -------------------------

class AuthRequest(BaseModel):
    email: str
    password: str


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "message": "FlyRank Auth API is running"
    }


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# -------------------------
# Stage 1: Signup
# -------------------------

@app.post("/auth/signup", status_code=201)
def signup(request: AuthRequest):

    if not request.email or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })

        return {
            "message": "Signup successful",
            "user_id": response.user.id if response.user else None
        }

    except AuthApiError:
        raise HTTPException(
            status_code=400,
            detail="Signup failed"
        )


# -------------------------
# Stage 1: Login
# -------------------------

@app.post("/auth/login")
def login(request: AuthRequest):

    if not request.email or not request.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })

        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token
        }

    except AuthApiError:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )


# -------------------------
# Stage 2: Public Route
# -------------------------

@app.get("/public/info")
def public_info():
    return {
        "message": "Welcome stranger! This info is public."
    }


# -------------------------
# Stage 4: Reusable Auth Dependency
# -------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Access token required"
        )

    try:
        response = supabase.auth.get_user(token)

        user = response.user

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        return user

    except AuthApiError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

# -------------------------
# Stage 4: Protected Profile
# -------------------------

@app.get("/protected/profile")
def protected_profile(user=Depends(get_current_user)):

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }


# -------------------------
# Stage 4: Protected Dashboard
# -------------------------

@app.get("/protected/dashboard")
def protected_dashboard(user=Depends(get_current_user)):

    return {
        "message": "Welcome to your dashboard!",
        "user_id": user.id,
        "email": user.email
    }


# -------------------------
# Stage 4: Logout
# -------------------------

@app.post("/auth/logout", status_code=204)
def logout(
    user=Depends(get_current_user)
):

    try:
        supabase.auth.sign_out()

        return Response(status_code=204)

    except AuthApiError:
        raise HTTPException(
            status_code=401,
            detail="Logout failed"
        )