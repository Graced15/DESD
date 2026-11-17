
from camunda_orchestration_sdk import (
    CamundaAsyncClient,
    ConnectedJobContext,
    WorkerConfig,
)


async def publish_product(job: ConnectedJobContext) -> dict[str, object]:
    # Read the product details submitted through the Camunda Form.
    variables = job.variables.to_dict()
    product_name = variables.get("productName")

    if not isinstance(product_name, str) or not product_name.strip():
        raise ValueError("Product name is missing")

    # Simulate publishing the product.
    job.log.info(f"Publishing product: {product_name}")

    # Return the publication result to the Camunda process.
    return {
        "publicationStatus": "published",
        "publishedProductName": product_name,
    }


def register_workers(client: CamundaAsyncClient) -> None:
    client.create_job_worker(
        config=WorkerConfig(
            job_type="publish-product",
            job_timeout_milliseconds=30_000,
            max_concurrent_jobs=5,
            worker_name="product-publisher",
        ),
        callback=publish_product,
        execution_strategy="async",
    )

