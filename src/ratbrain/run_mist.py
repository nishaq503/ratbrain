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


def recycle_vectors(  # noqa: PLR0913
    *,
    base_vector_path: pathlib.Path,
    recycle_vector_dir: pathlib.Path,
    num_channels: int,
    num_replicates: int,
    num_xs: int,
    num_ys: int,
) -> None:
    """Recycle the stitching vector for all channels and replicates."""
    base_img_name_pattern = "S1_R1_C1-C11_A1_y0{y:02d}_x0{x:02d}_c000.ome.tif"
    recycled_img_name_pattern = (
        "S1_R{r:d}_C1-C11_A1_y0{y:02d}_x0{x:02d}_c0{c:02d}.ome.tif"
    )
    recycle_vector_pattern = (
        "S1_R{r:d}_C1-C11_A1_y0(00-14)_x0(00-21)_c0{c:02d}-global-positions-1.txt"
    )

    with base_vector_path.open("r") as reader:
        raw_lines = reader.readlines()
    lines_parts = [line.split(";") for line in raw_lines]
    lines = {parts[0].split(": ")[1].strip(): parts[1:] for parts in lines_parts}

    for r in range(1, num_replicates + 1):
        for c in range(num_channels):
            recycled_vector_path = recycle_vector_dir / recycle_vector_pattern.format(
                r=r,
                c=c,
            )

            with recycled_vector_path.open("w") as writer:
                for y in range(num_ys):
                    for x in range(num_xs):
                        base_img_name = base_img_name_pattern.format(y=y, x=x)
                        recycled_img_name = recycled_img_name_pattern.format(
                            r=r,
                            y=y,
                            x=x,
                            c=c,
                        )

                        recycled_parts = [f"file: {recycled_img_name}"] + lines[
                            base_img_name
                        ]
                        recycled_line = ";".join(recycled_parts)
                        writer.write(recycled_line)
