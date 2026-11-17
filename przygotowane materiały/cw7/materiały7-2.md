# Code Injection i SQL Injection – ćwiczenia z wykorzystaniem Flask

## 1. Cel zajęć

Celem zajęć jest zapoznanie się z metodami ataków na aplikacje internetowe, polegającymi na wstrzyknięciu kodu zmieniającego działanie aplikacji na serwerze.

Omówione zostaną dwa rodzaje podatności:

- **Code Injection** – wstrzyknięcie kodu, który zostanie wykonany przez interpreter Pythona.
- **SQL Injection** – wstrzyknięcie fragmentu SQL, który zmienia działanie zapytania do bazy danych.

Wszystkie ćwiczenia wykonujemy lokalnie, na własnym komputerze.

---

# 2. Flask

```bash
python -m pip install flask
```

Sprawdzenie instalacji:

```bash
python -m flask --version
```

## 2.2. Przygotowanie katalogu projektu

Utwórz katalog:

```bash
mkdir flask_security
cd flask_security
```

Wszystkie poniższe pliki będziemy umieszczać w katalogu `flask_security`.

## 2.3. Jak działa Flask?

Przykład:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    expr = request.args.get("expr", "0")
    return expr

if __name__ == "__main__":
    app.run()
```

Wyjaśnienie:

| Element | Znaczenie |
|---|---|
| `Flask(__name__)` | Tworzy aplikację Flask |
| `@app.route("/")` | Definiuje adres, pod którym działa funkcja |
| `request.args` | Pobiera parametry z adresu URL |
| `.get("expr", "0")` | Pobiera parametr expr, domyślnie 0 |
| `return` | Zwraca odpowiedź do przeglądarki |
| `app.run()` | Uruchamia serwer Flask |

Przykładowy adres:

```text
http://127.0.0.1:5000/?expr=123
```

Flask pobierze wartość:

```python
expr = "123"
```

---

# 3. Code Injection - wykonywanie kodu dostarczonego przez użytkownika

Stworzymy prostą aplikację kalkulatora.

Utwórz plik:

```text
calc.py
```

Celowo podatna wersja aplikacji:

```python
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
```

### Co robi program?

1. Pobiera parametr `expr` z adresu URL.
2. Jeśli parametr nie został podany, przyjmuje wartość `0`.
3. Tworzy przestrzeń nazw `namespace`.
4. Wykonuje kod za pomocą `exec()`.
5. Odczytuje wynik.
6. Wyświetla go w przeglądarce.

Linia powodująca podatność:

```python
exec("result = " + expr, namespace)
```

Aplikacja nie sprawdza, czy użytkownik przekazał zwykłe działanie matematyczne, czy kod Pythona.

## 3.3. Uruchomienie kalkulatora

W terminalu:

```bash
python calc.py
```

Aplikacja będzie dostępna pod adresem:

```text
http://127.0.0.1:5000
```

## 3.4. Testowanie kalkulatora

Użyj curl w terminalu:

```bash
curl -G --data-urlencode "expr=2+3" http://127.0.0.1:5000/
```

Albo wpisz w przeglądarce:

```text
http://127.0.0.1:5000/?expr=2%2B3
```

Wynik:

```text
Wynik: 5
```


### Aplikacja jest podatna 

Użytkownik kontroluje zawartość zmiennej `expr`, przekazywanej do `exec()`

Interpreter nie rozróżnia zwykłego działania matematycznego od instrukcji Pythona.

## 3.5. Demonstracja możliwości podatności


Przykładowo możemy odczytać identyfikator użytkownika procesu na Linuxie:

```bash
curl -G --data-urlencode "expr=__import__('os').getuid()" http://127.0.0.1:5000/
```

Możemy też przygotować własny katalog i sprawdzić jego zawartość przez aplikację:

```bash
mkdir testowy
touch testowy/plik1.txt
touch testowy/plik2.txt
```


```bash
curl -G --data-urlencode "expr=__import__('os').listdir('testowy')" http://127.0.0.1:5000/
```

Wynik będzie zawierał nazwy utworzonych plików.

#### Funkcja `os.listdir()` pozwala poznawać strukturę katalogów dostępnych dla procesu aplikacji.

#### Podobnie nieograniczony dostęp do `open()` może umożliwiać odczytywanie plików, do których aplikacja ma uprawnienia.

---

## 3.6. Zadanie 1 – Code Injection

### Polecenie

Przeprowadź testy podatności kalkulatora. Celem jest:

1. Wyświetlenie zawartości katalogu testowego na serwerze.
2. Rozpoznanie nazwy i wersji systemu operacyjnego.
3. Sprawdzenie, jakie uprawnienia posiada proces aplikacji.
4. Zaproponowanie modyfikacji programu blokującej Code Injection.

### Rozwiązanie krok po kroku

**Krok 1. Przygotuj katalog testowy**

```bash
mkdir -p testowy
touch testowy/dokument.txt
touch testowy/notatki.txt
```

**Krok 2. Sprawdź zawartość katalogu**

```bash
curl -G --data-urlencode "expr=__import__('os').listdir('testowy')" http://127.0.0.1:5000/
```

Oczekiwany rezultat:

```text
Wynik: ['dokument.txt', 'notatki.txt']
```

**Krok 3. Sprawdź system operacyjny**

```bash
curl -G --data-urlencode "expr=__import__('platform').system()" http://127.0.0.1:5000/
```

Przykładowy wynik:

```text
Wynik: Linux
```

Aby uzyskać dokładniejsze informacje:

```bash
curl -G --data-urlencode "expr=__import__('platform').platform()" http://127.0.0.1:5000/
```

**Krok 4. Sprawdź uprawnienia procesu**

```bash
curl -G --data-urlencode "expr=__import__('os').getuid()" http://127.0.0.1:5000/
```

Otrzymana wartość to UID użytkownika uruchamiającego aplikację.

---

# 4. Naprawa podatności Code Injection

Najważniejszym rozwiązaniem jest całkowite usunięcie `exec()` i `eval()` z obsługi danych użytkownika.

Zamiast wykonywać kod Pythona, możemy:
1. sprawdzić poprawność danych,
2. dopuścić tylko określony format,
3. samodzielnie wykonać dozwolone działania matematyczne.

## 4.1. Bezpieczny kalkulator – wersja Flask

Utwórz plik:

```text
calc_safe.py
```

Wklej:

```python
from flask import Flask, request
import re
import ast
import operator

app = Flask(__name__)

# Dozwolone operacje
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def calculate(expression):
    if not expression or len(expression) > 100:
        raise ValueError("Niepoprawne wyrażenie")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        elif isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Niedozwolona wartość")
            if abs(node.value) > 10**12:
                raise ValueError("Liczba jest za duża")
            return node.value

        elif isinstance(node, ast.BinOp):
            operation = OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Niedozwolony operator")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Dzielenie przez zero")

            result = operation(left, right)

            if abs(result) > 10**12:
                raise ValueError("Wynik jest za duży")

            return result

        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -evaluate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return evaluate(node.operand)

        raise ValueError("Niedozwolone wyrażenie")

    return evaluate(tree)


@app.route("/")
def index():
    expr = request.args.get("expr", "0")

    try:
        result = calculate(expr)
        return f"<h3>Wynik: {result}</h3>"

    except (ValueError, SyntaxError, ZeroDivisionError):
        return "Nieprawidłowe wyrażenie", 400


if __name__ == "__main__":
    app.run(debug=False)
```

### Co zostało zmienione?

| Podatna wersja | Bezpieczna wersja |
|---|---|
| `exec()` | Usunięte |
| Dowolny kod Pythona | Tylko określone operacje matematyczne |
| Brak ograniczeń | Ograniczenie długości wyrażenia |
| Dowolne funkcje | Tylko operatory z listy |
| Brak obsługi dzielenia przez zero | Jawna kontrola |
| Dowolne wartości | Tylko liczby całkowite i zmiennoprzecinkowe |

### Dlaczego wykorzystujemy ast?

Moduł `ast` pozwala analizować strukturę wyrażenia Pythona bez wykonywania go jako dowolnego kodu.

Program sprawdza, czy występują tylko dozwolone elementy.

Nie wykonuje funkcji takich jak `open()`, `__import__()` czy `os.listdir()`.

## 4.2. Uruchomienie bezpiecznego kalkulatora

```bash
python calc_safe.py
```

Test poprawnego działania:

```bash
curl -G --data-urlencode "expr=10+5*2" http://127.0.0.1:5000/
```

Wynik:

```text
Wynik: 20
```

Test dzielenia przez zero:

```bash
curl -G --data-urlencode "expr=10/0" http://127.0.0.1:5000/
```

Oczekiwany kod HTTP:

```text
400
```

Test niedozwolonego wyrażenia:

```bash
curl -G --data-urlencode "expr=__import__('os')" http://127.0.0.1:5000/
```

Oczekiwany wynik:

```text
Nieprawidłowe wyrażenie
```

**Wniosek:** Bezpieczny kalkulator powinien interpretować tylko jawnie dozwolone operacje, a nie wykonywać dowolny kod użytkownika.

---

# 5. Ćwiczenie drugie – SQL Injection

## 5.1. Na czym polega SQL Injection?

SQL Injection to podatność polegająca na wstrzyknięciu fragmentu kodu SQL do zapytania wykonywanego przez aplikację.

W tym ćwiczeniu stworzymy prosty system przechowujący sekrety w bazie SQLite.

Użytkownik podaje klucz, a aplikacja zwraca przypisany do niego sekret.

Problem wystąpi, jeżeli aplikacja będzie bezpośrednio doklejała dane użytkownika do zapytania SQL.

## 5.2. Tworzenie bazy danych

Utwórz plik:

```text
create_db.py
```

Wklej:

```python
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
```

### Co robi kod?

1. Importuje moduł `sqlite3`.
2. Łączy się z bazą `secrets.db`.
3. Tworzy tabelę `secrets`.
4. Dodaje dwa przykładowe rekordy.
5. Zapisuje zmiany przez `commit()`.
6. Zamyka połączenie.

Struktura tabeli:

| key | secret |
|---|---|
| 1234 | Hello world |
| qwerty | Top secret |

Uruchom:

```bash
python create_db.py
```

Powinien powstać plik:

```text
secrets.db
```

---

# 6. Formularz HTML – SQL Secrets

We Flasku możemy umieścić formularz bezpośrednio w kodzie Pythona albo w osobnym pliku HTML.

W tym przykładzie wykorzystamy osobny plik.

Utwórz katalog:

```bash
mkdir templates
```

W nim utwórz plik:

```text
templates/sql_secrets.html
```

Wklej:

```html
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
```

### Wyjaśnienie formularza

| Element | Znaczenie |
|---|---|
| `form` | Tworzy formularz |
| `action="/sql_secrets"` | Określa adres obsługujący formularz |
| `method="GET"` | Wysyła dane jako GET |
| `name="key"` | Nazwa parametru |
| `input type="text"` | Pole tekstowe |
| `submit` | Przycisk wysyłający formularz |

Po wysłaniu formularza adres będzie wyglądał przykładowo tak:

```text
http://127.0.0.1:5000/sql_secrets?key=1234
```

---

# 7. Podatna aplikacja SQL Secrets – Flask

Utwórz plik:

```text
sql_secrets.py
```

Wklej:

```python
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

    # CELOWO PODATNE ZAPYTANIE
    query = "SELECT * FROM secrets WHERE key='%s'" % key

    try:
        for row in cursor.execute(query):
            html += "Secret: %s<br>" % row[1]

    except sqlite3.Error:
        html += "Wystąpił błąd SQL"

    conn.close()

    html += "</body></html>"

    return html


if __name__ == "__main__":
    app.run(debug=False)
```

**Uwaga:** Jest to wersja celowo podatna na SQL Injection. Wykorzystujemy ją wyłącznie w lokalnym laboratorium.

## 7.1. Jak działa aplikacja?

Najważniejsza linia:

```python
key = request.args.get("key", "")
```

Pobiera wartość parametru `key` z adresu URL.

Następnie:

```python
query = "SELECT * FROM secrets WHERE key='%s'" % key
```

Tworzy zapytanie SQL przez wstawienie wartości użytkownika bezpośrednio do tekstu zapytania.

To właśnie jest przyczyna podatności.

Prawidłowe zapytanie powinno wyglądać następująco:

```sql
SELECT * FROM secrets WHERE key = ?
```

Wartość powinna być przekazywana osobno.

## 7.2. Uruchomienie aplikacji

Najpierw upewnij się, że wykonałeś:

```bash
python create_db.py
```

Następnie uruchom:

```bash
python sql_secrets.py
```

Otwórz:

```text
http://127.0.0.1:5000/
```

Wpisz:

```text
1234
```

Wynik:

```text
Key: 1234
Secret: Hello world
```

Spróbuj również:

```text
qwerty
```

Wynik:

```text
Key: qwerty
Secret: Top secret
```

---

# 8. Demonstracja SQL Injection

## 8.1. Dlaczego podatność istnieje?

Aplikacja buduje zapytanie SQL przez łączenie tekstu i danych użytkownika.

Oryginalne zapytanie dla klucza `1234`:

```sql
SELECT * FROM secrets WHERE key='1234'
```

Wartość `key` wpływa bezpośrednio na strukturę zapytania.

W SQL istotne znaczenie mają:
- apostrofy `'`,
- operator `OR`,
- komentarz `--`,
- operator `UNION`.

Nieprawidłowe budowanie zapytań może pozwolić na zmianę warunków wyszukiwania.

## 8.2. Operator OR

Operator `OR` oznacza alternatywę logiczną.

Przykład:

```sql
SELECT * FROM secrets
WHERE key = '1234' OR key = 'qwerty';
```

Zapytanie zwróci rekordy spełniające przynajmniej jeden z warunków.

W podatnej aplikacji manipulowanie warunkiem WHERE może spowodować zwrócenie większej liczby rekordów niż zamierzono.

## 8.3. Operator UNION

`UNION` pozwala połączyć wyniki dwóch zapytań SELECT.

Przykład:

```sql
SELECT key, secret FROM secrets
UNION
SELECT key, secret FROM secrets;
```

Warunek: oba zapytania muszą zwracać taką samą liczbę kolumn.

W naszej tabeli są dwie kolumny:

- `key`,
- `secret`.

Dlatego zapytania muszą zwracać po dwie kolumny.

## 8.4. Zadanie 1 – SQL Injection

### Polecenie

Uruchom aplikację `sql_secrets.py`, a następnie zademonstruj, w jaki sposób podatność SQL Injection pozwala uzyskać wszystkie sekrety z przykładowej tabeli.

### Rozwiązanie krok po kroku

**Krok 1. Uruchom bazę i aplikację**

```bash
python create_db.py
python sql_secrets.py
```

**Krok 2. Otwórz formularz**

```text
http://127.0.0.1:5000/
```

**Krok 3. Przetestuj zapytanie SQL**

Wykonaj zwykłe zapytanie:

```bash
curl -G --data-urlencode "key=1234" http://127.0.0.1:5000/sql_secrets
```

Powinien pojawić się sekret przypisany do klucza `1234`.

W dalszej części laboratorium analizujemy wpływ zmiany warunków SQL i łączenia wyników za pomocą UNION na kontrolowanej bazie z fikcyjnymi danymi.

Ważna obserwacja: jeżeli aplikacja wyświetla wyniki wszystkich rekordów, oznacza to, że filtr nie ogranicza już dostępu zgodnie z pierwotnym zamierzeniem.

---

# 9. Poznawanie pól i struktury bazy danych

## 9.1. Tabela sqlite_master

SQLite posiada specjalną tabelę:

```sql
sqlite_master
```

Przechowuje ona informacje o obiektach bazy danych.

Najważniejsze kolumny:

| Kolumna | Znaczenie |
|---|---|
| `type` | Typ obiektu |
| `name` | Nazwa obiektu |
| `sql` | Instrukcja tworząca obiekt |

Możemy sprawdzić strukturę własnej testowej bazy:

```python
import sqlite3

db = sqlite3.connect("secrets.db")

wynik = db.execute("""
    SELECT type, name, sql
    FROM sqlite_master
""").fetchall()

for row in wynik:
    print(row)

db.close()
```

Przykładowy wynik:

```text
('table', 'secrets', 'CREATE TABLE secrets (key TEXT, secret TEXT)')
```

Widzimy:
- nazwę tabeli: `secrets`,
- kolumny: `key` i `secret`,
- typy kolumn: `TEXT`.

## 9.2. Sprawdzanie kolumn tabeli

SQLite udostępnia również polecenie:

```sql
PRAGMA table_info(secrets);
```

Przykład w Pythonie:

```python
import sqlite3

db = sqlite3.connect("secrets.db")

wynik = db.execute(
    "PRAGMA table_info(secrets)"
).fetchall()

for kolumna in wynik:
    print(kolumna)

db.close()
```

Wynik zawiera informacje o kolumnach tabeli.

Przykładowo:

```text
(0, 'key', 'TEXT', 0, None, 0)
(1, 'secret', 'TEXT', 0, None, 0)
```

Oznacza to, że tabela ma dwie kolumny tekstowe.

## 9.3. Zadanie 2 – Poznanie wszystkich pól key

### Polecenie

W jaki sposób atakujący może poznać wszystkie wartości pola `key`?

### Rozwiązanie krok po kroku

**Krok 1. Odczytaj strukturę tabeli**

Wykonaj:

```bash
python -c "import sqlite3; db=sqlite3.connect('secrets.db'); print(db.execute('PRAGMA table_info(secrets)').fetchall()); db.close()"
```

**Krok 2. Odczytaj klucze z własnej bazy testowej**

Utwórz plik `show_keys.py`:

```python
import sqlite3

db = sqlite3.connect("secrets.db")

wyniki = db.execute(
    "SELECT key FROM secrets"
).fetchall()

for row in wyniki:
    print(row[0])

db.close()
```

Uruchom:

```bash
python show_keys.py
```

Wynik:

```text
1234
qwerty
```

**Wniosek:** Jeżeli aplikacja pozwala na wykonywanie niekontrolowanych zapytań SQL, atakujący może próbować uzyskać dostęp do rekordów, które nie powinny być dla niego dostępne.

---

# 10. Naprawa SQL Injection

Najważniejszą metodą ochrony przed SQL Injection jest stosowanie zapytań parametryzowanych.

Zamiast:

```python
query = "SELECT * FROM secrets WHERE key='%s'" % key

cursor.execute(query)
```

należy użyć:

```python
cursor.execute(
    "SELECT * FROM secrets WHERE key = ?",
    (key,)
)
```

Wartość `key` jest przekazywana oddzielnie od treści zapytania.

SQLite traktuje ją jako dane, a nie jako kod SQL.

## 10.1. Bezpieczna wersja aplikacji Flask

Utwórz plik:

```text
sql_secrets_safe.py
```

Wklej:

```python
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
```

## 10.2. Co zostało zmienione?

| Podatny kod | Bezpieczny kod |
|---|---|
| Sklejanie SQL przez `%` | Parametr `?` |
| Dane bezpośrednio w zapytaniu | Dane przekazywane osobno |
| Brak ograniczenia wejścia | Sprawdzenie pustej wartości i długości |
| Szczegóły błędu mogą być ujawnione | Szczegóły trafiają do logów |
| Brak kontroli statusów HTTP | Odpowiedzi 400, 404 i 500 |

## 10.3. Testowanie bezpiecznej aplikacji

Uruchom:

```bash
python sql_secrets_safe.py
```

Test poprawnego klucza:

```bash
curl -G --data-urlencode "key=1234" http://127.0.0.1:5000/sql_secrets
```

Oczekiwany wynik:

```html
<p>Secret: Hello world</p>
```

Test drugiego klucza:

```bash
curl -G --data-urlencode "key=qwerty" http://127.0.0.1:5000/sql_secrets
```

Oczekiwany wynik:

```html
<p>Secret: Top secret</p>
```

Test nieistniejącego klucza:

```bash
curl -G --data-urlencode "key=nieistnieje" http://127.0.0.1:5000/sql_secrets
```

Oczekiwany kod:

```text
404
```

**Wniosek:** Parametryzacja sprawia, że nawet jeżeli użytkownik poda znaki specjalne SQL, zostaną potraktowane jako wartość tekstowa, a nie instrukcja SQL.

---

# 11. Dodatkowe zabezpieczenia aplikacji Flask

Samo zastosowanie parametrów SQL nie wystarcza do zabezpieczenia całej aplikacji.

Warto zastosować również kilka dodatkowych zasad.

## 11.1. Walidacja danych wejściowych

Przykład:

```python
key = request.args.get("key", "")

if not key:
    return "Brak klucza", 400

if len(key) > 50:
    return "Klucz jest za długi", 400
```

Można też sprawdzić format za pomocą wyrażenia regularnego:

```python
import re

if not re.fullmatch(r"[a-zA-Z0-9]+", key):
    return "Nieprawidłowy format klucza", 400
```

## 11.2. Ograniczanie uprawnień

Aplikacja powinna:
- działać na osobnym koncie systemowym,
- nie działać jako root,
- mieć dostęp tylko do potrzebnych plików,
- nie mieć zbędnych uprawnień do zapisu,
- nie mieć niepotrzebnego dostępu do sieci.

## 11.3. Bezpieczne komunikaty błędów

Nie należy zwracać użytkownikowi:

```python
return str(error)
```

Lepiej:

```python
except sqlite3.Error:
    app.logger.exception("Błąd bazy danych")
    return "Wystąpił błąd serwera", 500
```

Dzięki temu szczegóły trafiają do logów, a użytkownik otrzymuje ogólny komunikat.

## 11.4. Wyłączenie debugowania

Na produkcji:

```python
app.run(debug=False)
```

Nie należy udostępniać publicznie interaktywnego debuggera Flask.

W rzeczywistym wdrożeniu aplikację należy uruchamiać przez odpowiedni serwer WSGI, a nie przez developerski serwer Flask.

---

# 12. Podsumowanie – Code Injection i SQL Injection

| Cecha | Code Injection | SQL Injection |
|---|---|---|
| Miejsce podatności | Kod aplikacji | Zapytanie SQL |
| Język | Python | SQL |
| Niebezpieczna konstrukcja | `exec()`, `eval()` | Sklejanie zapytań SQL |
| Skutek | Wykonywanie niepożądanego kodu | Nieuprawniony dostęp lub zmiana danych |
| Ochrona | Walidacja i ograniczona interpretacja | Parametryzowane zapytania |
| Przykładowa funkcja | `exec()` | `execute()` z `?` |

## Najważniejsze różnice

**Code Injection:**

Użytkownik wpływa na kod wykonywany przez interpreter Pythona.

Przykładowy podatny fragment:

```python
exec("result = " + expr)
```

Naprawa:

```python
result = calculate(expr)
```

gdzie `calculate()` obsługuje tylko jawnie dozwolone działania.

**SQL Injection:**

Użytkownik wpływa na składnię zapytania SQL.

Przykładowy podatny fragment:

```python
query = "SELECT * FROM secrets WHERE key='%s'" % key
```

Naprawa:

```python
cursor.execute(
    "SELECT * FROM secrets WHERE key = ?",
    (key,)
)
```

---

# 13. Pytania kontrolne 


### Dlaczego funkcja exec() jest niebezpieczna?

Ponieważ wykonuje instrukcje Pythona. Jeżeli użytkownik kontroluje przekazywany tekst, może doprowadzić do wykonania niepożądanego kodu.

### Do czego służy app.logger?

Do zapisywania informacji diagnostycznych i błędów w logach aplikacji.

### Czy samo sprawdzanie danych wejściowych zabezpiecza SQL?

Nie. Podstawową ochroną jest parametryzacja zapytań. Walidacja jest dodatkową warstwą zabezpieczeń.


---

# 14. Najważniejsze komendy i fragmenty kodu

## Uruchamianie aplikacji Flask

```bash
python -m pip install flask
python calc.py
python calc_safe.py
python create_db.py
python sql_secrets.py
python sql_secrets_safe.py
```

Pamiętaj, że każdy serwer uruchomiony na porcie 5000 trzeba zatrzymać przed uruchomieniem kolejnej wersji. Można to zrobić przez `CTRL+C`.

## Testowanie przez curl

Zwykły parametr GET:

```bash
curl -G --data-urlencode "expr=2+3" http://127.0.0.1:5000/
```

Przekazanie klucza:

```bash
curl -G --data-urlencode "key=1234" http://127.0.0.1:5000/sql_secrets
```

## Flask – najważniejsze elementy

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    wartosc = request.args.get("q", "")
    return wartosc

if __name__ == "__main__":
    app.run(debug=False)
```

## SQLite – połączenie i pobieranie danych

```python
import sqlite3

db = sqlite3.connect("secrets.db")

wynik = db.execute(
    "SELECT * FROM secrets WHERE key = ?",
    ("1234",)
).fetchall()

print(wynik)

db.close()
```

## Bezpieczna obsługa błędów

```python
try:
    # operacja
    pass

except sqlite3.Error:
    app.logger.exception("Błąd bazy danych")
    return "Błąd serwera", 500
```

## Walidacja danych

```python
import re

if re.fullmatch(r"[0-9]+", wartosc):
    print("Poprawne dane")
else:
    print("Niepoprawne dane")
```

---
