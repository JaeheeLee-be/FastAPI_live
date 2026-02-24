import asyncio
from database import engine, Base
import models


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(init_models())
        print("데이터베이스 테이블 생성 완료!")
    except Exception as e:
        print(f"에러 발생: {e}")