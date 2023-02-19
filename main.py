from fastapi import FastAPI, HTTPException, Depends, Body
from app.database import Session, get_db
from app.models import UserTable
from app.schema import User, UserLogin
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT

app = FastAPI()


def check_user(user: UserLogin, db):
    user_table = (
        db.query(UserTable).filter_by(email=user.email, password=user.password).first()
    )
    if user_table:
        return True
    return False


@app.get("/")
async def home():
    return "Welcome: Circle is a new app that allows users to connect with service providers in their area. Service providers can register and post their business, making it easy for people to find and contact them."


@app.post("/register")
async def register(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserTable).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_table = UserTable(
        email=user.email,
        password=user.password,
        name=user.name,
        is_provider=user.is_provider,
    )
    db.add(user_table)
    db.commit()
    return signJWT(user.email)


@app.post("/login")
async def user_login(user: UserLogin, db: Session = Depends(get_db)):
    if check_user(user, db):
        return signJWT(user.email)
    raise HTTPException(status_code=400, detail="Wrong login details!")


@app.get("/users")
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserTable).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserTable).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.__dict__


@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    user_table = db.query(UserTable).filter_by(id=user_id).first()
    if not user_table:
        raise HTTPException(status_code=404, detail="User not found")
    user_table.email = user.email
    user_table.password = user.password
    user_table.name = user.name
    user_table.is_provider = user.is_provider
    db.commit()
    return user_table.__dict__


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_table = db.query(UserTable).filter_by(id=user_id).first()
    if user_table:
        db.delete(user_table)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        return HTTPException(status_code=400, detail="User not found")
