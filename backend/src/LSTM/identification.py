import os
import time
import datetime
from typing import Any, Union, Dict, List
import uuid
import json
import warnings

import pandas as pd
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
# import torchtext
# import nltk
# import sklearn
# import transformers
# import torchmetrics as tm
# from torchmetrics import MetricCollection, Metric, Accuracy, Precision, Recall, AUROC, HammingDistance, F1Score, ROC, \
#     PrecisionRecallCurve

from loguru import logger
from tqdm.auto import tqdm
from config import *

tqdm.pandas()

warnings.filterwarnings("ignore")

# CUDA
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

logger.add(LOG_FILE_PATH, level="TRACE")
logger.info(f"{SESSION_NAME=}")
logger.info(f"{TRAIN_DATASET_PATH=}")
logger.info(f"{TEST_DATASET_PATH=}")
logger.info(f"{CURRENT_SESSION_DIR_PATH=}")
logger.info(f"{LABEL_LIST=}")
logger.info(f"Checking consistency...")


if not os.path.exists(TRAIN_DATASET_PATH):
    logger.critical(f"Train dataset does not exist !")
    raise RuntimeError("Train dataset does not exist !")
if not os.path.exists(TEST_DATASET_PATH):
    logger.critical(f"Test dataset does not exist !")
    raise RuntimeError("Test dataset does not exist !")
logger.success("Datasets are reachable")


GPU_IS_AVAILABLE = torch.cuda.is_available()
GPU_COUNT = torch.cuda.device_count()
logger.info(f"{GPU_IS_AVAILABLE=}")
logger.info(f"{GPU_COUNT=}")
if not GPU_IS_AVAILABLE:
    logger.warning("GPU and CUDA are not available !")
    # raise RuntimeError("GPU and CUDA are not available !")
else:
    logger.success("GPU and CUDA are available")
logger.info(f"{device=}")
for gpu_id in range(GPU_COUNT):
    gpu_name = torch.cuda.get_device_name(0)
    logger.info(f"GPU {gpu_id} : {gpu_name}")

all_train_df = pd.read_csv(TRAIN_DATASET_PATH, index_col=0)
logger.success("Dataset loaded !")

all_train_df.head()
test_df = pd.read_csv(TEST_DATASET_PATH)
