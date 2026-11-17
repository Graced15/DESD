import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient, WorkerConfig


async def save_stock_details(job):
    """Placeholder worker: completes the save_stock_details job without saving data."""
    print("Placeholder save_stock_details job received.")

    # Return process variables here if your BPMN needs them.
    return {}


async def main():
    async with CamundaAsyncClient() as client:
        client.create_job_worker(
            config=WorkerConfig(
                job_type="save_stock_details",
                job_timeout_milliseconds=30000,
            ),
            callback=save_stock_details,
        )

        print("Worker started.")
        print("Listening for save_stock_details jobs...")

        await client.run_workers()


if __name__ == "__main__":
    asyncio.run(main())
