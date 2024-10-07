import os
import uuid
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, Response, send_from_directory, jsonify

app = Flask (__name__, template_folder = 'templates', static_folder='static', static_url_path='/')

# The function that returns a simple "Home" message
# @app.route('/home')
# def home():
#      return "Home"

# @app.route('/greet/<name>')
# def greet(name):
#      return f"Hello {name}"

# # The function that returns the result of adding two numbers together when the user visits a URL like /add/2/3 or /add/4/5.
# @app.route('/add/<int:number1>/<int:number2>')
# def add(number1, number2):
#      return f"The sum of {number1} + {number2} = {number1 + number2}"

# @app.route('/handle_method', methods = ['GET', 'POST'])
# def handle_methods()     :
#      if request.method == 'GET':
#           return 'You made a GET request'
#      elif request.method == 'POST':
#           return "You made a POST request"
#      else:
#           return "Invalid request method"
     

# def handle_params():
#      if 'greeting' in request.args.keys() and 'name' in request.args.keys():
#           greeting = request.args['greeting']
#           name = request.args.get('name')
#           return f"{greeting}, {name}"
#      else:
#           return "Some parameters are missing"

@app.route('/', methods = ['GET', 'POST'])
def index():
     if request.method == 'GET':
          return render_template('index.html')
     elif request.method == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')

          if username == 'Mengleap' and password == '123':
               return 'Login successfully'
          else:
               return 'Login failed'
          
@app.route('/file_upload', methods = ['POST'])
def file_upload():
     file = request.files.get('file')

     if file.content_type == 'text/plain':
          return file.read().decode()
     elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel': 
          df = pd.read_excel(file)
          return df.to_html()
        

@app.route('/convert_csv', methods = ['POST'])
def convert_csv():
     file = request.files['file']

     df = pd.read_excel(file)

     response = Response(
          df.to_csv(),
          mimetype = 'text/csv',
          headers = {
               'Content-disposition': 'attachment; filename="output.csv"'
          }
     )
     return response


@app.route('/convert_csv_two', methods = ['POST'])
def convert_csv_two():
     file = request.files['file']

     df = pd.read_excel(file)

     if not os.path.exists('downloads'):
          os.makedirs('downloads')

     filename = f'{uuid.uuid4()}.csv'
     df.to_csv(os.path.join('downloads', filename))

     return render_template('download.html', filename = filename)


@app.route('/download/<filename>')
def download(filename):
     return send_from_directory('downloads', filename, download_name = 'result.csv')

@app.route('/other')
def other():
     some_text = 'Hello Guys'
     return render_template('other.html', some_text = some_text)
     
@app.route('/home_page')
def home_page():
     mylist = [10, 20, 30, 40, 50]
     return render_template('index.html', mylists = mylist)

# Create our own filter
@app.template_filter('reverse_string') #Reverse
def reverse_string(s):
     return s[::-1]

@app.template_filter('repeat') #Repeat
def repeat(s, times = 3):
     return s * times

@app.template_filter('alternate_case') #alternate_case
def alternate_case(s):
     return ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s)])

# Redirect endpoint
@app.route('/redirect_endpoint')
def redirect_endpoint():
     return redirect(url_for('other'))

@app.route('/handle_post', methods = ['POST'])
def handle_post():
     greeting = request.json['greeting']
     name = request.json['name']

     with open('file.txt', 'w') as f:
          f.write(f'{greeting}, {name}')

     return jsonify({'message': 'Successfully written!'})

             
if __name__ == '__main__':
     app.run (host = '0.0.0.0', port=5555, debug=True)