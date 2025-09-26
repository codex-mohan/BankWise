from fastapi import Header, HTTPException
import os


# API Token Authentication
def verify_api_token(x_api_token: str = Header(...)):
    """Verify the API token from the request header"""
    expected_token = os.getenv("API_TOKEN")
    print("Expected token:", expected_token)
    if not expected_token:
        raise HTTPException(status_code=500, detail="API token not configured")
    if x_api_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid or missing API token")
    return True
