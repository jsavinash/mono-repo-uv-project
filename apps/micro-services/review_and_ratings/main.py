from typer import Typer

from shared.contracts import ProductPlan

app = Typer(add_completion=False)


@app.command()
def run():
    """Run the review and ratings CLI."""
    from shared.number_utils import add_two_numbers

    print("Hello from review and ratings!")
    print(f"Plans available: {ProductPlan(name='Starter', price_monthly=19, description='Test')}")
    add_two_numbers(1, 2)  # noqa: F841


if __name__ == "__main__":  # pragma: no cover
    app()