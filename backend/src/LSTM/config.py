import datetime
import os

# Model name
CUSTOME_NAME = "roberta-LSTM-augumented"

# Dataset
DATA_DIR_PATH = "./dataset"
TRAIN_DATASET_PATH = os.path.join(DATA_DIR_PATH, "train_ru.csv")
TEST_DATASET_PATH = os.path.join(DATA_DIR_PATH, "test_ru.csv")
LABEL_LIST = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

# Session
SESSION_DIR_PATH = os.path.abspath("./session")
SESSION_DATETIME = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S-%f")
SESSION_NAME = f"{CUSTOME_NAME}_{SESSION_DATETIME}"
CURRENT_SESSION_DIR_PATH = os.path.join(SESSION_DIR_PATH, SESSION_NAME)

os.makedirs(CURRENT_SESSION_DIR_PATH, exist_ok=True)

# Architecture de fichier dans `CURRENT_SESSION_DIR_PATH`
LOG_FILE_NAME = f"{SESSION_NAME}.loguru.log"
MODEL_FILE_NAME = f"{SESSION_NAME}.model"
TEST_FILE_NAME = f"{SESSION_NAME}.test.csv"
VALIDATION_DATASET_NAME = f"{SESSION_NAME}.jigsaw2019-validation.csv"
VALIDATION_FILE_NAME = f"{SESSION_NAME}.validation.csv"
METRIC_FILE_NAME = f"{SESSION_NAME}.metric.json"
LOG_FILE_PATH = os.path.join(CURRENT_SESSION_DIR_PATH, LOG_FILE_NAME)
MODEL_FILE_PATH = os.path.join(CURRENT_SESSION_DIR_PATH, MODEL_FILE_NAME)
TEST_FILE_PATH = os.path.join(CURRENT_SESSION_DIR_PATH, TEST_FILE_NAME)
VALIDATION_DATASET_FILE_PATH = os.path.join(CURRENT_SESSION_DIR_PATH, VALIDATION_DATASET_NAME)
VALIDATION_FILE_PATH = os.path.join(CURRENT_SESSION_DIR_PATH, VALIDATION_FILE_NAME)
METRIC_FILE_PATH = os.path.join(CURRENT_SESSION_DIR_PATH, METRIC_FILE_NAME)
