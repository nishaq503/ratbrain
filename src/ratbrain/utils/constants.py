"""Constants used in the package."""

import logging
import multiprocessing
import os

MAX_WORKERS = max(1, multiprocessing.cpu_count() // 2)

POLUS_LOG = getattr(logging, os.environ.get("POLUS_LOG", "INFO"))
POLUS_IMG_EXT = os.environ.get("POLUS_IMG_EXT", ".ome.tif")
POLUS_TAB_EXT = os.environ.get("POLUS_TAB_EXT", ".csv")
