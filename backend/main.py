# import libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
from fastapi.middleware.cors import CORSMiddleware

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017")
db = client["automobile_db"]
users_collection = db["users"]

# Password Hashing
def hash_password(password: str) -> str:
    print("password:", password)
    hashed_pwd =  pbkdf2_sha256.hash(password)
    print("hashed_password:", hash_password)
    return hashed_pwd

def verify_password(plain_passwd: str, hashed_pwd: str) -> bool:
    is_verified = pbkdf2_sha256.verify(plain_passwd, hashed_pwd)
    return is_verified

# FastAPI App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a specific domain for better security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class UserRegisterSchema(BaseModel):
    username: str
    password: str
    fullname: str
    city: str
    email: EmailStr
    phone: int

class UserLoginSchema(BaseModel):
    username: str
    password: str

@app.get("/")
async def get_root():
    return "Welcome to FastAPI backend app, it is running..!!!"

@app.post("/register")
async def register_user(user: UserRegisterSchema):
    user_exists = users_collection.find_one({"user": user.username})
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    user_data = {
        "username": user.username,
        "password": hash_password(user.password),
        "fullname": user.fullname,
        "city": user.city,
        "email": user.email,
        "phone": user.phone
    }
    users_collection.insert_one(user_data)

    return {"status":True,"message": "User registered successfully"}

@app.post("/login")
async def login_user(user: UserLoginSchema):
    db_user = users_collection.find_one({"username": user.username})

    if not db_user:
        raise HTTPException(status_code=401, detail="User not available in database")
    
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"status":True,"message": "Login successful"}