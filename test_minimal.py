from flask import Flask
app = Flask(__name__)
app.config['PREFERRED_URL_SCHEME'] = 'http'

@app.route('/minimal')
def minimal():
    return "Minimal test"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)