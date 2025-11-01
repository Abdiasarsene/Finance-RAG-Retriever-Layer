from fastapi import HTTPException, Header

API_KEY = "change_me_to_secure_key"

def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key