
Jeżeli plik jest dostępny jako `welcome.py`, wejście na:

```text
http://localhost/welcome.py
```

może wywołać funkcję `index()`.

Parametry żądania mogą być przekazywane jako argumenty funkcji:

```python
def index(req, name=''):
    return "Witaj " + name
```

Przy żądaniu:

```text
http://localhost/welcome.py?name=Jan
```

zmienna `name` otrzyma wartość `Jan`.

`req` reprezentuje obiekt żądania obsługiwany przez mod_python.

# 2. Przykładowa aplikacja — formularz i welcome.py

Aplikacja składa się z dwóch elementów.

## 2.1. Formularz HTML

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
</head>
<body>
    <h3>What is your name?</h3>

    <form action="welcome.py" method="GET">
        <input type="text" name="name">
        <input type="submit" value="Send">
    </form>
</body>
</html>
```

Co się tutaj dzieje?

- Użytkownik wpisuje imię.
- Formularz wysyła dane do `welcome.py`.
- Metoda `GET` oznacza, że dane trafiają do adresu URL jako parametry.

Przykładowo:

```text
welcome.py?name=Jan
```

## 2.2. Skrypt welcome.py

Oryginalny kod:

```python
def index(req, name=''):
    html = '<html>'
    html += 'Hello ' + name
    html += '<p>Nice to meet you..</p>'
    html += '</html>'

    return html
```

Problem znajduje się w instrukcji:

```python
html += 'Hello ' + name
```

Aplikacja bezpośrednio umieszcza dane użytkownika w kodzie HTML.

Nie sprawdza ich ani nie koduje.

Jeżeli użytkownik poda zwykły tekst:

```text
Jan
```

otrzyma:

```html
<html>
Hello Jan
<p>Nice to meet you..</p>
</html>
```

Jeśli jednak poda znaczniki HTML, przeglądarka może je zinterpretować jako elementy strony.

To właśnie przykład podatności XSS.

# 3. Atak XSS — analiza przykładów

W każdym przypadku należy pamiętać o następującym modelu:

1. Użytkownik dostarcza niezaufane dane.
2. Serwer odbiera dane.
3. Serwer umieszcza je w odpowiedzi HTML bez odpowiedniego kodowania.
4. Przeglądarka interpretuje otrzymany HTML.
5. Ewentualny JavaScript wykonuje się w kontekście strony.

## 3.1. Zmiana tła strony

JavaScript może modyfikować wygląd dokumentu za pomocą DOM.

Przykładowo:

```javascript
document.body.style.backgroundColor = "red";
```

Działanie:
- `document` reprezentuje dokument strony.
- `body` oznacza element `<body>`.
- `style` pozwala zmieniać style CSS.
- `backgroundColor` odpowiada za kolor tła.

To pokazuje, że skrypt wykonany przez XSS może zmieniać wygląd strony widzianej przez ofiarę.

## 3.2. Automatyczne przekierowanie na inną stronę

JavaScript może zmienić adres aktualnej strony:

```javascript
window.location.href = "https://example.com";
```

Znaczenie:
- `window` reprezentuje okno przeglądarki.
- `location` przechowuje informacje o aktualnym adresie.
- `href` pozwala ustawić nowy adres.

Po wykonaniu instrukcji przeglądarka przejdzie pod wskazany adres.

Może to zostać wykorzystane np. do przekierowania użytkownika na fałszywą stronę logowania.

## 3.3. Wyświetlenie zewnętrznego obrazka

HTML pozwala osadzać obrazki z zewnętrznych serwerów.

Przykład:

```html
<img src="https://example.com/reklama.png" alt="Reklama">
```

Przeglądarka:
1. Odczytuje znacznik `<img>`.
2. Pobiera obraz z podanego adresu.
3. Wyświetla go na stronie.

Można w ten sposób wyświetlać zewnętrzne reklamy lub inne obrazy.

**Ważne:** pobranie zewnętrznego zasobu może również ujawnić jego serwerowi np. adres IP użytkownika i informacje zawarte w nagłówkach żądania. Ciasteczka strony atakowanej nie są automatycznie przekazywane do obcej domeny.

## 3.4. Ciasteczka i JavaScript

JavaScript udostępnia właściwość:

```javascript
document.cookie
```

Pozwala ona odczytywać ciasteczka dostępne dla JavaScript w aktualnym dokumencie.

Przykład bezpiecznego odczytu własnego testowego ciasteczka:

```javascript
document.cookie = "test=123; Path=/; SameSite=Lax";

console.log(document.cookie);
```

Można również ustawiać ciasteczka:

```javascript
document.cookie = "motyw=dark; Path=/; SameSite=Lax";
```

To zapisuje ciasteczko o nazwie `motyw` i wartości `dark`.

### Ważne ograniczenia document.cookie

JavaScript:
- Może odczytywać ciasteczka dostępne dla JavaScript.
- Może zapisywać ciasteczka, jeśli pozwalają na to ich ograniczenia.
- Nie może odczytać ciasteczek oznaczonych `HttpOnly`.
- Nie może dowolnie ustawiać atrybutu `HttpOnly`.
- Nie może dowolnie zmieniać ciasteczek należących do innych domen.

### Dlaczego HttpOnly jest ważne?

Jeżeli ciasteczko sesyjne ma atrybut:

```http
Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Lax
```

JavaScript nie odczyta go przez `document.cookie`.

Jednak XSS nadal jest niebezpieczny.

Złośliwy kod może np. wykonywać żądania do aplikacji w kontekście zalogowanego użytkownika. Przeglądarka może automatycznie dołączyć odpowiednie ciasteczko sesyjne.

**Wniosek:** HttpOnly utrudnia kradzież tokenu sesyjnego, ale nie uniemożliwia wykonywania działań w ramach przejętej strony.

## 3.5. Dlaczego nie należy wykradać ciasteczek?

W ćwiczeniu pojawia się zadanie przesłania ciasteczka na zewnętrzny serwer i zapisania go w pliku.

Jest to przykład kradzieży tokenu sesyjnego.

Mechanizm zagrożenia wygląda następująco:

1. Użytkownik jest zalogowany.
2. Przeglądarka przechowuje ciasteczko sesyjne.
3. Podatna aplikacja pozwala wykonać obcy JavaScript.
4. Skrypt może próbować uzyskać dostęp do danych dostępnych dla JavaScript.
5. Jeżeli token nie ma `HttpOnly`, może być narażony na odczyt.
6. Posiadanie tokenu może pozwolić na przejęcie sesji.

Nie podaję gotowego kodu przesyłającego cudze tokeny na zewnętrzny serwer. Do nauki warto zamiast tego wykorzystać własne, sztuczne ciasteczko testowe i sprawdzić różnicę między ciasteczkiem z `HttpOnly` i bez tego atrybutu.

# 4. Manipulowanie elementami DOM

JavaScript może odczytywać i modyfikować elementy HTML strony.

Przykładowo:

```html
<div id="notatka">
    Moja przykładowa notatka
</div>
```

Odczyt tekstu:

```javascript
const element = document.getElementById("notatka");

console.log(element.textContent);
```

Wynik:

```text
Moja przykładowa notatka
```

Można również odczytać HTML:

```javascript
console.log(element.innerHTML);
```

Różnica:

| Właściwość | Działanie |
|---|---|
| `textContent` | Odczytuje tekst elementu. |
| `innerHTML` | Odczytuje HTML znajdujący się wewnątrz elementu. |

Analogicznie przy zapisie:

```javascript
element.textContent = "<b>Test</b>";
```

Wyświetli dosłownie znaczniki.

Natomiast:

```javascript
element.innerHTML = "<b>Test</b>";
```

Utworzy pogrubiony tekst.

**Zasada bezpieczeństwa:** przy wyświetlaniu zwykłego tekstu użytkownika preferuj `textContent`.

# 5. Kodowanie adresów URL

Czasami znaki specjalne w adresie URL mają specjalne znaczenie.

Przykładowo:
- `?` rozpoczyna parametry zapytania.
- `&` oddziela parametry.
- `=` oddziela nazwę parametru od wartości.
- `#` rozpoczyna fragment adresu.

Dlatego wartości parametrów należy kodować.

JavaScript udostępnia:

```javascript
encodeURIComponent("Ala ma kota & psa");
```

Wynik:

```text
Ala%20ma%20kota%20%26%20psa
```

Kodowanie:
- Spacja → `%20`
- `&` → `%26`
- `=` → `%3D`
- `?` → `%3F`

### A co z optymalizacją adresu przez przeglądarkę?

Przeglądarka może normalizować adresy URL, np. kodować niektóre znaki lub zmieniać ich reprezentację.

Nie należy traktować ręcznego wpisywania znaków jako metody zabezpieczenia.

Jeżeli chcemy przekazać konkretną wartość parametru GET, powinniśmy używać kodowania URL, np. `encodeURIComponent()` dla pojedynczej wartości.

Warto również pamiętać:

`encodeURIComponent()` nie zabezpiecza przed XSS. Koduje wartość URL, a nie treść HTML czy JavaScript.

# 6. Jak pobrać argument GET?

## W mod_python.publisher

Parametr może być przekazany bezpośrednio do argumentu funkcji:

```python
def index(req, name=''):
    return "Witaj " + name
```

Adres:

```text
welcome.py?name=Jan
```

Wartość `Jan` trafi do zmiennej `name`.

## We Flasku

Do pobierania parametrów GET służy:

```python
request.args.get("name")
```

Przykład:

```python
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name", "")
    return "Witaj " + name
```

Dane GET pochodzą od użytkownika i zawsze powinny być traktowane jako niezaufane.

# 7. Poprawiona wersja welcome.py

Oryginalny problem:

```python
html += 'Hello ' + name
```

Dane użytkownika trafiają bezpośrednio do HTML.

Poprawiona wersja:

```python
import html

def index(req, name=''):
    bezpieczne_imie = html.escape(name, quote=True)

    wynik = '<html>'
    wynik += '<body>'
    wynik += 'Hello ' + bezpieczne_imie
    wynik += '<p>Nice to meet you..</p>'
    wynik += '</body>'
    wynik += '</html>'

    return wynik
```

### Dlaczego to działa?

`html.escape()` zamienia znaki specjalne na encje HTML.

Przykładowo:

```python
html.escape("<b>Jan</b>")
```

Wynik:

```text
&lt;b&gt;Jan&lt;/b&gt;
```

Przeglądarka wyświetli tekst zamiast interpretować go jako znaczniki HTML.

**Najważniejsze:** kodowanie musi odpowiadać kontekstowi wstawienia danych. `html.escape()` nadaje się do tekstu HTML i odpowiednio kodowanych atrybutów, ale nie jest uniwersalnym zabezpieczeniem dla JavaScript ani URL.

---

# 8. Analiza programu Flask nr 1

Program:

```python
from flask import Flask, render_template, request, make_response
import markdown
from collections import deque

app = Flask(__name__)

notes = []
recent_users = deque(maxlen=3)

@app.route("/")
def username():
    return render_template("main.html")

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        username = request.form.get("username", "unknown")

        if not username in recent_users:
            recent_users.append(username)

        resp = make_response(
            render_template(
                "hello.html",
                username=username,
                notes=notes,
                recent_users=list(recent_users)
            )
        )

        resp.set_cookie("username", username)
        return resp

    if request.method == 'GET':
        username = request.cookies.get("username", "unknown")

        return render_template(
            "hello.html",
            username=username,
            notes=notes,
            recent_users=list(recent_users)
        )

@app.route("/render", methods=['POST'])
def render():
    md = request.form.get("markdown", "")
    rendered = markdown.markdown(md)

    notes.append(rendered)

    return render_template("markdown.html", rendered=rendered)

@app.route("/render/<rendered_id>")
def render_old(rendered_id):
    if int(rendered_id) > len(notes):
        return "Wrong note id", 404

    rendered = notes[int(rendered_id) - 1]

    return render_template("markdown.html", rendered=rendered)
```

## 8.1. Importy

```python
from flask import Flask, render_template, request, make_response
```

Importowane elementy:

| Element | Znaczenie |
|---|---|
| `Flask` | Tworzy aplikację. |
| `render_template` | Renderuje szablony HTML. |
| `request` | Udostępnia informacje o żądaniu HTTP. |
| `make_response` | Pozwala utworzyć i modyfikować odpowiedź HTTP. |

```python
import markdown
```

Biblioteka przekształca tekst Markdown na HTML.

```python
from collections import deque
```

`deque` to kolejka, która może mieć ograniczoną maksymalną długość.

## 8.2. Inicjalizacja aplikacji

```python
app = Flask(__name__)

notes = []
recent_users = deque(maxlen=3)
```

- `app` to obiekt aplikacji Flask.
- `notes` przechowuje notatki.
- `recent_users` przechowuje maksymalnie trzech ostatnich użytkowników.

`maxlen=3` oznacza, że po dodaniu kolejnego elementu najstarszy może zostać usunięty.

## 8.3. Strona główna

```python
@app.route("/")
def username():
    return render_template("main.html")
```

Dekorator `@app.route("/")` określa adres strony głównej.

Po wejściu na `/` Flask renderuje plik `main.html`.

## 8.4. Obsługa użytkownika — /hello

```python
@app.route("/hello", methods=['GET', 'POST'])
```

Trasa obsługuje dwie metody HTTP:

- GET
- POST

### Metoda POST

```python
username = request.form.get("username", "unknown")
```

Pobiera wartość pola `username` przesłanego formularzem.

Jeżeli pole nie istnieje, zwraca `unknown`.

Następnie:

```python
if not username in recent_users:
    recent_users.append(username)
```

Jeśli użytkownika nie ma na liście, zostaje dodany.

### make_response

```python
resp = make_response(
    render_template("hello.html", username=username)
)
```

Tworzy obiekt odpowiedzi HTTP, który można dodatkowo modyfikować.

### set_cookie

```python
resp.set_cookie("username", username)
```

Ustawia ciasteczko o nazwie `username`.

Przeglądarka zapisze je i będzie przesyłać przy kolejnych odpowiednich żądaniach.

**Ważne:** to ciasteczko nie jest mechanizmem uwierzytelniania. Użytkownik może sam zmienić jego wartość.

Nie wolno traktować wartości ciasteczka `username` jako dowodu tożsamości użytkownika.

### Metoda GET

```python
username = request.cookies.get("username", "unknown")
```

Pobiera ciasteczko `username`.

Jeśli nie istnieje, używa wartości `unknown`.

To pokazuje różnicę:

| Kod | Co pobiera? |
|---|---|
| `request.form.get()` | Dane formularza POST. |
| `request.args.get()` | Parametry GET z URL. |
| `request.cookies.get()` | Ciasteczka przysłane przez przeglądarkę. |

## 8.5. Renderowanie Markdown — /render

```python
@app.route("/render", methods=['POST'])
def render():
    md = request.form.get("markdown", "")
    rendered = markdown.markdown(md)

    notes.append(rendered)

    return render_template("markdown.html", rendered=rendered)
```

Krok po kroku:

1. Użytkownik przesyła tekst Markdown.
2. Flask pobiera go przez `request.form.get()`.
3. Biblioteka Markdown przekształca tekst na HTML.
4. Wynik trafia do listy `notes`.
5. Wynik zostaje przekazany do szablonu `markdown.html`.

### Gdzie znajduje się potencjalna podatność XSS?

Ważna jest instrukcja:

```python
rendered = markdown.markdown(md)
```

Konwersja Markdown na HTML nie oznacza automatycznego oczyszczenia HTML.

Markdown często pozwala umieszczać w dokumencie również surowe znaczniki HTML.

Jeżeli użytkownik wprowadzi niebezpieczną zawartość, może ona przetrwać konwersję.

Następnie wynik jest przekazywany do szablonu.

Jeśli szablon wyświetla go z użyciem:

```jinja2
{{ rendered|safe }}
```

to przeglądarka zinterpretuje wynik jako HTML.

Jeżeli nie zastosowano sanitizacji, może powstać Stored XSS.

### Dlaczego Stored XSS?

Ponieważ wynik zostaje zapisany:

```python
notes.append(rendered)
```

i może być wyświetlany również innym użytkownikom.

## 8.6. Odczytywanie zapisanych notatek

```python
@app.route("/render/<rendered_id>")
def render_old(rendered_id):
```

Flask pobiera identyfikator z adresu URL.

Przykład:

```text
/render/1
```

Wartość `1` trafia do zmiennej `rendered_id`.

Następnie:

```python
if int(rendered_id) > len(notes):
    return "Wrong note id", 404
```

Sprawdza, czy identyfikator nie jest większy od liczby notatek.

Później:

```python
rendered = notes[int(rendered_id) - 1]
```

Pobiera notatkę z listy.

Dlaczego odejmujemy 1?

Ponieważ:
- Identyfikatory w URL zaczynają się tutaj od 1.
- Indeksy list Pythona zaczynają się od 0.

### Błąd w walidacji

Kod ma kilka problemów:

1. Nie sprawdza, czy identyfikator jest liczbą.
2. Dla wartości `0` użyje indeksu `-1`, czyli ostatniego elementu listy.
3. Dla wartości ujemnej może odczytać element z końca listy.
4. Przy pustej liście może wystąpić `IndexError`.

Poprawiona wersja:

```python
@app.route("/render/<rendered_id>")
def render_old(rendered_id):
    try:
        note_id = int(rendered_id)
    except ValueError:
        return "Wrong note id", 404

    if note_id < 1 or note_id > len(notes):
        return "Wrong note id", 404

    rendered = notes[note_id - 1]

    return render_template("markdown.html", rendered=rendered)
```

### Jak zabezpieczyć Markdown przed XSS?

Samo `markdown.markdown()` nie wystarczy.

Należy zastosować sprawdzoną bibliotekę do sanitizacji HTML, np. `nh3`, przed wyświetleniem wyniku jako HTML.

Przykład:

```python
import markdown
import nh3

md = request.form.get("markdown", "")

rendered = markdown.markdown(md)

rendered = nh3.clean(rendered)

notes.append(rendered)

return render_template("markdown.html", rendered=rendered)
```

W szablonie można wtedy wyświetlić oczyszczony HTML:

```jinja2
{{ rendered|safe }}
```

`safe` jest tutaj uzasadnione tylko dlatego, że wcześniej zastosowano sanitizację HTML odpowiednim narzędziem.

Sanitizację należy skonfigurować odpowiednio do potrzeb aplikacji i dozwolonych elementów HTML.

---

# 9. Analiza programu mod_python nr 2 — tablica ogłoszeń

Oryginalny program:

```python
#!/usr/bin/env python

import json

try:
    f = open("/tmp/wall.json", "r")
    wall = json.load(f)
except:
    wall = []

login_form = """
<html>
<form>
What is your name?
<input type=text name=user>
<br/>
<input type=submit name=login value=login>
</form>
</html>
"""

def index(req, user='', text=''):
    if user == '':
        return login_form

    if text != "":
        wall.append((user, text))

        f = open("/tmp/wall.json", "w")
        json.dump(wall, f)

    html = "<html><h2>wall</h2>"

    for post in wall:
        html += post[0] + " - " + post[1] + "<br/>"

    html += "<form>"
    html += '<p><input type=text name=text><input type=submit value=comment>'
    html += "<input type=hidden name=user value=" + user + ">"
    html += '<p><a href="wall.py">Exit</a></p>'

    html += "</html>"

    return html
```

Jest to prosta tablica ogłoszeń.

Użytkownik może:
- Podać swoją nazwę.
- Wprowadzać komentarze.
- Zapisywać komentarze w pliku JSON.
- Wyświetlać wcześniej dodane komentarze.

## 9.1. Odczyt danych z pliku JSON

```python
import json

try:
    f = open("/tmp/wall.json", "r")
    wall = json.load(f)
except:
    wall = []
```

Program próbuje odczytać zapisane komentarze.

`json.load(f)`:
- Odczytuje zawartość pliku.
- Przekształca JSON na obiekty Pythona.

Jeżeli wystąpi błąd, program tworzy pustą listę.

## 9.2. Formularz logowania

```python
login_form = """
<html>
<form>
What is your name?
<input type=text name=user>
<br/>
<input type=submit name=login value=login>
</form>
</html>
"""
```

Formularz pobiera nazwę użytkownika.

Nie jest to jednak prawdziwe logowanie.

Nie ma:
- Hasła.
- Weryfikacji tożsamości.
- Bezpiecznego mechanizmu sesji.
- Uwierzytelniania po stronie serwera.

Użytkownik może podać dowolną nazwę.

## 9.3. Funkcja index()

```python
def index(req, user='', text=''):
```

Przyjmuje:
- `req` – obiekt żądania.
- `user` – nazwę użytkownika.
- `text` – treść komentarza.

Wartości mogą pochodzić z parametrów GET lub POST obsługiwanych przez publisher.

### Sprawdzenie nazwy

```python
if user == '':
    return login_form
```

Jeżeli użytkownik nie podał nazwy, wyświetlany jest formularz.

### Dodawanie komentarza

```python
if text != "":
    wall.append((user, text))
```

Dodaje parę:

```python
(user, text)
```

do listy komentarzy.

Następnie zapisuje ją w pliku:

```python
f = open("/tmp/wall.json", "w")
json.dump(wall, f)
```

`json.dump()` zapisuje dane jako JSON.

## 9.4. Wyświetlanie komentarzy

Najważniejszy fragment:

```python
for post in wall:
    html += post[0] + " - " + post[1] + "<br/>"
```

Program łączy dane użytkowników i komentarze bezpośrednio z HTML.

Nie stosuje kodowania HTML.

To oznacza, że użytkownik może umieścić w komentarzu znaczniki HTML lub potencjalnie JavaScript.

Ponieważ komentarze są zapisywane w pliku i wyświetlane później, jest to przykład potencjalnego Stored XSS.

### Gdzie jest source?

Źródłem jest parametr:

```python
text
```

oraz nazwa użytkownika:

```python
user
```

### Gdzie jest sink?

Miejscem niebezpiecznego wykorzystania jest:

```python
html += post[0] + " - " + post[1] + "<br/>"
```

Dane są łączone z HTML bez kodowania.

## 9.5. Ukryte pole formularza

```python
html += "<input type=hidden name=user value=" + user + ">"
```

Pole `hidden` jest niewidoczne dla użytkownika, ale jego wartość jest przesyłana wraz z formularzem.

W tym przykładzie przechowuje nazwę użytkownika.

**Ważne:** ukryte pole nie jest zabezpieczeniem.

Użytkownik może zmienić jego wartość w narzędziach deweloperskich przeglądarki lub wysłać własne żądanie HTTP.

Nie wolno traktować go jako wiarygodnego źródła informacji o tożsamości użytkownika.

# 10. Podatności w programie nr 2

| Problem | Dlaczego jest niebezpieczny? | Rozwiązanie |
|---|---|---|
| Brak kodowania `user` | Możliwa manipulacja HTML. | Kodowanie HTML. |
| Brak kodowania `text` | Możliwy Stored XSS. | Kodowanie HTML lub bezpieczna sanitizacja. |
| Ukryte pole `user` | Możliwa zmiana nazwy użytkownika. | Weryfikacja tożsamości po stronie serwera. |
| Brak prawdziwego logowania | Każdy może podać cudzą nazwę. | Bezpieczne uwierzytelnianie. |
| Globalna lista `wall` | Problemy przy wielu użytkownikach i procesach. | Baza danych lub właściwy mechanizm współdzielenia danych. |
| Ogólny `except` | Ukrywa różne rodzaje błędów. | Obsługa konkretnych wyjątków. |
| Zapis bez kontroli współbieżności | Możliwość nadpisywania danych. | Baza danych i transakcje. |

## 10.1. Poprawiona wersja wyświetlania komentarzy

W wersji opartej na ręcznym składaniu HTML można użyć:

```python
import html

for post in wall:
    bezpieczny_user = html.escape(post[0], quote=True)
    bezpieczny_text = html.escape(post[1], quote=True)

    wynik += bezpieczny_user
    wynik += " - "
    wynik += bezpieczny_text
    wynik += "<br/>"
```

Teraz dane użytkownika będą wyświetlane jako tekst, a nie interpretowane jako HTML.

Analogicznie należy zabezpieczyć wartość w atrybucie formularza:

```python
bezpieczny_user = html.escape(user, quote=True)

html += (
    '<input type="hidden" name="user" value="'
    + bezpieczny_user
    + '">'
)
```

Zwróć uwagę na cudzysłowy wokół wartości `value`.

W praktyce lepiej jednak generować HTML za pomocą szablonów Jinja2 i korzystać z automatycznego kodowania.

---

# 11. Ćwiczenia dotyczące kradzieży danych — co trzeba rozumieć?

W materiałach pojawiają się trzy zadania:

1. Przekazywanie ciasteczek użytkownika do skryptu i zapisywanie ich w pliku.
2. Odczytywanie tajnej notatki użytkownika.
3. Modyfikowanie ciasteczek w celu uzyskania dostępu do konta innego użytkownika.

Są to przykłady wykorzystania XSS do naruszenia poufności i integralności danych.

Nie są to już tylko zmiany wyglądu strony.

## 11.1. Ciasteczka i przejęcie sesji

Mechanizm zagrożenia:

- Aplikacja przechowuje identyfikator sesji w ciasteczku.
- Przeglądarka automatycznie wysyła je do serwera.
- Jeżeli token zostanie skradziony, może zostać wykorzystany do uzyskania dostępu do sesji.
- Serwer może uznać osobę przedstawiającą token za zalogowanego użytkownika.

Dlatego token sesyjny musi być traktowany jak poufne hasło.

Zabezpieczenia:
- `HttpOnly`.
- `Secure`.
- `SameSite`.
- HTTPS.
- Odpowiednie zarządzanie sesją.
- Regenerowanie identyfikatora sesji po zalogowaniu.
- Unieważnianie sesji po wylogowaniu.

## 11.2. Odczytywanie tajnej notatki

Jeżeli aplikacja przechowuje notatkę w DOM, np.:

```html
<div id="secret">
    To jest testowa notatka.
</div>
```

JavaScript może odczytać jej tekst:

```javascript
const secret = document.getElementById("secret").textContent;

console.log(secret);
```

To pokazuje ważną właściwość XSS:

Jeśli złośliwy skrypt wykonuje się w kontekście strony, może mieć dostęp do elementów DOM dostępnych tej stronie.

`HttpOnly` nie zabezpiecza przed odczytem danych umieszczonych bezpośrednio w DOM.

Dlatego poufnych danych nie należy udostępniać stronie użytkownika, jeśli nie są mu potrzebne.

## 11.3. Modyfikowanie ciasteczek i podszywanie się pod użytkownika

W przykładzie Flask znajduje się:

```python
resp.set_cookie("username", username)
```

oraz:

```python
username = request.cookies.get("username", "unknown")
```

Oznacza to, że aplikacja odczytuje nazwę użytkownika bezpośrednio z ciasteczka.

Problem polega na tym, że użytkownik może sam zmienić ciasteczko.

Jeżeli aplikacja traktuje jego zawartość jako dowód zalogowania, można podszyć się pod inną osobę.

**To nie jest bezpieczne uwierzytelnianie.**

Prawidłowa aplikacja powinna:
- Weryfikować użytkownika po stronie serwera.
- Używać odpowiedniego mechanizmu sesji.
- Nie ufać wartościom przesyłanym przez klienta.
- Chronić token sesyjny.
- Nie przechowywać uprawnień w zwykłym, edytowalnym ciasteczku.

---

# 12. Przydatne funkcje JavaScript i Flask

| Funkcja | Zastosowanie |
|---|---|
| `document.cookie` | Odczytywanie i zapisywanie ciasteczek dostępnych dla JavaScript. |
| `document.getElementById()` | Pobieranie elementu HTML po ID. |
| `element.textContent` | Odczyt lub zapis tekstu elementu. |
| `element.innerHTML` | Odczyt lub zapis HTML elementu. |
| `window.location.href` | Odczyt lub zmiana adresu strony. |
| `encodeURIComponent()` | Kodowanie wartości parametru URL. |
| `console.log()` | Wyświetlanie informacji w konsoli. |
| `request.args.get()` | Pobieranie parametrów GET we Flasku. |
| `request.form.get()` | Pobieranie danych formularza POST. |
| `request.cookies.get()` | Pobieranie ciasteczek we Flasku. |
| `resp.set_cookie()` | Ustawianie ciasteczka w odpowiedzi Flask. |
| `render_template()` | Renderowanie szablonu HTML. |
| `html.escape()` | Kodowanie znaków specjalnych HTML w Pythonie. |
| `markdown.markdown()` | Konwersja Markdown do HTML. |
| `json.load()` | Odczytywanie JSON z pliku. |
| `json.dump()` | Zapisywanie JSON do pliku. |

# 13. XSS Game — praktyczne ćwiczenia

Strona:

https://xss-game.appspot.com/

To edukacyjna gra pozwalająca ćwiczyć rozpoznawanie i wykorzystywanie podatności XSS w przygotowanych zadaniach.

Podczas rozwiązywania zwracaj uwagę na:

1. Skąd pochodzą dane użytkownika?
2. Czy dane są przetwarzane przez serwer, czy przez JavaScript?
3. Gdzie trafiają dane?
4. Czy są interpretowane jako HTML?
5. Czy występuje `innerHTML`?
6. Czy aplikacja zapisuje dane w bazie lub innym trwałym magazynie?
7. Czy przeglądarka wykonuje kod w kontekście podatnej strony?
8. Jak można naprawić podatność?

Najważniejsze jest nie tylko znalezienie sposobu wywołania XSS, ale również zrozumienie, dlaczego podatność istnieje.

---

# 14. Najważniejsze rzeczy do zapamiętania na zaliczenie

| Pytanie | Odpowiedź |
|---|---|
| Co robi mod_python? | Umożliwia wykonywanie kodu Python przez Apache. |
| Co robi PythonHandler? | Określa handler obsługujący pliki Python. |
| Co robi mod_python.publisher? | Udostępnia funkcje Pythona jako endpointy. |
| Jak przekazywane są parametry GET w publisher? | Mogą trafiać bezpośrednio do argumentów funkcji. |
| Skąd bierze się XSS w welcome.py? | Z bezpośredniego wstawiania `name` do HTML. |
| Jak naprawić welcome.py? | Zastosować `html.escape()`. |
| Jak zmienić tło strony? | Przez `document.body.style.backgroundColor`. |
| Jak przekierować użytkownika? | Przez `window.location.href`. |
| Jak odczytać ciasteczka? | Przez `document.cookie`, z wyjątkiem ciasteczek HttpOnly. |
| Jak ustawić ciasteczko? | Przez `document.cookie = "nazwa=wartość; Path=/"`. |
| Jak odczytać tekst elementu HTML? | `element.textContent`. |
| Jak odczytać HTML elementu? | `element.innerHTML`. |
| Jak pobrać element po ID? | `document.getElementById()`. |
| Jak pobrać parametr GET we Flasku? | `request.args.get()`. |
| Jak pobrać dane POST? | `request.form.get()`. |
| Jak pobrać cookie we Flasku? | `request.cookies.get()`. |
| Jak ustawić cookie we Flasku? | `response.set_cookie()`. |
| Co robi markdown.markdown()? | Zamienia Markdown na HTML. |
| Czy konwersja Markdown zabezpiecza przed XSS? | Nie. |
| Co robi `safe` w Jinja2? | Wyłącza automatyczne kodowanie HTML. |
| Co robi html.escape()? | Zamienia znaki specjalne HTML na encje. |
| Co oznacza Stored XSS? | Niebezpieczna treść jest zapisana i wyświetlana kolejnym użytkownikom. |
| Dlaczego hidden input nie jest bezpieczny? | Użytkownik może zmienić jego wartość. |
| Dlaczego username w cookie nie wystarcza do logowania? | Klient może samodzielnie zmienić ciasteczko. |
| Co daje HttpOnly? | Blokuje odczyt ciasteczka przez JavaScript. |

# 15. Najważniejszy schemat myślenia

**XSS:**

`Dane użytkownika → niezabezpieczone przetwarzanie → HTML/DOM → interpretacja przez przeglądarkę → wykonanie niepożądanego kodu`

**Stored XSS:**

`Dane użytkownika → zapis w bazie/pliku → późniejsze wyświetlenie → wykonanie kodu u odwiedzającego`

**Reflected XSS:**

`Parametr żądania → odpowiedź serwera → interpretacja przez przeglądarkę`

**DOM XSS:**

`Dane dostępne w przeglądarce → JavaScript → niebezpieczny sink (np. innerHTML) → interpretacja`

**Ochrona:**

`Niezaufane dane → kodowanie lub sanitizacja odpowiednia do kontekstu → bezpieczne wyświetlenie`

Najważniejsza zasada: nie ufaj danym użytkownika, nie traktuj ciasteczek jako wiarygodnego źródła tożsamości i nie pozwalaj, aby niezaufane dane były interpretowane jako HTML lub JavaScript.