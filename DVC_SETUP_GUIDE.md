# Step-by-Step DVC Pipeline Setup Guide

This document explains the sequence of DVC commands required to build and connect this ML pipeline from scratch. It outlines the exact commands to create the `dvc.yaml` file by defining which Python files to execute and connecting their inputs and outputs.

### Step 1: Initialize Git and DVC
DVC relies on Git, so the repository must be initialized with Git first, followed by DVC.
```bash
git init
dvc init
```

### Step 2: Create the Data Ingestion Stage
The first step is to ingest the raw data. This command creates a DVC stage named `data_ingestion`.
- **File to execute**: `src/data_ingestion.py`
- **Command**:
```bash
dvc stage add -n data_ingestion \
    -d src/data_ingestion.py \
    -o data/raw \
    python src/data_ingestion.py
```

### Step 3: Create the Data Preprocessing Stage
This stage depends on the raw data created in the previous step and cleans the text.
- **File to execute**: `src/data_preprocessing.py`
- **Command**:
```bash
dvc stage add -n data_preprocessing \
    -d src/data_preprocessing.py \
    -d data/raw \
    -o data/processed \
    python src/data_preprocessing.py
```

### Step 4: Create the Feature Engineering Stage
This stage transforms the processed text data into numerical vectors using Bag of Words.
- **File to execute**: `src/feature_engineering.py`
- **Command**:
```bash
dvc stage add -n feature_engineering \
    -d src/feature_engineering.py \
    -d data/processed \
    -o data/features \
    python src/feature_engineering.py
```

### Step 5: Create the Model Building Stage
This stage trains the Gradient Boosting model on the engineered features.
- **File to execute**: `src/model_building.py`
- **Command**:
```bash
dvc stage add -n model_building \
    -d src/model_building.py \
    -d data/features \
    -o model.pkl \
    python src/model_building.py
```

### Step 6: Create the Model Evaluation Stage
This final stage evaluates the trained model and produces accuracy, precision, recall, and AUC.
- **File to execute**: `src/model_evaluation.py`
- **Command**:
```bash
dvc stage add -n model_evaluation \
    -d src/model_evaluation.py \
    -d data/features/test_bow.csv \
    -d model.pkl \
    -o data/metrics.json \
    python src/model_evaluation.py
```
*(Note: In DVC, if you want to track a file specifically as a metric rather than a standard output, you can use `-m data/metrics.json` instead of `-o data/metrics.json`)*

### Step 7: Execute the Pipeline
By running the `dvc stage add` commands above, DVC generates the `dvc.yaml` file. To execute the entire sequence of scripts in the correct order, run:
```bash
dvc repro
```
DVC will automatically analyze the dependencies and execute the scripts in the correct order:
1. `src/data_ingestion.py`
2. `src/data_preprocessing.py`
3. `src/feature_engineering.py`
4. `src/model_building.py`
5. `src/model_evaluation.py`

### Step 8: View Execution Flow and Graph (Optional)
To verify your pipeline dependencies and see a visual representation of how the scripts are connected:
```bash
dvc dag
```
