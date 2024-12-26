from flask import Flask, request, jsonify
import pandas as pd
from data_cleaning import clean_data, detect_duplicates

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        df = pd.read_csv(file)

        # Clean the data
        df_cleaned = clean_data(df)
        
        # Detect duplicates
        duplicates = detect_duplicates(df_cleaned)

        return jsonify({
            "cleaned_data": df_cleaned.to_dict(orient="records"),
            "potential_duplicates": duplicates
        })

    return '''
    <form method="post" enctype="multipart/form-data">
        Upload CSV File: <input type="file" name="file">
        <input type="submit">
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)