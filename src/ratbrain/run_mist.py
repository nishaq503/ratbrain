"""Run the MIST docker container to get a single stitching vector."""


import logging
import pathlib
import subprocess

from .utils import constants

logger = logging.getLogger(__name__)
logger.setLevel(constants.POLUS_LOG)


def main(  # noqa: PLR0913
    *,
    data_dir: pathlib.Path,
    docker_image_name: str,
    image_dir: str,
    filename_pattern_type: str,
    filename_pattern: str,
    grid_origin: str,
    grid_width: int,
    grid_height: int,
    start_tile_row: int,
    start_tile_col: int,
    start_row: int,
    start_col: int,
    extent_width: int,
    extent_height: int,
    is_time_slices: bool,
    assemble_no_overlap: bool,
    stage_repeatability: int,
    overlap_uncertainty: int,
    program_type: str,
    output_path: str,
) -> None:
    """Run the MIST docker container to get a single stitching vector."""
    logger.info("Starting MIST docker container...")

    command_parts = [
        "--imageDir",
        f"/data/{image_dir}",
        "--filenamePatternType",
        filename_pattern_type,
        "--filenamePattern",
        filename_pattern,
        "--gridOrigin",
        grid_origin,
        "--gridWidth",
        str(grid_width),
        "--gridHeight",
        str(grid_height),
        "--startTileRow",
        str(start_tile_row),
        "--startTileCol",
        str(start_tile_col),
        "--startRow",
        str(start_row),
        "--startCol",
        str(start_col),
        "--extentWidth",
        str(extent_width),
        "--extentHeight",
        str(extent_height),
        "--isTimeSlices",
        str(is_time_slices),
        "--assembleNoOverlap",
        str(assemble_no_overlap),
        "--stageRepeatability",
        str(stage_repeatability),
        "--overlapUncertainty",
        str(overlap_uncertainty),
        "--programType",
        program_type,
        "--outputPath",
        f"/data/{output_path}",
    ]

    command = [
        "docker",
        "run",
        "-v",
        f"{data_dir}:/data",
        docker_image_name,
        *command_parts,
    ]

    logger.info(f"Running command: {' '.join(command)}")

    subprocess.run(command, check=True)  # noqa: S603
