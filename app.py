from flask import (Flask, jsonify, render_template, render_template_string,
                   request)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/submit', methods=['POST'])
def submit():
    print("here, you submmited something")
    name = request.form.get('name')
    if name:
        response_html = f'<p>Hello, {name}!</p>'
    else:
        response_html = '<p>Please enter your name.</p>'
      
    return render_template_string(response_html)

if __name__ == '__main__':
    app.run(debug=True)

