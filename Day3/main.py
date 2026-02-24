# 실습1
# from sqlalchemy import String, Integer, text
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# import asyncio
#
# # 비동기 SQLite (데이터 저장 주소)
# DATABASE_URL = "sqlite+aiosqlite:///:memory:"
#
# # 엔진 생성 (데이터베이스를 이걸 사용하겠다고 알림)
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True
# )
#
#
# # 데이터베이스 세부 내용 세팅
# ## Base 클래스 생성: python -> sql (테이블 내용. 번역기)
# class Base(DeclarativeBase):
#     pass
#
#
# ## 모델 정의: db에 들어갈 테이블 정의
# class User(Base):
#     __tablename__ = "users"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String)
#     email: Mapped[str] = mapped_column(String, unique=True)
#
#
# # 데이터베이스 초기화: 테이블 세팅
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# # 데이터베이스 세션 생성: db (B) <----연결 통로----> 서버 (A)
# AsyncSessionLocal = async_sessionmaker(
#     bind=engine, # 목적지
#     class_=AsyncSession, # 비동기임을 알림
#     expire_on_commit=False,
# )
#
#
# # async def get_db():
# #     async with AsyncSessionLocal() as session:
# #         yield session
#
#
# ########
# # CRUD
# ########
#
# # 1. Create
# async def create_user(name: str, email: str):
#     async with AsyncSessionLocal() as db:  # 데이터베이스 연결
#         new_user = User(name=name, email=email)
#         db.add(new_user)
#         await db.commit()
#         await db.refresh(new_user)
#         return new_user
#
#
# # 2. Read
# ## 전체
# async def get_all_users():
#     async with AsyncSessionLocal() as db:
#         result = await db.execute(text("SELECT * FROM users"))
#         users = result.fetchall()
#         return users
#
#
# ## 특정
# async def get_user_by_email(email: str):
#     async with AsyncSessionLocal() as db:
#         result = await db.execute(
#             text("SELECT * FROM users WHERE email = :email"),
#             {"email": email}
#         )
#         user = result.fetchone()
#         return user
#
#
# # 3. Update
# async def update_user(user_id: int, name: str, email: str):
#     async with AsyncSessionLocal() as db:
#         user = await db.get(User, user_id)
#         if not user:
#             return None
#
#         user.name = name
#         user.email = email
#         await db.commit()
#         await db.refresh(user)
#         return user
#
#
# # 4. Delete
# async def delete_user(user_id: int):
#     async with AsyncSessionLocal() as db:
#         user = await db.get(User, user_id)
#         if not user:
#             return None
#         await db.delete(user)
#         await db.commit()
#         return user_id
#
#
# if __name__ == "__main__":
#
#     async def main():
#         await init_db()
#
#         # 사용자 생성
#         user1 = await create_user(name="이재희", email="clodusky1@gmail.com")
#         user2 = await create_user(name="LLL", email="qmffkqmffk@gmail.com")
#         print(user1, user2)
#
#         # 모든 사용자 조회
#         users = await get_all_users()
#         for user in users:
#             print(user)
#
#         # 특정 사용자
#         user = await get_user_by_email(email="clodusky1@gmail.com")
#         print(user)
#
#         # 사용자 수정
#         updated_user = await update_user(user_id=user2.id, name="LLL2", email="qmffkqmffk2@gmail.com")
#         print(updated_user)
#
#         # 사용자 삭제
#         deleted_id = await delete_user(user_id=user1.id)
#         print(deleted_id)
#
#
#     asyncio.run(main())

# 실습2
# fastapi
# from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel
#
# # 암호화
# from passlib.context import CryptContext
# from jose import jwt
# from datetime import datetime, timedelta
#
# # db
# from database import get_db
# from models import User
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
#
# app = FastAPI()
#
#
#
# ######################
# # utils
# ######################
#
# # Password
# pwd_context = CryptContext(
#     schemes=["argon2"], # 암호화 알고리즘 (bcrypt, argon2)
#     deprecated="auto"
# )
#
# def hash_password(password: str):
#     return pwd_context.hash(password)
#
# def verify_password(plain, hashed):
#     return pwd_context.verify(plain, hashed)
#
#
# # Access Token (JWT 형태)
# ALGORITHM = "HS256"
# SECRET_KEY = "be-oz" # 자물쇠
# ACCESS_TOKEN_EXPIRE_MINS = 30
#
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#
# ######################
# # pydantic
# ######################
# class UserRegister(BaseModel):
#     username: str
#     password: str
#
# class UserLogin(BaseModel):
#     username: str
#     password: str
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
#
# ######################
# # api
# ######################
# @app.post("/register")
# async def register(
#     user: UserRegister,
#     db: AsyncSession = Depends(get_db)
# ):
#     # 유저가 이미 가입했는지 확인하기
#     result = await db.execute(
#         select(User).where(User.username == user.username)
#     )
#     existing_user = result.scalar_one_or_none()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="이미 가입한 사람")
#
#     # 새로운 유저를 db 추가
#     new_user = User(
#         username=user.username,
#         password=hash_password(user.password)
#     )
#     db.add(new_user)
#     await db.commit()
#     return {"message": "회원가입 성공"}
#
#
# @app.post("/login", response_model=Token)
# async def login(
#     user: UserLogin,
#     db: AsyncSession = Depends(get_db)
# ):
#     # 유저가 등록되어 있는지 확인하기
#     result = await db.execute(
#         select(User).where(User.username == user.username)
#     )
#     db_user = result.scalar_one_or_none()
#
#     # 유저가 없거나 비밀번호 오류
#     if not db_user or not verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="아이디나 비밀번호가 잘못됨")
#
#     access_token = create_access_token({"sub": db_user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

# 실습3
# fastapi
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

# 암호화
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# db
from database import get_db
from models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

######################
# utils
######################

# Password
pwd_context = CryptContext(
    schemes=["argon2"],  # 암호화 알고리즘 (bcrypt, argon2)
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# Access Token (JWT 형태)
ALGORITHM = "HS256"
SECRET_KEY = "be-oz"  # 자물쇠
ACCESS_TOKEN_EXPIRE_MINS = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# TODO: 인증 관련
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
):
    """ TODO
    1. 전달된 JWT 토큰을 검증하여 사용자 정보를 가져옴
    2. 토큰이 유효하지 않거나 만료되면 401 반환
    3. DB에서 사용자 존재 여부 확인
    4. 사용자가 없거나 토큰이 유효하지 않다면, 401 Unauthorized 오류를 반환
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 토큰"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        exp = payload.get("exp")

        if username is None:
            raise credential_exception

        if exp is None or (datetime.utcfromtimestamp(exp) < datetime.utcnow()):
            raise credential_exception

    except JWTError:
        raise credential_exception

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credential_exception

    return {
        "id": user.id,
        "username": user.username
    }


######################
# pydantic
######################
class UserRegister(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


######################
# api
######################
@app.post("/register")
async def register(
        user: UserRegister,
        db: AsyncSession = Depends(get_db)
):
    # 유저가 이미 가입했는지 확인하기
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 가입한 사람")

    # 새로운 유저를 db 추가
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(new_user)
    await db.commit()
    return {"message": "회원가입 성공"}


@app.post("/login", response_model=Token)
async def login(
        user: UserLogin,
        db: AsyncSession = Depends(get_db)
):
    # 유저가 등록되어 있는지 확인하기
    result = await db.execute(
        select(User).where(User.username == user.username)
    )
    db_user = result.scalar_one_or_none()

    # 유저가 없거나 비밀번호 오류
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="아이디나 비밀번호가 잘못됨")

    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/profile")
async def profile(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"]
    }