from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os
import httpx

# Load environment variables from .env
load_dotenv()

# Konfigurasi Google OAuth dan API router
router = APIRouter()

# Google OAuth URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Load Google API credentials
GOOGLE_CLIENT_ID = os.getenv("CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CALLBACK_URL = os.getenv("CALLBACK_URL")  # Anda harus memastikan CALLBACK_URL diset dalam .env

# Validasi konfigurasi
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("Google Client ID or Client Secret is missing in environment variables")


@router.get("/login", summary="Login with Google OAuth")
def login_with_google():
    """
    Redirect user to Google's OAuth login page.
    """
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": CALLBACK_URL,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "access_type": "offline",
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return RedirectResponse(auth_url)


@router.get("/callback", summary="Callback for Google OAuth")
async def callback(code: str):
    """
    Handle the callback after Google OAuth login.
    """
    try:
        # Tukar code menjadi token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": CALLBACK_URL,
                    "grant_type": "authorization_code",
                    "code": code,
                },
            )
        token_response.raise_for_status()
        tokens = token_response.json()

        # Ambil informasi pengguna dari Google
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
            )
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "user_info": user_info,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during Google OAuth: {str(e)}")
