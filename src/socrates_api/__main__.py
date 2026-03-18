"""CLI entry point for running Socrates API server."""

import argparse
import sys
from typing import Optional

import uvicorn

from socrates_api import create_app


def main(argv: Optional[list[str]] = None) -> int:
    """Run Socrates API server."""
    parser = argparse.ArgumentParser(description="Socrates API Server")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)",
    )

    args = parser.parse_args(argv)

    app = create_app()

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
