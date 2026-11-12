from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("welcome.html")


@app.route("/welcome")
def welcome():
    name = request.args.get("name", "")

    html = "<html>"
    html += "Hello " + name
    html += "<p>Nice to meet you..</p>"
    html += "</html>"

    return html


if __name__ == "__main__":
    app.run(debug=True)