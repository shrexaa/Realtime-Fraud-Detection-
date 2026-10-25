# FinShield: Real-Time Fraud & Anomaly Detection Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-7.5.0-red.svg)](https://kafka.apache.org/)
[![Apache Spark](https://img.shields.io/badge/Apache_Spark-3.5.0-orange.svg)](https://spark.apache.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-PR--AUC_Optimized-green.svg)](https://xgboost.readthedocs.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live_Dashboard-FF4B4B.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Final Practical Assessment & Major Capstone Project**  
> **Course:** Big Data Analytics (BDA) — 8th Semester  
> **Institution:** Department of Computer Science & Engineering, Arya College of Engineering & I.T.  
> **Affiliation:** Rajasthan Technical University (RTU), Kota  
> **Candidate:** Gaurav Singh Sikarwar (Roll No: `22EARCS053`)

---

## 📌 1. Project Overview

Modern financial ecosystems (UPI, credit cards, POS gateways) process tens of thousands of transactions every second. Traditional batch analytics and end-of-day SQL reconciliation fail to prevent fraudulent transactions in flight. 

**FinShield** is an enterprise-grade distributed streaming analytics system designed to solve this latency challenge. It ingests high-velocity transaction streams, processes micro-batches across distributed clusters via **Apache Spark Structured Streaming** and **Apache Kafka**, executes real-time inference using an imbalanced-tuned **XGBoost Classifier**, and surfaces risk indicators on a live reactive **Streamlit & Plotly** dashboard.

---

## 🏗️ 2. Architectural Design

```
                     HIGH-VELOCITY DISTRIBUTED ARCHITECTURE
                     
  [High-Velocity POS/UPI]               [Message Broker]                [Distributed Stream Processor]
   ┌────────────────────┐            ┌────────────────────┐            ┌──────────────────────────────┐
   │                    │            │    Apache Kafka    │            │       Apache PySpark         │
   │  producer.py       │ ──────────>│  Topic:            │ ──────────>│    Structured Streaming      │
   │  (~10-50 tx/sec)   │   JSON     │  "transactions-in" │  Micro-    │    (Windowed Aggregations)   │
   └────────────────────┘            └────────────────────┘  batches   └──────────────┬───────────────┘
                                                │                                     │
                                                │ (Admin Telemetry)                   │ Low-Latency Inference
                                                ▼                                     ▼
                                     ┌────────────────────┐            ┌──────────────────────────────┐
                                     │  Kafka-UI Console  │            │     Trained XGBoost Model    │
                                     │  (Port 8080)       │            │     (Scale Pos-Weight Tuned) │
                                     └────────────────────┘            └──────────────┬───────────────┘
                                                                                      │
                                                                       Flags Suspicious Transactions
                                                                                      │
                                                                                      ▼
                               [Presentation & Alerting]               [Audit & Persistence Layer]
   ┌────────────────────────────────────────────────────────┐          ┌──────────────────────────────┐
   │             Live Operations Center                     │          │   Distributed DB / SQLite    │
   │  - Real-Time Fraud KPI Metrics (Throughput, Blocked $) │<─────────│   Table:                     │
   │  - Plotly Anomaly Geographic Heatmaps (Jaipur, etc.)   │          │   "transactions_stream"      │
   │  - Live Suspicious Transaction Interception Feed       │          └──────────────────────────────┘
   └────────────────────────────────────────────────────────┘
```

---

## 📂 3. Repository Structure

```text
realtime-fraud-detection-bigdata/
│
├── docker-compose.yml        # Docker definitions: Zookeeper, Kafka, Kafka-UI
├── Dockerfile                # Production multi-stage Dockerfile
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT Open Source License
├── README.md                 # Project documentation & presentation guide
├── run_demo.py               # 1-Click offline demonstrator & dashboard launcher
│
├── data/
│   ├── .gitkeep
│   ├── transactions.csv      # Baseline benchmark training dataset (auto-generated)
│   └── fraud_audit.db        # Live telemetry SQLite audit database
│
├── models/
│   ├── .gitkeep
│   └── fraud_model.json      # Serialized XGBoost classification artifact
│
├── src/
│   ├── __init__.py
│   ├── database.py           # Database connection, audit schema & query helpers
│   ├── train_model.py        # ML training script with severe imbalance handling
│   ├── producer.py           # Kafka stream producer with burst anomaly injection
│   └── stream_processor.py   # Dual-engine streaming consumer (Spark + Direct)
│
├── dashboard/
│   ├── __init__.py
│   └── app.py                # Live Streamlit & Plotly analytics dashboard
│
└── tests/
    └── test_pipeline.py      # Automated unit tests for ETL & database integrity
```

---

## ⚡ 4. Quick Start (Prerequisites & Installation)

### Prerequisites
* **Python 3.10+**
* **Docker Desktop** (for Apache Kafka & Kafka-UI)
* Optional: OpenJDK 11+ (if executing native PySpark mode)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/realtime-fraud-detection-bigdata.git
cd realtime-fraud-detection-bigdata
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 5. How to Run the Distributed Pipeline

### Step 1: Start Distributed Kafka Infrastructure
Launch Zookeeper, Kafka Broker, and Kafka-UI in the background:
```bash
docker compose up -d
```
> 💡 *Check Kafka-UI at `http://localhost:8080` to view brokers, topics, and message rates in real time.*

### Step 2: Train & Export the Machine Learning Model
```bash
python src/train_model.py
```
* Generates 150,000 synthetic transaction records.
* Applies `scale_pos_weight` to compensate for the 2.5% fraud imbalance.
* Exports serialized weights to `models/fraud_model.json` along with ROC-AUC & PR-AUC scores.

### Step 3: Run the Stream Processing Engine
Open a new terminal window:
```bash
# Recommended for all operating systems (Zero-dependency direct streaming engine)
python src/stream_processor.py --engine direct

# Or with distributed PySpark Structured Streaming (Requires Java/Hadoop environment)
python src/stream_processor.py --engine spark
```

### Step 4: Start the High-Velocity Transaction Producer
Open a new terminal window:
```bash
python src/producer.py
```
* Generates continuous live transactions simulating Indian metropolitan payment gateways (Jaipur, Delhi, Mumbai, Bengaluru, etc.).
* Periodically simulates burst fraud attacks for real-time interception testing.

### Step 5: Launch the Live Operations Dashboard
Open a new terminal window:
```bash
streamlit run dashboard/app.py
```
* Navigate to `http://localhost:8501`.
* Monitor live intercepted transactions, geographic risk distribution, and protected capital.

---

## 🎯 6. One-Click Demonstration Mode (No Docker Required)

If presenting on a college laptop without Docker or for immediate offline demonstrations:
```bash
python run_demo.py
```
This script will:
1. Initialize the audit database schema.
2. Train the XGBoost model if not present.
3. Pre-seed 50 realistic transactions into the database.
4. Automatically boot up the interactive Streamlit dashboard.

---

## 🧪 7. Running Unit Tests

Run automated unit tests to verify database operations and synthetic generation:
```bash
python -m unittest tests/test_pipeline.py
```

---

## 🌐 8. Production Cloud Deployment (AWS EC2 / Linux VM)

### 1. Provision Server
Launch an **Ubuntu 22.04 LTS (t3.large or 4GB+ RAM)** instance and open ports `8501`, `8080`, and `80`.

### 2. Run Containerized Stack
```bash
# Install Docker on Ubuntu
sudo apt update && sudo apt install -y docker.io docker-compose git

# Clone repository
git clone https://github.com/<your-username>/realtime-fraud-detection-bigdata.git
cd realtime-fraud-detection-bigdata

# Build and start services
docker compose up -d --build
```

### 3. Nginx Reverse Proxy (Optional)
```nginx
server {
    listen 80;
    server_name fraud-analytics.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 🎓 9. Viva Voce & External Examiner Defense (Q&A)

### Q1: What makes this a "Big Data" project rather than traditional ML?
**Answer:** The architecture addresses the core **3 V's**:
* **Velocity:** Transactions arrive asynchronously at sub-second speeds. Kafka decouples ingestion while Spark processes micro-batches without locking.
* **Volume:** Scalable horizontally across Kafka partitions and Spark worker nodes.
* **Variety:** Semi-structured JSON payloads with varied attributes (telemetry, geo-spatial, device trust scores).

### Q2: How did you solve the severe class imbalance problem in fraud detection?
**Answer:** In retail and financial datasets, fraudulent records constitute only 1–3% of total volume. We:
1. Applied **PR-AUC (Precision-Recall AUC)** instead of standard accuracy (which is deceptively high on imbalanced data).
2. Set the `scale_pos_weight` parameter in XGBoost proportional to $\frac{\text{Negative Samples}}{\text{Positive Samples}}$ to heavily penalize false negatives (missed frauds).

### Q3: Why use Kafka between the producer and the stream processor?
**Answer:** Kafka acts as a distributed shock absorber (backpressure buffer). If transaction traffic surges during peak festival seasons (e.g., Diwali or Big Billion Days), Kafka queues incoming events without dropping packets, allowing consumer workers to process them at their sustainable rate.

---

## 📄 10. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
