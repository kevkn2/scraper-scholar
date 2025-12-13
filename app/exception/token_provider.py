from fastapi import HTTPException


class FailedToGetTokenException:
    raise HTTPException(status_code=500, detail="Failed to get token from provider")
