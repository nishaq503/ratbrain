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

    # Columns in "Supplementary Table 7.xlsx" are:
    # ['ID', 'centroid_x', 'centroid_y', 'xmin', 'ymin', 'xmax', 'ymax',
    #    'NeuN', 'S100', 'Olig2', 'Iba1', 'RECA1', 'Cleaved Caspase-3',
    #    'Tyrosine Hydroxylase', 'Blood Brain Barrier', 'GFP', 'PDGFR beta',
    #    'Parvalbumin', 'Choline Acetyltransferase', 'GFAP',
    #    'Smooth Muscle Actin', 'Glutaminase', 'Doublecortin', 'Sox2', 'PCNA',
    #    'Vimentin', 'GAD67', 'Tbr1', 'Eomes', 'Calretinin', 'Nestin',
    #    'Aquaporin-4', 'Calbindin']


if __name__ == "__main__":
    app()
