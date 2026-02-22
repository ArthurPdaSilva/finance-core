from fastapi import HTTPException


def check_api_key(key: str):
    from config.secrets import Secrets

    if key != Secrets.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: Invalid API key provided.",
        )
