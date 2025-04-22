from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__) 
CSV_FOLDER = 'CSVs'

# Fetch csv files from directory:
def get_csv_files():
    files = [f for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]
    return files

# Read the data from the sample csv file:
def csv_to_html(csv_filepath):
    try:
        df = pd.read_csv(csv_filepath)
        return df.to_html(index=False)
    except FileNotFoundError:
        return "<p>Error: CSV file not found.</p>"
    except Exception as e:
        return f"<p>Error reading CSV file: {e}</p>"

# Route url:
@app.route('/', methods=['GET','POST'])
def index(): 
    csv_files = get_csv_files()
    selected_file = None
    html_table = None
    uploaded_file = False
    selected_source = request.form.get('csv_source', '')

    if request.method == 'POST':
        selected_source = request.form.get('csv_source', '')
        # Handle file upload:
        if selected_source == 'upload':
            if 'file' in request.files:
                file = request.files['file']
                if file.filename != '' and file.filename.endswith('.csv'):
                    html_table = csv_to_html(file)  # Pass the file buffer directly
                    uploaded_file = True
                else:
                    html_table = "<p>Error: Please upload a valid CSV file.</p>"
            else:
                html_table = "<p>Error: No file part in the request.</p>"
        
        # Handle selection from the server:
        else:
            selected_file = request.form['csv_source']
            csv_filepath = os.path.join(CSV_FOLDER, selected_file)
            html_table = csv_to_html(csv_filepath)
    
    return render_template('table.html', tables=[html_table], titles=[''], csv_files=csv_files, selected_file=selected_file, uploaded_file=uploaded_file) 
  
# Run locally:
if __name__ == "__main__": 
    app.run(debug=True, host="localhost", port=int("8000"))