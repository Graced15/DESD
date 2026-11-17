import json
from datetime import date
from pathlib import Path

from camunda_orchestration_sdk import (
    CamundaAsyncClient,
    ConnectedJobContext,
    JobError,
    WorkerConfig,
)

# A simple JSON file stands in for the "Product inventory database".
STORE_FILE = Path(__file__).parent / "stock_store.json"


def parse_date(value: object) -> date | None:
    # Form dates arrive as text like "2026-11-16".
    try:
        return date.fromisoformat(str(value)[:10]) if value else None
    except ValueError:
        return None


async def validate_stock(job: ConnectedJobContext) -> dict[str, object]:
    # Check the stock update submitted through the Camunda Form.
    variables = job.variables.to_dict()
    product_id = variables.get("productId")
    product_name = variables.get("productName")
    new_stock = variables.get("newStockQuantity")
    season_start = parse_date(variables.get("seasonStartDate"))
    season_end = parse_date(variables.get("seasonEndDate"))

    valid_info = (
        bool(str(product_id or "").strip())
        and bool(str(product_name or "").strip())
        and isinstance(new_stock, (int, float))
        and new_stock >= 0
        and season_start is not None
        and season_end is not None
        and season_end >= season_start
    )

    job.log.info(
        f"Validating {product_name}: stock={new_stock}, "
        f"season={season_start} to {season_end}, valid={valid_info}"
    )

    # The "Is any info invalid?" gateway checks validInfo.
    return {"validInfo": valid_info}


async def save_stock_details(job: ConnectedJobContext) -> dict[str, object]:
    variables = job.variables.to_dict()

    # Test switch: start the instance with {"simulateSaveFailure": true}
    # to throw a BPMN error, which the "Save failed" boundary event catches.
    if variables.get("simulateSaveFailure"):
        job.log.info("Simulating a database failure")
        raise JobError("SAVE_FAILED", "Could not save the stock update")

    # Simulate saving to the inventory database.
    store = json.loads(STORE_FILE.read_text()) if STORE_FILE.exists() else {}
    store[str(variables["productId"])] = {
        "productName": variables.get("productName"),
        "stockQuantity": variables.get("newStockQuantity"),
        "seasonStartDate": variables.get("seasonStartDate"),
        "seasonEndDate": variables.get("seasonEndDate"),
        "reason": variables.get("stockUpdateReason"),
    }
    STORE_FILE.write_text(json.dumps(store, indent=2))

    job.log.info(f"Saved stock for {variables.get('productName')}")
    return {"saved": True}


async def product_unavailable(job: ConnectedJobContext) -> dict[str, object]:
    # Stock is zero, so customers can no longer order this product.
    job.log.info("Marking product unavailable")
    return {"productStatus": "unavailable"}


async def product_available(job: ConnectedJobContext) -> dict[str, object]:
    # Restocked and in season, so the product goes back on sale.
    job.log.info("Marking product available")
    return {"productStatus": "available"}


async def hide_product(job: ConnectedJobContext) -> dict[str, object]:
    # Restocked but out of season, so the product stays hidden for now.
    job.log.info("Keeping product hidden until season starts")
    return {"productStatus": "hidden"}


async def availability_published(job: ConnectedJobContext) -> dict[str, object]:
    # Simulate updating the customer-facing marketplace listing.
    variables = job.variables.to_dict()
    job.log.info(
        f"Publishing availability: {variables.get('productName')} is "
        f"{variables.get('productStatus')}"
    )
    return {"availabilityPublished": True}


async def notify_producer(job: ConnectedJobContext) -> dict[str, object]:
    # Simulate notifying the producer of the outcome (or the failed save).
    variables = job.variables.to_dict()
    product_status = variables.get("productStatus")

    if product_status:
        message = f"Your product {variables.get('productName')} is now {product_status}."
    else:
        message = "Your stock update could not be saved. Please try again."

    job.log.info(f"Notifying producer: {message}")
    return {"producerNotified": True}


def register_workers(client: CamundaAsyncClient) -> None:
    # One worker per job type in the F2 BPMN.
    workers = [
        ("validate_stock", "stock-validator", validate_stock),
        ("save_stock_details", "stock-saver", save_stock_details),
        ("product_unavailable", "product-unavailable-marker", product_unavailable),
        ("product_available", "product-available-marker", product_available),
        ("hide_product", "product-hider", hide_product),
        ("availability_published", "availability-publisher", availability_published),
        ("notify_producer", "failure-notifier", notify_producer),
        ("producer_notified", "status-notifier", notify_producer),
    ]

    for job_type, worker_name, callback in workers:
        client.create_job_worker(
            config=WorkerConfig(
                job_type=job_type,
                job_timeout_milliseconds=30_000,
                max_concurrent_jobs=5,
                worker_name=worker_name,
            ),
            callback=callback,
            execution_strategy="async",
        )