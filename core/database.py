import aiosqlite
from config.settings import DATABASE_PATH


class Database:
    def __init__(self):
        self.path = str(DATABASE_PATH)
        self.conn = None

    async def connect(self):
        if self.conn:
            return

        self.conn = await aiosqlite.connect(self.path)
        await self._create_tables()

    async def _create_tables(self):
        await self.conn.execute("""
        CREATE TABLE IF NOT EXISTS welcome_settings (
            chat_id INTEGER PRIMARY KEY,
            enabled INTEGER DEFAULT 1,
            custom_message TEXT
        )
        """)
        await self.conn.execute("""
        CREATE TABLE IF NOT EXISTS feature_settings (
            chat_id INTEGER,
            feature TEXT,
            enabled INTEGER DEFAULT 1,
            PRIMARY KEY (chat_id, feature)
        )
        """)
        await self.conn.commit()

    async def fetchone(self, query, params=()):
        async with self.conn.execute(query, params) as cursor:
            return await cursor.fetchone()

    async def execute(self, query, params=()):
        await self.conn.execute(query, params)
        await self.conn.commit()


# 🔹 SINGLE shared instance
db = Database()