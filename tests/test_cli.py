from typer.testing import CliRunner

from core.print import printAnything


def test_main() -> None:
    """Test the main function of the CLI."""

    runner = CliRunner()
    result = runner.invoke(printAnything)
    assert result.exit_code == 0
    assert "Hello from core packages" in result.output
