import os
import pyodbc
from flask import Flask, request, render_template, jsonify
from parser_logic import extract_text_from_pdf, extract_entities
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


def get_db_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=103.207.1.91;"        # Use the IP from your working expense.py
        "DATABASE=CSE9286;"           # Use the DB name from your working expense.py
        "UID=MZCET;"                  # Use 'MZCET' instead of 'sa'
        "PWD=MZCET@1234;"             # Use the verified password
    )
    return pyodbc.connect(conn_str)


@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file = request.files['resume']
        if file:
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            
          
            text = extract_text_from_pdf(path)
            data = extract_entities(text)
            
            
            conn = get_db_connection()
            cur = conn.cursor()
            # Use '?' for SQL Server instead of '%s'
            cur.execute(
                "INSERT INTO candidates (name, email, phone, skills) VALUES (?, ?, ?, ?)",
                (data['name'], data['email'], data['phone'], ",".join(data['skills']))
            )
            conn.commit()
            cur.close()
            conn.close()
            
            return jsonify({"status": "Success", "data": data})
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
