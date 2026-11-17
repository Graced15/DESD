import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient, WorkerConfig


async def handle_job(job):
    """Placeholder worker: completes the job without performing business logic."""
    print(f"Placeholder product_unavailable job received.")
    return {}


async def main():
    async with CamundaAsyncClient() as client:
        client.create_job_worker(
            config=WorkerConfig(
                job_type="product_unavailable",
                job_timeout_milliseconds=30000,
            ),
            callback=handle_job,
        )

        print("Worker started.")
        print("Listening for product_unavailable jobs...")

        await client.run_workers()


if __name__ == "__main__":
    asyncio.run(main())
