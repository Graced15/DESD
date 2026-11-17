
import asyncio
from camunda_orchestration_sdk import (
    CamundaAsyncClient,
    WorkerConfig,
)

async def validate_stock(job):
    print("Stock validation job received!")

    return {
        "validInfo": True
    }

async def main():
    async with CamundaAsyncClient() as client:

        client.create_job_worker(
            config=WorkerConfig(
                job_type="validate_stock",
                job_timeout_milliseconds=30000,
            ),
            callback=validate_stock,
        )

        print("Worker started!")
        print("Listening for validate_stock jobs...")

        await client.run_workers()

if __name__ == "__main__":
    asyncio.run(main())
