# Bezpieczne zapytanie SQL
import sqlite3
import re

# Utworzenie bazy w pamięci
db = sqlite3.connect(":memory:")

db.execute("""
    CREATE TABLE osoby (
        id INTEGER,
        nazwa TEXT
    )
""")

db.execute(
    "INSERT INTO osoby VALUES (?, ?)",
    (1, "O'Neil")
)

wynik = db.execute(
    "SELECT id, nazwa FROM osoby WHERE nazwa = ?",
    ("O'Neil",)
).fetchall()

print(wynik)

# Walidacja danych
print(bool(re.fullmatch(r'[0-9]+', '123')))
print(bool(re.fullmatch(r'[0-9]+', '12x')))

db.close()




# Zapytanie SQL z parametrem
import sqlite3

db = sqlite3.connect(":memory:")

db.execute("CREATE TABLE osoby (id INTEGER, nazwa TEXT)")

db.execute(
    "INSERT INTO osoby VALUES (?, ?)",
    (1, "O'Neil")
)

wynik = db.execute(
    "SELECT id, nazwa FROM osoby WHERE nazwa = ?",
    ("O'Neil",)
).fetchall()

print(wynik)



# Bezpieczne wybieranie tabeli
dozwolone_tabele = ["osoby", "pracownicy"]

wybrana = "osoby"

if wybrana not in dozwolone_tabele:
    raise ValueError("Niedozwolona tabela")

zapytanie = f"SELECT * FROM {wybrana}"



# re.fullmatch
import re

wyrazenie = "123"

if re.fullmatch(r"[0-9]+", wyrazenie):
    liczba = int(wyrazenie)
    print(liczba)
else:
    print("Niepoprawne dane")



# http://localhost:5000/szukaj?q=Jan
from flask import Flask, request

app = Flask(__name__)

@app.route("/szukaj")
def szukaj():
    q = request.args.get("q")
    return q




# 400 Bad Request
from flask import Flask, request

app = Flask(__name__)

@app.route("/liczba")
def liczba():
    wartosc = request.args.get("n")

    if wartosc is None or not wartosc.isdigit():
        return "Nieprawidłowe dane", 400

    return "Poprawne dane"


# app.logger
try:
    wynik = 10 / 0
except Exception:
    app.logger.exception("Wystąpił błąd")
    return "Wystąpił błąd serwera", 500




### Część 2 - Code injection

# Niebezpieczny kalkulator
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    expr = request.args.get("expr", "0")

    namespace = {}

    html = "<html><body>"
    html += "<h3>Kalkulator</h3>"

    try:
        # CELOWO PODATNY KOD
        exec("result = " + expr, namespace)

        html += "Wynik: "
        html += str(namespace["result"])

    except Exception:
        html += "Wystąpił błąd"

    html += "</body></html>"

    return html


if __name__ == "__main__":
    app.run(debug=False)

"""
mkdir testowy
touch testowy/plik1.txt
touch testowy/plik2.txt

curl -G --data-urlencode "expr=__import__('os').listdir('testowy')" http://127.0.0.1:5000/
curl -G --data-urlencode "expr=__import__('platform').platform()" http://127.0.0.1:5000/
curl -G --data-urlencode "expr=__import__('os').getuid()" http://127.0.0.1:5000/
"""


# Bezpieczny kalkulator
from flask import Flask, request
import re

app = Flask(__name__)

@app.route("/")
def index():
    expr = request.args.get("expr", "0")

    try:
        if not re.fullmatch(r"[0-9+\-*/(). ]+", expr):
            raise ValueError("Nieprawidłowe dane")

        result = eval(expr)

        return f"Wynik: {result}"

    except Exception:
        app.logger.exception("Błąd podczas obliczania wyrażenia")
        return "Nieprawidłowe dane", 400


if __name__ == "__main__":
    app.run(debug=False)


# Tworzenie bazy danych (trwałej), 
# python create_db.py:
import sqlite3

db = sqlite3.connect("secrets.db")

cur = db.cursor()

cur.execute("""
    CREATE TABLE secrets (
        key TEXT,
        secret TEXT
    )
""")

cur.execute(
    "INSERT INTO secrets VALUES (?, ?)",
    ("1234", "Hello world")
)

cur.execute(
    "INSERT INTO secrets VALUES (?, ?)",
    ("qwerty", "Top secret")
)

db.commit()
db.close()

print("Baza danych została utworzona.")


# mkdir templates
# templates/sql_secrets.html
"""
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>SQL Secrets</title>
</head>
<body>

    <h3>SQL Secrets</h3>

    <form action="/sql_secrets" method="GET">
        Enter key:
        <input type="text" name="key" size="50">
        <input type="submit" value="Get secret">
    </form>

</body>
</html>
"""


# Podatny SQL, python sql_secrets.py:
import sqlite3

from flask import Flask, request, render_template_string

app = Flask(__name__)

DBFILE = "secrets.db"


@app.route("/")
def index():
    return """
    <h3>SQL Secrets</h3>

    <form action="/sql_secrets" method="GET">
        Enter key:
        <input type="text" name="key" size="50">
        <input type="submit" value="Get secret">
    </form>
    """


@app.route("/sql_secrets")
def sql_secrets():

    key = request.args.get("key", "")

    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()

    html = "<html><body>"

    html += f"Key: {key}<br>"

    # CELOWO PODATNE ZAPYTANIE, np. dla key:
    #     ' OR '1'='1' -- 
    #     SELECT * FROM secrets WHERE key='' OR '1'='1' --'
    # zwróci wszystkie rekordy z tabeli secrets
    query = f"SELECT * FROM secrets WHERE key='{key}'"

    try:
        for row in cursor.execute(query):
            html += f"Secret: {row[1]}<br>"

    except sqlite3.Error:
        html += "Wystąpił błąd SQL"

    conn.close()

    html += "</body></html>"

    return html


if __name__ == "__main__":
    app.run(debug=False)

"""
python create_db.py
python sql_secrets.py

Atak przez injection:
curl -G --data-urlencode "key=' OR '1'='1' -- " http://127.0.0.1:5000/sql_secrets
(może ' UNION SELECT * FROM secrets -- też by zadziałało)

Poprawny klucz:
curl -G --data-urlencode "key=1234" http://127.0.0.1:5000/sql_secrets


Do sql injection można użyć', OR, --, UNION.
"""


# Bezpieczny SQL, python sql_secrets_safe.py:
import sqlite3

from flask import Flask, request, render_template_string

app = Flask(__name__)

DBFILE = "secrets.db"


@app.route("/")
def index():
    return """
    <h3>SQL Secrets</h3>

    <form action="/sql_secrets" method="GET">
        Enter key:
        <input type="text" name="key" size="50">
        <input type="submit" value="Get secret">
    </form>
    """


@app.route("/sql_secrets")
def sql_secrets():

    key = request.args.get("key", "")

    if not key or len(key) > 50:
        return "Nieprawidłowe dane", 400

    conn = sqlite3.connect(DBFILE)

    try:
        cursor = conn.cursor()

        # BEZPIECZNE ZAPYTANIE PARAMETRYZOWANE
        cursor.execute(
            "SELECT secret FROM secrets WHERE key = ?",
            (key,)
        )

        results = cursor.fetchall()

        if not results:
            return "Nie znaleziono sekretu", 404

        secrets = "".join(
            f"<p>Secret: {row[0]}</p>"
            for row in results
        )

        return secrets

    except sqlite3.Error:
        app.logger.exception("Błąd bazy danych")
        return "Wystąpił błąd serwera", 500

    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=False)

