import warnings
import logging
import os

# Suppress warnings and logs
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
warnings.filterwarnings("ignore")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("accelerate").setLevel(logging.ERROR)

from transformers import pipeline

llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device_map=None
)

def run_llm(prompt):
    return llm(prompt, max_length=200, truncation=True, max_new_tokens=None)[0]["generated_text"]
