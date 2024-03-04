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
            

    async def add_user(self, user_id: int, username: str, tokens: int, ref_id: int = None):
        async with self.pool.acquire() as connection:
            sql = str()
            if ref_id:
                sql = "INSERT INTO users (id, username, tokens, referral) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING"
                return await connection.execute(sql, user_id, username, tokens, ref_id)
            else:
                sql = "INSERT INTO users (id, username, tokens) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING"
                await connection.execute(sql, user_id, username, tokens)

    async def get_username_by_id(self, user_id: int):
        async with self.pool.acquire() as connection:
            sql = "SELECT username FROM users WHERE id = $1"
            return await connection.fetchrow(sql, user_id)
        
    async def get_user_referrer_id(self, user_id: int) -> int:
        async with self.pool.acquire() as connection:
            sql = "SELECT u2.id FROM users u1 JOIN users u2 ON u1.referral = u2.id WHERE u1.id = $1"
            return await connection.fetchval(sql, user_id)

    async def add_tokens(self, user_id: int, tokens: int):
        async with self.pool.acquire() as connection:
            try:
                async with connection.transaction():
                    sql1 = "UPDATE users SET tokens = tokens + $1 WHERE id = $2"
                    sql2 = "UPDATE users SET role = 'user' WHERE id = $1 AND role = 'guest'"
                    await connection.execute(sql1, tokens, user_id)
                    await connection.execute(sql2, user_id)
            except:
                pass

    async def add_order(self, user_id: int, label: str, amount: int) -> int:
        async with self.pool.acquire() as connection:
            sql = "INSERT INTO orders (user_id, label, amount) VALUES ($1, $2, $3) RETURNING id"
            return await connection.fetchval(sql, user_id, label, amount)

    async def confirm_order(self, order_id: int):
        async with self.pool.acquire() as connection:
            sql = "UPDATE orders SET confirmed = True WHERE id = $1"
            await connection.execute(sql, order_id)

    async def get_balance(self, user_id: int) -> int:
        async with self.pool.acquire() as connection:
            sql = "SELECT tokens FROM users WHERE id = $1"
            return await connection.fetchval(sql, user_id)
        
    async def pay_for_gen(self, user_id: int, tokens: int):
        async with self.pool.acquire() as connection:
            sql = "UPDATE users SET tokens = tokens - $2 WHERE id = $1"
            await connection.execute(sql, user_id, tokens)

    async def get_free_token_used(self, user_id:int) -> int:
        async with self.pool.acquire() as connection:
            sql = "SELECT free_token_used FROM users WHERE id = $1"
            return await connection.fetchval(sql, user_id)
        
    async def set_free_token_used(self, user_id:int, free_token_used: bool):
        async with self.pool.acquire() as connection:
            sql = "UPDATE users SET free_token_used = $2 WHERE id = $1"
            await connection.execute(sql, user_id, free_token_used)


