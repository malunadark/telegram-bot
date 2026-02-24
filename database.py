import asyncpg
from config import DATABASE_URL

pool = None

async def connect():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

async def get_user(telegram_id):
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id=$1",
            telegram_id
        )

async def create_user(telegram_id, username):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id, username)
            VALUES ($1, $2)
        """, telegram_id, username)

async def update_stat(telegram_id, field, value):
    async with pool.acquire() as conn:
        await conn.execute(
            f"UPDATE users SET {field} = {field} + $1 WHERE telegram_id=$2",
            value, telegram_id
        )
