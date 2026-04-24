import aioboto3
from dataclasses import dataclass




@dataclass(slots=True, kw_only=True)
class GetImg:

    async def __call__(self, name: str) -> str:
        session = aioboto3.Session()
        async with session.client(
            "s3",
            endpoint_url="http://localhost:9000",
            aws_access_key_id="minioadmin",
            aws_secret_access_key="minioadmin",
            region_name="us-east-1",
        ) as s3:

            url = await s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": "cafe",
                    "Key": f"{name}",
                },
                ExpiresIn=3600,
            )

            return url