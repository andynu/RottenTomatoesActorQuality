from flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
  return 'hello World!'

if __name__ == '__main__':
  #app.run() # localhost only
  app.run(host='0.0.0.0') # listen externally