from config import *
from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url=f"postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()
