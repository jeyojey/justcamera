from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello bro</h1>"  # Directly return HTML content


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")  # Allow access from any host
