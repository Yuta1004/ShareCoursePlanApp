from flask import Flask


app = Flask(__name__)
app.config["SECRET_KEY"] = "db1app"
app.config["MAX_CONTENT_LENGTH"] = 4*1024*1024


@app.route("/")
def top():
    return "Hello"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000)
