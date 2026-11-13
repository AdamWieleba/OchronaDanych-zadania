from flask import Flask, render_template, request, make_response
from markupsafe import escape

app = Flask(__name__)

# Strona główna
@app.route("/")
def index():
    return render_template("welcome2.html")


# Odczyt argumentu GET
@app.route("/welcome2")
def welcome2():
    name = request.args.get("name", "")

    # Zabezpieczenie przed XSS
    html = "<html><body>"
    html += "<h1>Hello " + str(escape(name)) + "</h1>"
    html += "<p>Nice to meet you!</p>"
    html += "</body></html>"

    return html


# Ustawianie ciasteczka
@app.route("/set_cookie")
def set_cookie():
    response = make_response("Cookie zapisane!")
    response.set_cookie(
        "username",
        "student",
        httponly=True,
        secure=False,
        samesite="Lax"
    )
    return response


# Odczyt ciasteczka po stronie serwera
@app.route("/get_cookie")
def get_cookie():
    username = request.cookies.get("username", "Brak ciasteczka")
    return f"Zapisana wartość: {escape(username)}"


# Przykładowa tajna notatka
@app.route("/note")
def note():
    return """
    <div id="secret-note">
        To jest przykładowa tajna notatka.
    </div>
    """


if __name__ == "__main__":
    app.run(debug=True)
