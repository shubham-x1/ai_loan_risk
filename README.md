CrediAI – AI-Based Loan Risk Assessment System

CrediAI is an end-to-end AI underwriting platform that evaluates loan applicants in real time. The system analyzes financial and demographic inputs, applies a trained machine learning model, and generates an instant credit decision along with risk insights and analytics.

It predicts the probability of loan approval, assigns a risk score, recommends an appropriate interest rate, and flags potentially fraudulent applications. All applications are stored in a database and visualized through a dashboard that provides approval trends and risk analytics.

The project simulates how modern fintech and NBFC companies automate credit decisioning using machine learning, APIs, and cloud deployment.
AI Loan Risk & Approval System

A full-stack AI powered loan underwriting web application that predicts loan approval probability, risk score, suggested interest rate and fraud flag in real time.
The system simulates a mini credit decision engine similar to those used by NBFCs and fintech companies.

Live Links

Frontend (Vercel):
https://ailoanrisk-izvhbbab2-satputeshubham424-gmailcoms-projects.vercel.app/

Backend API Docs (Render):
https://ai-loan-risk.onrender.com/docs

Project Overview

This project demonstrates an end-to-end AI + FinTech architecture:

User enters loan applicant details →
FastAPI backend processes request →
Machine learning model predicts approval →
Results stored in MongoDB Atlas →
React dashboard visualizes analytics.

Features

Loan approval prediction using Machine Learning
Risk scoring and interest rate recommendation
Fraud flag detection based on business rules
Real-time REST API using FastAPI
MongoDB Atlas integration for storing applications
Interactive analytics dashboard with charts
Cloud deployment using Render and Vercel

Tech Stack

Frontend
React
Axios
Recharts
CSS

Backend
FastAPI
Scikit-learn
Motor (MongoDB async driver)
Uvicorn

Machine Learning
Python
Pandas
NumPy
Random Forest Classifier

Database
MongoDB Atlas

Deployment
Render (Backend)
Vercel (Frontend)

Machine Learning Model

Dataset: Loan Prediction Dataset (Kaggle)

Algorithms evaluated:

Logistic Regression

Random Forest

Gradient Boosting

Final model: Random Forest Classifier

Model outputs:

Loan approval probability

Risk score (0–100)

Suggested interest rate

Fraud flag

Natural language explanation

API Endpoints

Base URL
https://ai-loan-risk.onrender.com

POST /api/predict
Predict loan approval and risk

GET /api/applications
Fetch recent loan applications

GET /api/stats
Fetch dashboard analytics

Sample Prediction Request

POST /api/predict

{
  "gender": "Male",
  "married": "Yes",
  "dependents": "0",
  "education": "Graduate",
  "self_employed": "No",
  "applicant_income": 5000,
  "coapplicant_income": 1500,
  "loan_amount": 120,
  "loan_amount_term": 360,
  "credit_history": 1,
  "property_area": "Urban"
}

Local Setup
Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python apps.py

Frontend
cd frontend
npm install
npm start

Deployment

Backend deployed on Render with environment variables:

MONGO_URL

PYTHON_VERSION

Frontend deployed on Vercel with production API URL.
