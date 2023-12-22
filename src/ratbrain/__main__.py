"""CLI for the package."""

import logging
import pathlib

import filepattern
import typer
from polus.plugins.formats.ome_converter.__main__ import main as ome_converter_main
from polus.plugins.visualization.precompute_slide.__main__ import (
    main as precompute_slide_main,
)

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
def main(  # noqa: PLR0915
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
    single_replicate: bool = typer.Option(
        False,
        "--single-replicate",
        "-s",
        help="Run only on a single replicate from the dataset.",
    ),
    delete_intermediates: bool = typer.Option(  # noqa: ARG001
        False,
        "--delete-intermediates",
        "-D",
        help="Delete intermediate files after processing.",
    ),
) -> None:
    """Run some experiments with the RatBrain dataset."""
    logger.info(f"Data directory: {data_dir}")

    original_dir = data_dir / "original"
    if not original_dir.exists():
        msg = f"Original data directory does not exist: {original_dir}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    czi_dir = data_dir / "RB_50-plex-IHC"
    if not czi_dir.exists():
        msg = f"RatBrain CZI data directory does not exist: {czi_dir}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    # Use the ome-converter plugin to convert the original images to OME-TIFF
    logger.info("Converting original images to OME-TIFF...")

    if single_replicate:
        num_images = 11
        original_pattern = "R1C{c:d+}.tif"
        original_ome_pattern = "R1C{c:d+}.ome.tif"
        original_pyramids_pattern = "R1C{c:d+}.ome.zarr"
        czi_pattern = "S1_R1_C1-C11_A1.czi"
    else:
        num_images = 11 * 5
        original_pattern = "R{r:d}C{c:d+}.tif"
        original_ome_pattern = "R{r:d}C{c:d+}.ome.tif"
        original_pyramids_pattern = "R{r:d}C{c:d+}.ome.zarr"
        czi_pattern = "S1_R{r:d}_C1-C11_A1.czi"

    original_ome_dir = data_dir / "original-ome"
    original_ome_dir.mkdir(exist_ok=True)

    original_ome_fp = filepattern.FilePattern(original_ome_dir, original_ome_pattern)
    original_ome_files = [file for _, [file] in original_ome_fp()]
    if len(original_ome_files) == num_images:
        logger.info("OME-TIFF files already exist. Skipping conversion.")
    else:
        ome_converter_main(
            inp_dir=original_dir,
            pattern=original_pattern,
            file_extension=".ome.tif",
            out_dir=original_ome_dir,
            preview=False,
        )

    # Use the pre-compute-slide plugin to create pyramids for the original
    # images
    logger.info("Creating pyramids for the original images...")

    original_pyramids_dir = data_dir / "original-pyramids"
    original_pyramids_dir.mkdir(exist_ok=True)

    original_pyramids_fp = filepattern.FilePattern(
        original_pyramids_dir,
        original_pyramids_pattern,
    )
    original_pyramids_files = [file for _, [file] in original_pyramids_fp()]
    if len(original_pyramids_files) == num_images:
        logger.info("Pyramids already exist. Skipping pyramid creation.")
    else:
        precompute_slide_main(
            inp_dir=original_ome_dir,
            filepattern=original_ome_pattern,
            out_dir=original_pyramids_dir,
            pyramid_type="Zarr",
            image_type="Intensity",
            preview=False,
        )
        # Some pyramids do not have the ".ome.zarr" extension. Add it to their names
        pre_zaar_fp = filepattern.FilePattern(original_pyramids_dir, "R{r:d}C{c:d+}")
        file: pathlib.Path
        for _, [file] in pre_zaar_fp():
            if ".ome.zarr" not in file.name:
                file.rename(file.name + ".ome.zarr")

    # Use the czi-extract plugin to extract the CZI files into FOVs
    fovs_dir = data_dir / "fovs"
    fovs_dir.mkdir(exist_ok=True)

    logger.info(f"Extracting CZI files into FOVs {czi_pattern}...")
    logging.info("TODO")

    # Use the basic-flatfield-estimation plugin to estimate the flatfield and
    # darkfield components of the FOVs.

    ff_dir = data_dir / "fovs-ff"
    ff_dir.mkdir(exist_ok=True)

    logger.info("Estimating flatfield and darkfield components of FOVs...")
    logger.info("TODO")

    # Use the apply-flatfield plugin to apply the flatfield and darkfield
    # correction to the FOVs.

    logger.info("Applying flatfield and darkfield correction to FOVs...")
    logger.info("TODO")

    # Use the MIST plugin to get a stitching vector
    logger.info("Getting stitching vector...")
    logger.info("TODO")

    # Recycle the stitching vector for all channels and replicates
    logger.info("Recycling stitching vector for all channels and replicates...")
    logger.info("TODO")

    # Use the image-assembler plugin to stitch the FOVs
    logger.info("Stitching FOVs...")
    logger.info("TODO")

    # Use the pre-compute-slide plugin to create pyramids for the stitched
    # images
    logger.info("Creating pyramids for the stitched images...")
    logger.info("TODO")


if __name__ == "__main__":
    app()
