from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import UserSignup, UserLogin, Token, UserProfile
from app.services.user_service import user_service
from app.core.security import create_access_token, decode_access_token
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

class UserUpdate(BaseModel):
    name: str
    age: int
    investment_style: str
    investment_goal: str
    budget: int
    experience: str

@router.post("/signup", response_model=UserProfile)
async def signup(user: UserSignup):
    try:
        new_user = user_service.create_user(user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"회원가입 실패: {str(e)}")

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    user = user_service.authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자 ID 또는 비밀번호가 올바르지 않습니다."
        )
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user['username']})
    
    # Return token and user profile
    user_profile = UserProfile(
        username=user['username'],
        name=user['name'],
        age=user['age'],
        investment_style=user['investment_style'],
        investment_goal=user['investment_goal'],
        budget=user['budget'],
        experience=user['experience'],
        created_at=user.get('created_at')
    )
    
    return Token(access_token=access_token, user=user_profile)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@router.get("/profile", response_model=UserProfile)
async def get_profile(user: dict = Depends(get_current_user)):
    return UserProfile(
        username=user['username'],
        name=user['name'],
        age=user['age'],
        investment_style=user['investment_style'],
        investment_goal=user['investment_goal'],
        budget=user['budget'],
        experience=user['experience'],
        created_at=user.get('created_at')
    )

@router.put("/profile", response_model=UserProfile)
async def update_profile(
    update_data: UserUpdate,
    user: dict = Depends(get_current_user)
):
    try:
        updated_user = user_service.update_user(user['username'], update_data)
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"프로필 업데이트 실패: {str(e)}")
