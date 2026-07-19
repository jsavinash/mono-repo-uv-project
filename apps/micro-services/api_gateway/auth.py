from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBasic()


@router.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security)) -> dict[str, str]:
    if credentials.username != "demo" or credentials.password != "starterkit":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )

    return {"message": "authenticated", "user": credentials.username}
