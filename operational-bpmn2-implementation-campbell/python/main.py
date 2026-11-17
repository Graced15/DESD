import asyncio

from camunda_orchestration_sdk import CamundaAsyncClient
from workers import register_workers


async def main() -> None:
    async with CamundaAsyncClient() as client:
        register_workers(client)

        print("Worker started. Waiting for Camunda jobs...")
        await client.run_workers()


if __name__ == "__main__":
    asyncio.run(main())