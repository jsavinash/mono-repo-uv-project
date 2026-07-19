from core.print import printAnything
from shared.numberUtils import addTwoNumbers
from typer import Typer

app = Typer(add_completion=False)


@app.command()
def main():
    print("Hello from product!")
    printAnything()
    addTwoNumbers(1, 2)


if __name__ == "__main__":  # pragma: no cover
    app()
