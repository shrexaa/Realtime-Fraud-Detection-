"""
FinShield: All-in-One Local Runner & Demonstration Launcher
"""

import os
import sys
import time
import subprocess
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from train_model import train_and_export, MODEL_PATH
from database import init_db, insert_transactions
from producer import generate_transaction_event
from stream_processor import load_scoring_model, score_dataframe

def prepare_system():
    print("=" * 65)
    print("  FinShield: Real-Time Fraud & Anomaly Detection Pipeline")
    print("  Big Data Analytics (BDA) Capstone Project")
    print("=" * 65)

    # 1. Initialize DB
    print("[1/3] Initializing local audit database...")
    init_db()

    # 2. Check / Train ML Model
    if not os.path.exists(MODEL_PATH):
        print("[2/3] Trained model artifact not detected. Triggering training pipeline...")
        train_and_export()
    else:
        print(f"[2/3] Found existing trained model at: {MODEL_PATH}")

    # 3. Pre-seed simulated stream so dashboard immediately populates
    print("[3/3] Pre-seeding 50 telemetry transactions into audit store...")
    model = load_scoring_model()
    events = []
    for i in range(50):
        is_fraud = (i % 12 == 0)
        events.append(generate_transaction_event(simulate_fraud=is_fraud))
    
    df = pd.DataFrame(events)
    scored_df = score_dataframe(df, model)
    insert_transactions(scored_df)
    print(f"[+] Successfully loaded {len(scored_df)} scored events into audit store.")

    print("\n" + "=" * 65)
    print("  SETUP COMPLETE! Launching interactive Streamlit dashboard...")
    print("=" * 65)

    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard", "app.py")
    subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])

if __name__ == "__main__":
    prepare_system()
