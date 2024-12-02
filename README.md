# Phishing URL Detection System

A live web application designed to identify and predict phishing URLs using advanced machine learning techniques. This project was developed as part of the CMPE255 Data Mining course at San Jose State University.

## Hosted Application

- **Streamlit App**: [Phishing App](https://phishing-app-255.streamlit.app/)  
  _(Note: The application may take ~1 minute to load if idle for a while.)_

## Project Overview

Phishing attacks pose significant risks in today's digital world. This project aims to address these challenges by creating a reliable and user-friendly system to classify URLs as phishing or legitimate. The application leverages a robust backend powered by machine learning and a user-friendly frontend hosted on Streamlit.

### Features

- **Real-time Prediction**: Predicts whether a URL is malicious or safe.
- **User-Friendly Interface**: Simple input form with binary classification output (Safe/Phishing).
- **Secure Design**: Focuses on minimizing false negatives to enhance user safety.

## System Design

### Architecture

- **Frontend**: 
  - Built using HTML, hosted with Streamlit.
  - Collects user input (URL + additional Y/N questions).
- **Backend**:
  - Developed in Python.
  - Loads trained machine learning models to process user input and returns predictions.

### Models Used

1. **Supervised Models**:
   - Decision Tree Classification
   - Perceptron
   - Support Vector Classification (SVC)
   - K-Nearest Neighbors (KNN)
2. **Unsupervised Models**:
   - KMeans Clustering
   - Agglomerative Clustering

### Dataset

- **Source**: PhiUSIIL Phishing URL dataset (UC Irvine Machine Learning Repository)
- **Features**: 54 features across 235,795 entries, including HTML and URL-extracted attributes.
- **Class Distribution**: 134,850 legitimate websites and 100,945 phishing websites.

## Implementation Details

- **Data Preprocessing**:
  - Feature selection based on correlation analysis (e.g., retaining `IsHTTPs` for strong predictive power).
  - Dimensionality reduction techniques: LDA and PCA.
- **Evaluation Metrics**:
  - Accuracy, F1 Score, and False Negative Rate (FNR).
- **Key Model**: 
  - SVC with scaled data achieved the best performance:
    - Accuracy > 90%
    - FNR < 15%

## How to Run Locally

### Prerequisites

- Python 3.7+
- Streamlit
- Required libraries: `pandas`, `numpy`, `sklearn`, `seaborn`, `matplotlib`

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/ishang999/phishing-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd phishing-app
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```
5. Access the app at `http://localhost:8501`.

## Results and Insights

- **Dimensionality Reduction**: LDA outperformed PCA in preserving class separability.
- **Model Evaluation**:
  - Supervised models significantly outperformed unsupervised ones.
  - SVC was selected for deployment due to its superior performance.
- **Cross-Validation**: Ensured robustness with 10-fold validation over sampled data.
