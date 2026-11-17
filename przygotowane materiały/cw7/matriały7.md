# Bezpieczeństwo aplikacji – Injection, SQL, Python i Flask

## 1. Czym jest Injection (wstrzyknięcie)?

**Injection** to podatność polegająca na tym, że aplikacja łączy dane dostarczone przez użytkownika z kodem wykonywanym przez interpreter, np.:

- SQL – zapytania do bazy danych.
- Python – wykonywanie kodu Pythona.
- Shell – polecenia systemowe.

Problem pojawia się wtedy, gdy interpreter nie potrafi odróżnić danych od instrukcji.

### Przykład podatnego kodu SQL

```python
nazwa = input("Podaj nazwę: ")

zapytanie = "SELECT * FROM osoby WHERE nazwa = '" + nazwa + "'"

db.execute(zapytanie)
```

Jeżeli użytkownik wpisze zwykłą nazwę, zapytanie może działać poprawnie.

Jednak użytkownik może wprowadzić znaki specjalne, które zmienią strukturę zapytania.

**Najważniejsze:** Dane użytkownika nie powinny być bezpośrednio doklejane do kodu SQL, Pythona ani poleceń systemowych.

---

# 2. Podstawy SQL

SQL (Structured Query Language) to język służący do komunikacji z relacyjnymi bazami danych.

## 2.1. SELECT

`SELECT` służy do wybierania danych z tabeli.

```sql
SELECT * FROM osoby;
```

- `SELECT` – wybierz dane.
- `*` – wybierz wszystkie kolumny.
- `FROM osoby` – z tabeli osoby.

Możemy również wybrać konkretne kolumny:

```sql
SELECT id, nazwa FROM osoby;
```

To zapytanie zwraca kolumny `id` i `nazwa`.

## 2.2. WHERE

`WHERE` służy do filtrowania rekordów.

```sql
SELECT * FROM osoby WHERE id = 1;
```

Zwraca rekordy, których `id` wynosi 1.

Możemy używać różnych operatorów:

| Operator | Znaczenie |
|---|---|
| `=` | równe |
| `!=` | różne |
| `>` | większe |
| `<` | mniejsze |
| `>=` | większe lub równe |
| `<=` | mniejsze lub równe |
| `AND` | oba warunki muszą być prawdziwe |
| `OR` | przynajmniej jeden warunek musi być prawdziwy |

```sql
SELECT * FROM osoby
WHERE id = 1 OR id = 2;
```

Zwraca osoby o identyfikatorze 1 lub 2.

## 2.3. Napisy w apostrofach

W SQL wartości tekstowe zapisujemy zazwyczaj w apostrofach.

```sql
SELECT * FROM osoby WHERE nazwa = 'Jan';
```

Tekst `Jan` jest wartością, której szukamy.

Problem pojawia się, kiedy tekst zawiera apostrof.

```text
O'Neil
```

Jeżeli bezpośrednio dokleimy go do zapytania, apostrof może zostać potraktowany jako zakończenie tekstu.

Dlatego należy stosować parametry zapytań, a nie ręcznie sklejać SQL.

## 2.4. Komentarz SQL – `--`

W SQL dwa myślniki rozpoczynają komentarz do końca bieżącego wiersza.

Przykład:

```sql
SELECT * FROM osoby; -- To jest komentarz
```

Interpreter SQL ignoruje tekst komentarza.

Komentarze mogą wpływać na interpretację niepoprawnie zbudowanych zapytań.

## 2.5. UNION SELECT

`UNION` służy do łączenia wyników dwóch zapytań SELECT.

```sql
SELECT id, nazwa FROM osoby
UNION
SELECT id, nazwa FROM pracownicy;
```

Wynik zawiera rekordy pochodzące z obu zapytań.

### Warunek zgodnej liczby kolumn

Oba zapytania muszą zwracać:
- taką samą liczbę kolumn,
- typy danych, które można ze sobą odpowiednio połączyć.

W przykładzie każde zapytanie SELECT zwraca dwie kolumny, więc liczba kolumn jest zgodna.

---

# 3. SQLite

SQLite to lekka, relacyjna baza danych, która przechowuje dane najczęściej w jednym pliku.

W Pythonie można korzystać z niej za pomocą standardowego modułu, nie trzeba instalować dodatkowej biblioteki.

```python
import sqlite3
```

## 3.1. Tabela sqlite_master

SQLite ma "tabelę systemową":

```sql
sqlite_master
```

Przechowuje ona informacje o obiektach znajdujących się w bazie danych.

Najważniejsze kolumny:

| Kolumna | Znaczenie |
|---|---|
| `type` | typ obiektu, np. table lub index |
| `name` | nazwa obiektu |
| `sql` | instrukcja SQL, która utworzyła obiekt |

Przykładowe typy obiektów:
- `table` – tabela,
- `index` – indeks,
- `view` – widok,
- `trigger` – wyzwalacz.

Przykład odczytania informacji o tabelach:

```sql
SELECT type, name, sql
FROM sqlite_master;
```

Zapytanie pozwala sprawdzić strukturę obiektów w bazie.

## 3.2. Operator `||`

W SQLite operator " | | " służy do łączenia tekstów.

```sql
SELECT 'Ala' || ' ma kota';
```

Wynik:

```text
Ala ma kota
```

To tak jak  "Ala" + " ma kota"  w Pythonie.


# 4. Zapytania SQL z parametrami



**Zapytania parametryzowane chronią przed SQL Injection** - oddzielają treść zapytania od danych użytkownika.

## 4.1. Znak zapytania `?` - miejsce na parametr

```python
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
```

Wynik:

```python
[(1, "O'Neil")]
```

### Jak to działa?

```python
db.execute(
    "SELECT * FROM osoby WHERE nazwa = ?",
    ("O'Neil",)
)
```

Mamy dwa elementy:

1. Treść zapytania SQL:

```sql
SELECT * FROM osoby WHERE nazwa = ?
```

2. Wartość parametru:

```python
("O'Neil",)
```

SQLite traktuje przekazaną wartość (w tym apostrof) jako dane, a nie fragment kodu SQL.

## 4.2. Dlaczego w `(wartosc,)` jest przecinek?

W Pythonie  (wartosc,)  oznacza krotkę jednoelementową.


```python
(5)      # zwykła liczba
(5,)     # krotka jednoelementowa
(5, 10)  # krotka dwuelementowa
```

Przecinek tworzy krotkę, a nie same nawiasy.

## 4.3. Czego parametr `?` nie zastąpi?

Parametry zapytań służą do przekazywania **wartości**, a nie elementów składni SQL.

Nie można przekazać:
- nazwy tabeli,
- nazwy kolumny,
- słowa kluczowego SQL,
- kierunku sortowania, np. ASC lub DESC.

Niepoprawny pomysł:

```python
db.execute("SELECT * FROM ?", (nazwa_tabeli,))
```

Parametr zostanie potraktowany jako wartość, a nie nazwa tabeli.

### Jak bezpiecznie wybierać nazwę tabeli?

Trzeba zastosować jawną listę dozwolonych wartości.

```python
dozwolone_tabele = ["osoby", "pracownicy"]

wybrana = "osoby"

if wybrana not in dozwolone_tabele:
    raise ValueError("Niedozwolona tabela")

zapytanie = f"SELECT * FROM {wybrana}"
```

Wstawienie nazwy tabeli do zapytania jest dopuszczalne tylko dlatego, że pochodzi ona ze sprawdzonej listy, a nie bezpośrednio od użytkownika.

---

# 5. Ujawnianie informacji (Information Disclosure)

Ujawnianie informacji to sytuacja, w której aplikacja pokazuje użytkownikowi dane, które powinny pozostać wewnętrzne.

Przykłady:
- szczegóły błędów bazy danych,
- ślady stosu (stack trace),
- nazwy tabel i kolumn,
- ścieżki do plików,
- informacje o systemie operacyjnym,
- fragmenty kodu aplikacji.

## 5.1. Komunikaty błędów bazy danych

Przykładowy błąd:

```text
no such table: użytkownicy
```

Informuje, że tabela o nazwie `użytkownicy` nie istnieje.

Takie komunikaty mogą ujawniać strukturę bazy danych.

## 5.2. Ślad stosu (Stack Trace)

Stack trace to szczegółowy zapis informacji o błędzie w programie.

Może zawierać:
- nazwę pliku,
- numer linii,
- nazwę funkcji,
- rodzaj wyjątku,
- fragmenty wywołań funkcji.

Jest przydatny programiście, ale nie powinien być pokazywany zwykłemu użytkownikowi.

## 5.3. Tryb diagnostyczny

Tryb diagnostyczny (debug mode) pomaga podczas tworzenia aplikacji.

Może pokazywać szczegółowe informacje o błędach.

Na produkcji należy:
- wyłączyć publiczny tryb debugowania,
- nie zwracać użytkownikowi szczegółowych wyjątków,
- zapisywać szczegóły błędów w logach,
- zwracać ogólne komunikaty.

---

# 6. Niebezpieczne funkcje Pythona: eval, exec i compile

Python pozwala dynamicznie wykonywać kod. Niektóre funkcje mogą jednak stanowić poważne zagrożenie, jeżeli wykorzystujemy dane użytkownika.

## 6.1. eval()

Oblicza wyrażenie Pythona i zwraca jego wynik.


```python
wynik = eval("2 + 3")
```

Wynik:

```text
5
```

Problem:

```python
eval(dane_uzytkownika)
```

Jeżeli użytkownik kontroluje zawartość `dane_uzytkownika`, może doprowadzić do wykonania niepożądanego kodu.

Ważne: `eval()` nie ogranicza się wyłącznie do prostych działań matematycznych.

## 6.2. exec()

Wykonuje instrukcje Pythona.

Przykład:

```python
kod = "x = 10\nprint(x)"

exec(kod)
```

Wynik:

```text
10
```

| _ |  |
|---|---|
| `eval()` | oblicza wyrażenie |
| `exec()` | wykonuje instrukcje |
| `compile()` | tworzy obiekt kodu do późniejszego wykonania lub ewaluacji |

## 6.3. compile()

`compile()` przekształca tekst lub kod w obiekt kodu.

Przykład:

```python
kod = compile("2 + 3", "<string>", "eval")

wynik = eval(kod)
```

Wynik:

```text
print(wynik) -> 5
```

`compile()` samo w sobie nie wykonuje kodu. Tworzy obiekt, który może zostać wykonany później.

## 6.4. __import__()

`__import__()` to wbudowana funkcja Pythona pozwalająca dynamicznie importować moduły.

```python
modul = __import__("math")

print(modul.sqrt(16))
```

Wynik:

```text
4.0
```

Brak słowa `import` w tekście użytkownika nie oznacza, że kod jest bezpieczny.

## 6.5. os.listdir()

Funkcja `os.listdir()` zwraca listę plików i katalogów znajdujących się w podanej lokalizacji.

```python
import os

pliki = os.listdir(".")

print(pliki)
```

Kropka oznacza bieżący katalog.

Funkcja może ujawnić strukturę systemu plików.

## 6.6. open()

Funkcja `open()` służy do otwierania plików.

Przykład:

```python
plik = open("dane.txt", "r")

zawartosc = plik.read()

plik.close()
```

Tryby:
- `r` – odczyt,
- `w` – zapis z wyczyszczeniem dotychczasowej zawartości,
- `a` – dopisywanie,
- `x` – utworzenie nowego pliku.

Nieograniczony dostęp do `open()` może pozwolić na odczyt lub modyfikację plików, do których proces aplikacji ma uprawnienia.

## 6.7. os.getuid()

Funkcja `os.getuid()` zwraca identyfikator użytkownika systemowego, pod którego uprawnieniami działa proces.

```python
import os

print(os.getuid())
```

Wynik to liczba całkowita oznaczająca UID.

UID równy `0` oznacza użytkownika root w systemach Unix/Linux.

Ta funkcja jest dostępna na systemach obsługujących UID, np. Linux i macOS.

---

# 7. Walidacja danych wejściowych

## 7.1. Lista dozwolonych wartości (Allowlist)

To metoda polegająca na określeniu, jakie wartości są dopuszczalne.


```python
dozwolone = ["admin", "user", "guest"]

rola = "user"

if rola in dozwolone:
    print("Poprawna rola")
else:
    print("Niepoprawna rola")
```

Wynik:

```text
Poprawna rola
```

Dopuszczamy tylko znane, wcześniej określone wartości.

To bezpieczniejsze niż próba blokowania pojedynczych niebezpiecznych słów.

## 7.2. Wyrażenia regularne – re.fullmatch()

Wyrażenia regularne pozwalają sprawdzać, czy tekst spełnia określony wzorzec.

Moduł:

```python
import re
```

Funkcja `re.fullmatch()` sprawdza, czy cały tekst pasuje do wzorca.

```python
import re

print(bool(re.fullmatch(r'[0-9]+', '123')))
print(bool(re.fullmatch(r'[0-9]+', '12x')))
```

Wynik:

```text
True
False
```

### Wyjaśnienie wzorca `[0-9]+`

| Element | Znaczenie |
|---|---|
| `[0-9]` | dowolna cyfra od 0 do 9 |
| `+` | jedna lub więcej powtórzeń |

Czyli `[0-9]+` oznacza: tekst musi zawierać przynajmniej jedną cyfrę i żadnych innych znaków.

### fullmatch() a match() i search()

| Funkcja | Działanie |
|---|---|
| `re.match()` | sprawdza dopasowanie od początku tekstu |
| `re.search()` | szuka dopasowania w dowolnym miejscu |
| `re.fullmatch()` | wymaga dopasowania całego tekstu |

Przykład:

```python
re.fullmatch(r'[0-9]+', '123abc')
```

Zwróci `None`, ponieważ cały tekst nie składa się z cyfr.

**Do zapamiętania:** `fullmatch()` jest przydatne, gdy wymagamy, aby całe wejście spełniało określony format.

---

# 8. Bezpieczny kalkulator w Pythonie

Jeżeli chcemy stworzyć kalkulator, nie powinniśmy wykonywać danych użytkownika za pomocą `eval()`.

Lepszym rozwiązaniem jest zdefiniowanie dozwolonego formatu wejścia i samodzielne wykonywanie operacji.

Przykładowa prosta walidacja:

```python
import re

wyrazenie = "123"

if re.fullmatch(r"[0-9]+", wyrazenie):
    liczba = int(wyrazenie)
    print(liczba)
else:
    print("Niepoprawne dane")
```

Przy tworzeniu kalkulatora trzeba dodatkowo:
- zdefiniować dozwoloną gramatykę wyrażeń,
- obsługiwać tylko jawnie wybrane operatory,
- odrzucać puste dane,
- ograniczać długość wejścia i wielkość liczb,
- obsługiwać dzielenie przez zero,
- nie wykonywać dowolnego kodu Pythona.

**Najważniejsza zasada:** Nie należy traktować `eval()` jako bezpiecznego kalkulatora tylko dlatego, że próbujemy zablokować niektóre słowa.

---

# 9. Zasada najmniejszych uprawnień (Least Privilege)

Zasada najmniejszych uprawnień polega na tym, że program powinien mieć tylko takie uprawnienia, jakie są niezbędne do jego działania.

Przykłady:

1. Aplikacja nie powinna działać jako root.
2. Powinna korzystać z osobnego użytkownika systemowego.
3. Powinna mieć dostęp tylko do potrzebnych plików.
4. Jeżeli nie musi zapisywać danych, system plików powinien być tylko do odczytu.
5. Powinna mieć ograniczony dostęp do zasobów systemowych.

### Dlaczego jest to ważne?

Załóżmy, że aplikacja posiada podatność pozwalającą na wykonanie niepożądanego kodu.

Jeśli działa jako zwykły użytkownik z ograniczonymi uprawnieniami, skutki ataku będą mniejsze niż gdyby miała root.

---

# 10. Flask – obsługa żądań HTTP

Flask to framework Pythona służący do tworzenia aplikacji internetowych.

Instalacja:

```bash
pip install flask
```

## 10.1. request.args

`request.args` służy do pobierania parametrów przekazanych w adresie URL metodą GET.

Przykładowy adres:

```text
http://localhost:5000/szukaj?q=Jan
```

Pobranie parametru:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/szukaj")
def szukaj():
    q = request.args.get("q")
    return q
```

W tym przypadku:

```python
q = "Jan"
```

## 10.2. Kod HTTP 400

Kod HTTP 400 oznacza:

**Bad Request – nieprawidłowe żądanie.**

Możemy go zwrócić, jeśli użytkownik przekazał niepoprawne dane.

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/liczba")
def liczba():
    wartosc = request.args.get("n")

    if wartosc is None or not wartosc.isdigit():
        return "Nieprawidłowe dane", 400

    return "Poprawne dane"
```

Jeśli użytkownik nie poda liczby albo poda nieprawidłową wartość, aplikacja zwróci kod 400.

## 10.3. app.logger

`app.logger` służy do zapisywania komunikatów w logach aplikacji.

```python
try:
    wynik = 10 / 0
except Exception:
    app.logger.exception("Wystąpił błąd")
    return "Wystąpił błąd serwera", 500
```

Co się dzieje?

1. Program próbuje wykonać dzielenie przez zero.
2. Pojawia się wyjątek.
3. Szczegóły błędu trafiają do logów.
4. Użytkownik dostaje ogólny komunikat.
5. Nie otrzymuje szczegółowego stack trace.

### Dlaczego nie pokazywać szczegółów błędu użytkownikowi?

Ponieważ mogą zawierać:
- ścieżki plików,
- nazwy tabel,
- dane techniczne,
- informacje o konfiguracji,
- fragmenty kodu.

---

# 11. SQLite w Pythonie – najważniejsze funkcje

Do obsługi SQLite używamy modułu:

```python
import sqlite3
```

## 11.1. connect()

Łączy się z bazą danych.

```python
db = sqlite3.connect("baza.db")
```

Jeżeli plik bazy nie istnieje, SQLite zazwyczaj go utworzy.

Baza wyłącznie w pamięci:

```python
db = sqlite3.connect(":memory:")
```

Po zamknięciu połączenia baza pamięciowa przestaje istnieć.

## 11.2. execute()

Wykonuje zapytanie SQL.

```python
db.execute("CREATE TABLE osoby (id INTEGER, nazwa TEXT)")
```

Może wykonywać m.in.:
- SELECT,
- INSERT,
- UPDATE,
- DELETE,
- CREATE TABLE.

Przy przekazywaniu danych należy używać parametrów:

```python
db.execute(
    "INSERT INTO osoby VALUES (?, ?)",
    (1, "Jan")
)
```

## 11.3. fetchall()

Pobiera wszystkie rekordy zwrócone przez zapytanie SELECT.

```python
wynik = db.execute(
    "SELECT * FROM osoby"
).fetchall()

print(wynik)
```

Wynik jest listą krotek.

Przykładowo:

```python
[(1, 'Jan'), (2, 'Anna')]
```

---



# 12. curl opcje -G oraz --data-urlencode

Opcja `-G` powoduje, że dane przekazane przez `--data` lub `--data-urlencode` są dodawane do adresu URL jako parametry GET.

Opcja:

```bash
--data-urlencode
```

koduje przekazaną wartość zgodnie z zasadami kodowania parametrów URL.

Połączenie obu:

```bash
curl -G --data-urlencode 'q=tekst ze spacją' http://localhost:5000/szukaj
```

Wysyła żądanie GET z parametrem `q`.

Dzięki kodowaniu spacja i inne znaki specjalne są prawidłowo reprezentowane w adresie URL.

### Dlaczego kodowanie jest ważne?

Adres URL ma określoną składnię.

Niektóre znaki, np. spacje, `&` czy `#`, mają specjalne znaczenie.

Kodowanie pozwala przekazać je jako część wartości parametru, zamiast przypadkowo zmieniać strukturę adresu.

Kodowanie URL nie zabezpiecza przed SQL Injection. Ochronę zapytań SQL zapewniają przede wszystkim parametryzowane zapytania.

---

# 13. Kompletny przykład – bezpieczne zapytanie SQLite

Poniższy kod pokazuje podstawowe operacje na bazie danych i prawidłowe przekazywanie parametrów.

```python
import sqlite3
import re

# Utworzenie bazy w pamięci
db = sqlite3.connect(":memory:")

# Utworzenie tabeli
db.execute("""
    CREATE TABLE osoby (
        id INTEGER,
        nazwa TEXT
    )
""")

# Dodanie rekordu
db.execute(
    "INSERT INTO osoby VALUES (?, ?)",
    (1, "O'Neil")
)

# Pobranie rekordu z parametrem
wynik = db.execute(
    "SELECT id, nazwa FROM osoby WHERE nazwa = ?",
    ("O'Neil",)
).fetchall()

print(wynik)

# Walidacja danych
print(bool(re.fullmatch(r'[0-9]+', '123')))
print(bool(re.fullmatch(r'[0-9]+', '12x')))

db.close()
```

Oczekiwany wynik:

```text
[(1, "O'Neil")]
True
False
```


---
`eval()` oblicza wyrażenie i zwraca wynik. `exec()` wykonuje instrukcje Pythona.

### Pytanie 5

Co robi `sqlite3.connect(":memory:")`?

**Odpowiedź:** Tworzy połączenie z bazą SQLite przechowywaną w pamięci RAM. Nie tworzy trwałego pliku bazy.

### Pytanie 6

Dlaczego nie należy udostępniać stack trace użytkownikowi?

**Odpowiedź:** Może zawierać szczegóły techniczne aplikacji, ścieżki plików, informacje o bazie danych i fragmenty kodu.

### Pytanie 10

Dlaczego aplikacja nie powinna działać jako root?

**Odpowiedź:** Ponieważ w razie wykorzystania podatności atakujący mógłby uzyskać bardzo szerokie uprawnienia do systemu.

### Pytanie 12

Dlaczego parametr `?` nie może zastąpić nazwy tabeli?

**Odpowiedź:** Ponieważ parametry przekazują wartości danych, a nie elementy składni SQL, takie jak nazwy tabel i kolumn.


## Najważniejsze zasady

**Nigdy nie ufaj danym pochodzącym od użytkownika.**

Zawsze:
- waliduj dane wejściowe,
- stosuj parametryzowane zapytania SQL,
- nie wykonuj niezaufanego kodu przez `eval()` lub `exec()`,
- nie ujawniaj szczegółowych błędów użytkownikowi,
- ograniczaj uprawnienia aplikacji,
- korzystaj z list dozwolonych wartości tam, gdzie jest to możliwe.