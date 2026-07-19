from main import build_welcome_message


def test_build_welcome_message() -> None:
    assert build_welcome_message() == "Hello from python-mono-repo-starter-kit!"
