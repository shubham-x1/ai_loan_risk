from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import joblib
import numpy as np
from datetime import datetime
from model import LoanApplication, PredictionResponse
import os
from typing import List

app = FastAPI(title="AI Loan Risk API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.loan_risk_db
applications_collection = db.applications

# Load ML model
try:
    model = joblib.load('loan_model.pkl')
    label_encoders = joblib.load('label_encoders.pkl')
    target_encoder = joblib.load('target_encoder.pkl')
    feature_names = joblib.load('feature_names.pkl')
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    model = None

def preprocess_input(application: LoanApplication):
    """Convert input to model format"""
    data = {
        'Gender': application.gender,
        'Married': application.married,
        'Dependents': application.dependents,
        'Education': application.education,
        'Self_Employed': application.self_employed,
        'ApplicantIncome': application.applicant_income,
        'CoapplicantIncome': application.coapplicant_income,
        'LoanAmount': application.loan_amount,
        'Loan_Amount_Term': application.loan_amount_term,
        'Credit_History': application.credit_history,
        'Property_Area': application.property_area,
    }
    
    # Encode categorical variables
    for col, encoder in label_encoders.items():
        try:
            data[col] = encoder.transform([data[col]])[0]
        except:
            data[col] = 0
    
    # Create feature array in correct order
    features = [data[col] for col in feature_names]
    return np.array(features).reshape(1, -1)

def calculate_risk_score(probability: float, application: LoanApplication) -> float:
    """Calculate risk score (0-100)"""
    base_risk = (1 - probability) * 100
    
    # Adjust based on factors
    income_ratio = application.loan_amount / (application.applicant_income / 12)
    if income_ratio > 3:
        base_risk += 10
    
    if application.credit_history < 1.0:
        base_risk += 20
    
    return min(base_risk, 100)

def calculate_interest_rate(risk_score: float, approved: bool) -> float:
    """Calculate suggested interest rate"""
    if not approved:
        return 0.0
    
    base_rate = 8.5
    if risk_score < 20:
        return base_rate
    elif risk_score < 40:
        return base_rate + 1.5
    elif risk_score < 60:
        return base_rate + 3.0
    else:
        return base_rate + 5.0

def detect_fraud(application: LoanApplication) -> bool:
    """Simple fraud detection"""
    # Check for unrealistic values
    if application.applicant_income > 50000:
        return True
    if application.loan_amount > 1000:
        return True
    if application.applicant_income < 1000 and application.loan_amount > 200:
        return True
    return False

def generate_explanation(approved: bool, risk_score: float, application: LoanApplication) -> str:
    """Generate AI explanation"""
    reasons = []
    
    if application.credit_history < 1.0:
        reasons.append("poor credit history")
    
    income_ratio = application.loan_amount / (application.applicant_income / 12)
    if income_ratio > 3:
        reasons.append("high loan-to-income ratio")
    
    total_income = application.applicant_income + application.coapplicant_income
    if total_income < 3000:
        reasons.append("low total income")
    
    if approved:
        if risk_score < 30:
            return f"✅ Application approved with low risk. Applicant shows strong financial profile with good credit history."
        else:
            reason_text = ", ".join(reasons) if reasons else "moderate risk factors"
            return f"✅ Application approved but with elevated risk due to: {reason_text}. Higher interest rate recommended."
    else:
        reason_text = ", ".join(reasons) if reasons else "overall risk assessment"
        return f"❌ Application rejected due to: {reason_text}. Recommend improving credit score and income stability."

@app.get("/")
async def root():
    return {"message": "AI Loan Risk API", "status": "active"}

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_loan(application: LoanApplication):
    """Predict loan approval and risk"""
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Preprocess input
        features = preprocess_input(application)
        
        # Get prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        # Calculate metrics
        approved = bool(prediction == 1)
        approval_prob = float(probability[1])
        risk_score = calculate_risk_score(approval_prob, application)
        interest_rate = calculate_interest_rate(risk_score, approved)
        fraud_flag = detect_fraud(application)
        explanation = generate_explanation(approved, risk_score, application)
        
        # Save to database
        app_data = application.dict()
        app_data.update({
            "approved": approved,
            "approval_probability": approval_prob,
            "risk_score": risk_score,
            "suggested_interest_rate": interest_rate,
            "fraud_flag": fraud_flag,
            "explanation": explanation,
            "timestamp": datetime.utcnow()
        })
        
        result = await applications_collection.insert_one(app_data)
        
        return PredictionResponse(
            approved=approved,
            approval_probability=approval_prob,
            risk_score=risk_score,
            suggested_interest_rate=interest_rate,
            fraud_flag=fraud_flag,
            explanation=explanation,
            application_id=str(result.inserted_id)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applications")
async def get_applications(limit: int = 50):
    """Get recent applications"""
    try:
        cursor = applications_collection.find().sort("timestamp", -1).limit(limit)
        applications = []
        async for doc in cursor:
            doc['_id'] = str(doc['_id'])
            applications.append(doc)
        return applications
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get dashboard statistics"""
    try:
        total = await applications_collection.count_documents({})
        approved = await applications_collection.count_documents({"approved": True})
        rejected = total - approved
        
        # Average risk score
        pipeline = [{"$group": {"_id": None, "avg_risk": {"$avg": "$risk_score"}}}]
        result = await applications_collection.aggregate(pipeline).to_list(1)
        avg_risk = result[0]['avg_risk'] if result else 0
        
        return {
            "total_applications": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": (approved / total * 100) if total > 0 else 0,
            "average_risk_score": avg_risk
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)