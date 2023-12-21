"""CLI for the package."""

import logging
import pathlib

import typer

from ratbrain.utils import constants

# Initialize the logger
logging.basicConfig(
    format="%(asctime)s - %(name)-8s - %(levelname)-8s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
logger = logging.getLogger("RatBrain")
logger.setLevel(constants.POLUS_LOG)

app = typer.Typer()


@app.command()
def main(
    data_dir: pathlib.Path = typer.Option(
        ...,
        "--data-dir",
        "-d",
        help="Path to the data directory.",
        exists=True,
        file_okay=False,
        readable=True,
        writable=True,
        resolve_path=True,
    ),
) -> None:
    """Run some experiments with the RatBrain dataset."""
    logger.info(f"Data directory: {data_dir}")


if __name__ == "__main__":
    app()
