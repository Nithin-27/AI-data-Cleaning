import pandas as pd
import re
from fuzzywuzzy import fuzz


# Function to clean data
def clean_data(df):
    # Standardize text to lowercase
    if 'First Name' in df.columns:
        df['First Name'] = df['First Name'].str.lower()
    else:
        print("Column 'First Name' is missing.")
    
    if 'Last Name (Surname)' in df.columns:
        df['Last Name (Surname)'] = df['Last Name (Surname)'].str.lower()
    else:
        print("Column 'Last Name (Surname)' is missing.")
    
    if 'Email Address' in df.columns:
        df['Email Address'] = df['Email Address'].str.lower()
    else:
        print("Column 'Email Address' is missing.")
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Validate email addresses
    if 'Email Address' in df.columns:
        df['Valid_Email_Address'] = df['Email Address'].apply(validate_email_address)
    else:
        df['Valid_Email_Address'] = False
    
    return df

# Function to validate email addresses
def validate_email_address(email):
    pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    return bool(re.match(pattern, email))

# Function to detect duplicates using fuzzy matching
def detect_duplicates(df):
    if not {'First Name', 'Last Name (Surname)'}.issubset(df.columns):
        print("Cannot detect duplicates. Missing 'First Name' or 'Last Name (Surname)' columns.")
        return []
    
    similar_names = []
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            name1 = f"{df['First Name'].iloc[i]} {df['Last Name (Surname)'].iloc[i]}"
            name2 = f"{df['First Name'].iloc[j]} {df['Last Name (Surname)'].iloc[j]}"
            if fuzz.ratio(name1, name2) > 85:  # Similarity threshold
                similar_names.append((name1, name2))
    return similar_names

# Example usage
if __name__ == "__main__":
    try:
        # Load the dataset
        df = pd.read_csv(r"C:/Users/nithi/Desktop/CSV files/Data.csv")
        print("Columns in the dataset:", df.columns)
        
        # Clean the data
        df_cleaned = clean_data(df)
        
        # Detect duplicates
        duplicates = detect_duplicates(df_cleaned)
        print("Potential Duplicates:", duplicates)
        
        # Save cleaned data
        df_cleaned.to_csv("cleaned_crm_data.csv", index=False)
        print("Cleaned data saved to 'cleaned_crm_data.csv'.")
    except FileNotFoundError:
        print("Error: The file was not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")
