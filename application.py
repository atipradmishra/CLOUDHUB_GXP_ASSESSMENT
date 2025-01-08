from flask import Flask, flash, redirect, render_template, request, session, url_for
import pandas as pd

app = Flask(__name__)

application = app

app.secret_key = '80e9676c95d1a5c82f458a528ab484a7'

USERNAME = 'CloudHub'
PASSWORD = 'cloudhub@2020'

file_path = "Change Impact Assessment.xlsx"


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Route for serving the home page (index.html)
@app.route('/home')
def home():
    return render_template('home.html')

# Route for serving CIA.html when clicked
@app.route('/CIA.html', methods=['GET', 'POST'])
def cia():

    if request.method == 'POST':
        responses = request.form.to_dict()
        total_questions = len(responses)
        
        yes_count = sum(1 for response in responses.values() if response == "Yes")

        yes_percentage = (yes_count / total_questions) * 100

        classification = "Major Changes" if yes_percentage > 40 else "Minor Changes"

        df = pd.read_excel(file_path,sheet_name='CLASSIFICATION')
        

        matched_classification = df[(df['CLASSIFICATION'] == classification)]['Impact Classification Criteria']

        return render_template('results.html', app_name=responses['app_name'], classification=classification, matched_classification=matched_classification)

    df = pd.read_excel(file_path, engine='openpyxl')

    grouped_data = df.groupby('Impact')['Questions'].apply(list).to_dict()

    return render_template('CIA.html',grouped_data=grouped_data)

@app.route('/aws-controls')
def aws_controls():
    app_name = request.args.get('app_name')
    df = pd.read_excel(file_path,sheet_name='aws',engine='openpyxl')
    table_data = df.to_dict(orient='records')
    columns = df.columns.tolist()
    return render_template('aws_controls.html', table_data=table_data, app_name=app_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
