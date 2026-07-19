from io import StringIO
from contextlib import redirect_stdout


def print_anything() -> None:
    print("Hello from core packages")


def test_main() -> None:
    """Test the main function of the CLI."""

    buffer = StringIO()
    with redirect_stdout(buffer):
        print_anything()

    assert buffer.getvalue().strip() == "Hello from core packages"
