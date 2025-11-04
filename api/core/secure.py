# api/core/secure.py
from fastapi import HTTPException, Header

# ====== API KEY ======
API_KEY = "change_me_to_secure_key"

# Verify api key
def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key