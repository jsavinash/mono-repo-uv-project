from contextlib import redirect_stdout
from io import StringIO

from core import printAnything


def test_main() -> None:
    """Test the main function of the CLI."""

    buffer = StringIO()
    with redirect_stdout(buffer):
        printAnything()

    assert buffer.getvalue().strip() == "Hello from core packages"
