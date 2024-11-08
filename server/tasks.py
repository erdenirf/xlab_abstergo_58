from datetime import datetime
import logging
from celery import Celery
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

CELERY_BROKER = os.environ.get("CELERY_BROKER")
CELERY_BACKEND = os.environ.get("CELERY_BACKEND")

app = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)

THE_FILENAMES: dict[str, str] = {}
DEFAULT_FILENAME = ""

def model_generate(prompt: str, filename_id: str) -> str:
    
    THE_FILENAMES[filename_id] = DEFAULT_FILENAME

    time.sleep(10)   #sec

    THE_FILENAMES[filename_id] = "./16742513.mp3"
    return "./16742513.mp3"

def is_exist(filename_id: str) -> bool:
    return filename_id in THE_FILENAMES

def get_filename(filename_id: str) -> str | None:
    return THE_FILENAMES.get(filename_id) if THE_FILENAMES.get(filename_id) != DEFAULT_FILENAME else None

@app.task()
def ai_model_get_filename(prompt: str, filename_id: str) -> str:

    filename = model_generate(prompt, filename_id)
    return filename