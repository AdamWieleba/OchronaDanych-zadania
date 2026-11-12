from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/zaloguj", methods=["POST"])
def zaloguj():
    haslo = request.form.get("haslo")
    if haslo == "tajne haslo":
        return "Zalogowany OK"
    else:
        return "Niepoprawne hasło"

@app.route("/")
def aboutme():
    return """
    <html>
    <head>
        <title>Moja strona</title>
    </head>
    <body>
        <h1>witaj <b>świecie</b></h1>
        <p>This is a simple Flask app.</p>
    </body>
    <form action="/zaloguj" method="POST">
        <label for="haslo">Hasło:</label>
        <input type="text" name="haslo">
        <input type="submit" name="submit" value="Zaloguj">
    </form>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
