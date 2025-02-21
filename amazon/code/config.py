import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
COMMENTS_DIR = os.path.join(RESULTS_DIR, "Comments")
AI_SUMMARY_DIR = os.path.join(RESULTS_DIR, "AI_Summary")

# Ensure directories exist
os.makedirs(COMMENTS_DIR, exist_ok=True)
os.makedirs(AI_SUMMARY_DIR, exist_ok=True)
