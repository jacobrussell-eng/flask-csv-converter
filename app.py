from flask import Flask, render_template
import pandas as pd

app = Flask(__name__) 

# Read the data from the sample csv file:
df = pd.read_csv('sample.csv') 
df.to_csv('sample.csv', index=None)

# Route url:
@app.route('/') 
@app.route('/table')

def table(): 
    # Convert csv to html:
    data = pd.read_csv('sample.csv') 
    return render_template('table.html', tables=[data.to_html()], titles=['']) 
  
# Run locally:
if __name__ == "__main__": 
    app.run(host="localhost", port=int("8000"))