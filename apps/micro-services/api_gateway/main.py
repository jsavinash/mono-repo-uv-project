from typer import Typer

from shared.contracts import ProductPlan

app = Typer(add_completion=False)


@app.command()
def run():
    """Run the api gateway CLI."""
    print("Hello from api gateway!")
    print(f"Plans available: {ProductPlan(name='Starter', price_monthly=19, description='Test')}")


if __name__ == "__main__":  # pragma: no cover
    app()