from httpx import AsyncClient
from src.application.schemas.auth import AuthSchema
from loguru import logger

class TokenParser:

    async def __call__(self, token: str) -> AuthSchema:
        async with AsyncClient(timeout=30.0) as client:
            headers = {"Authorization": token}
            response = await client.get("http://fusionauth:9011/api/jwt/validate", headers=headers)
            r = response.json()
            logger.info(r["jwt"]["user"])
            return AuthSchema.model_validate(r["jwt"]["user"])