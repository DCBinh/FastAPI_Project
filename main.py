from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import User

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Tạo user
@app.post("/users/")
async def create_user(name: str, email: str):
    user = await User.create(name=name, email=email)
    return user

# Lấy danh sách user
@app.get("/users/")
async def get_users():
    users = await User.all()
    return users

# Lấy user theo ID
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    return user

# Cập nhật user
@app.put("/users/{user_id}")
async def update_user(user_id: int, name: str, email: str):
    user = await User.get_or_none(id=user_id)
    if user:
        user.name = name
        user.email = email
        await user.save()
        return user
    return {"error": "User not found"}

# Xóa user
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        return {"message": "User deleted"}
    return {"error": "User not found"}

# Kết nối MySQL
register_tortoise(
    app,
    db_url="mysql://root:123456@localhost/fastapi_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
