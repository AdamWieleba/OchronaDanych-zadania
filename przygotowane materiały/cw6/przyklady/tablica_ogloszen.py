from flask import Flask, request, render_template
import json

app = Flask(__name__)

try:
    f = open("/tmp/wall.json", "r")
    wall = json.load(f)
except:
    wall = []


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/wall")
def wall_page():
    user = request.args.get("user", "")
    text = request.args.get("text", "")

    if user == "":
        return render_template("login.html")

    if text != "":
        wall.append((user, text))

        f = open("/tmp/wall.json", "w")
        json.dump(wall, f)

    html = "<html><h2>wall</h2>"

    for post in wall:
        html += post[0] + " - " + post[1] + "<br/>"

    html += "<form action='/wall' method='GET'>"
    html += '<p><input type="text" name="text">'
    html += '<input type="submit" value="comment">'
    html += "<input type='hidden' name='user' value=" + user + ">"
    html += "</form>"
    html += '<p><a href="/">Exit</a></p>'

    html += "</html>"

    return html


if __name__ == "__main__":
    app.run(debug=True)