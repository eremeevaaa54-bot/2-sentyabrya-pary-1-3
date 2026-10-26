import logging
import sys
from src.gui.app import run

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("http_gui.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> int:
    configure_logging()
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())