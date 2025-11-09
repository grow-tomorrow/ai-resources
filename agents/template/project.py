import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from sentence_transformers import SentenceTransformer
import markdown
from dotenv import load_dotenv
from openai import OpenAI
import re
from pathlib import Path
import numpy as np
import hashlib
from pymilvus import MilvusClient, DataType


# Load environment variables from .env file
load_dotenv()

# Debug flag from environment (default to False)
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Connect to Milvus (local server or Milvus Lite)
# client_milvus = MilvusClient(uri="http://localhost:19530")
#client_milvus = MilvusClient(uri="milvus-lite.db")


if __name__ == "__main__":
    print("Starting the project...")