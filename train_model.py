import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pickle
import os

def train_and_save_model():
    print("Loading dataset requiredfinaldataset.csv...")
    try:
        df = pd.read_csv('requiredfinaldataset.csv')
    except FileNotFoundError:
        print("Error: requiredfinaldataset.csv not found.")
        return

    # Map the exact columns from the dataset
    numeric_features = [
        'cgpa', 'backlogs', 'coding_skills', 'dsa_score', 
        'aptitude_score', 'communication_skills', 'ml_knowledge', 
        'system_design', 'internships', 'projects_count', 
        'certifications', 'hackathons', 'open_source_contributions', 
        'extracurriculars'
    ]
    categorical_features = ['branch']
    
    features = categorical_features + numeric_features

    # Handle missing values if any
    for col in numeric_features:
        df[col] = df[col].fillna(0)
        
    df['branch'] = df['branch'].fillna('Unknown')
    df['placement_status'] = df['placement_status'].fillna(0)
    
    X = df[features]
    y = df['placement_status']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Building Preprocessing Pipeline...")
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    print("Training Hist Gradient Boosting Classifier pipeline...")
    # Create a pipeline with the preprocessor and the classifier
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('gb', HistGradientBoostingClassifier(max_iter=150, learning_rate=0.1, random_state=42))
    ])
    
    model.fit(X_train, y_train)
    
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)
    
    print(f"Model Training Accuracy: {train_acc:.4f}")
    print(f"Model Test Accuracy: {test_acc:.4f}")
    
    # Fit on all data for the final model deployment
    model.fit(X, y)
    print(f"Final Model Overall Accuracy: {model.score(X, y):.4f}")
    
    os.makedirs('model', exist_ok=True)
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved to model/model.pkl")

if __name__ == "__main__":
    train_and_save_model()
