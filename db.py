import asyncpg
import config

class Database:
    def __init__(self):
        self.pool = None

    async def pre_process(self):
        conn_str = config.get_ConnString()
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                    user=conn_str["user"],
                    password=conn_str["password"],
                    database=conn_str["database"],
                    host=conn_str["host"]
                )
            

    async def add_user(self, user_id: int, username: str, tokens: int):
        async with self.pool.acquire() as connection:
            sql = "INSERT INTO users (user_id, username, tokens) VALUES ($1, $2, $3)"
            await connection.execute(sql, user_id, username, tokens)


