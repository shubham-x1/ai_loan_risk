import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

def train_model():
    print("📊 Loading real loan dataset...")
    
    df = pd.read_csv('train.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Handle missing values
    print("🔧 Cleaning data...")
    df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)
    df['Married'].fillna(df['Married'].mode()[0], inplace=True)
    df['Dependents'].fillna(df['Dependents'].mode()[0], inplace=True)
    df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace=True)
    df['LoanAmount'].fillna(df['LoanAmount'].median(), inplace=True)
    df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0], inplace=True)
    df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace=True)
    
    # Drop Loan_ID (not a feature)
    df = df.drop('Loan_ID', axis=1)
    
    print("🔧 Encoding categorical variables...")
    # Encode categorical variables
    label_encoders = {}
    categorical_cols = ['Gender', 'Married', 'Dependents', 'Education', 
                       'Self_Employed', 'Property_Area']
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Prepare features and target
    X = df.drop('Loan_Status', axis=1)
    y = df['Loan_Status']
    
    # Encode target
    le_target = LabelEncoder()
    y = le_target.fit_transform(y)
    
    print(f"Target distribution: {np.bincount(y)}")
    print(f"Approval rate: {(y == 1).mean():.2%}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("🤖 Training Random Forest model...")
    # Train model with class balancing
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight='balanced',  # Handle imbalance
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"\n{'='*50}")
    print(f"✅ Training Accuracy: {train_score:.2%}")
    print(f"✅ Testing Accuracy: {test_score:.2%}")
    print(f"{'='*50}\n")
    
    # Detailed metrics
    y_pred = model.predict(X_test)
    print("📊 Classification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=['Rejected', 'Approved']))
    
    print("\n📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Feature importance
    print("\n📊 Top 5 Most Important Features:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    print(feature_importance.head())
    
    # Save model and encoders
    joblib.dump(model, 'loan_model.pkl')
    joblib.dump(label_encoders, 'label_encoders.pkl')
    joblib.dump(le_target, 'target_encoder.pkl')
    joblib.dump(list(X.columns), 'feature_names.pkl')
    
    print("\n💾 Model saved successfully!")
    print(f"Model file size: {os.path.getsize('loan_model.pkl') / 1024:.2f} KB")
    
    return model

if __name__ == "__main__":
    train_model()