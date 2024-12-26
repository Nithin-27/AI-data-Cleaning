import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Function to predict missing dates of birth
def predict_missing_dob(df):
    # Filter rows with non-missing DOB
    df_with_dob = df.dropna(subset=['Date of Birth'])
    
    # Encode names into numerical values for modeling
    df_with_dob['Name_Encoded'] = df_with_dob['First Name'].factorize()[0] + df_with_dob['Last Name'].factorize()[0]
    
    # Features and target
    X = df_with_dob[['Name_Encoded']]
    y = pd.to_datetime(df_with_dob['Date of Birth']).astype(int) // 10**9  # Convert to UNIX timestamp

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Predict missing DOB
    df_missing_dob = df[df['Date of Birth'].isna()]
    df_missing_dob['Name_Encoded'] = df_missing_dob['First Name'].factorize()[0] + df_missing_dob['Last Name'].factorize()[0]
    df_missing_dob['Predicted_DOB'] = model.predict(df_missing_dob[['Name_Encoded']])
    df_missing_dob['Predicted_DOB'] = pd.to_datetime(df_missing_dob['Predicted_DOB'], unit='s')
    return df_missing_dob[['First Name', 'Last Name', 'Predicted_DOB']]

# Example usage
if __name__ == "__main__":
    df = pd.read_csv("cleaned_crm_data.csv")
    predictions = predict_missing_dob(df)
    print("Predicted Missing DOBs:", predictions)