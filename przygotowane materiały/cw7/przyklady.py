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
    app.run(debug=False) #/True /w ogóle wywalić
