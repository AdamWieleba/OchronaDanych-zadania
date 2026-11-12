# mod_python a Flask
if __name__ == "__main__":  
. . . app.run(debug=True)  
jest wymagane żeby po [python app.py] serwer się uruchomił na  
http://127.0.0.1:5000  
  
if __name__ == "__main__": . sprawdza, czy plik uruchomiono bezpośrednio, a nie zaimportowano z innego pliku.  
app.run(debug=True) . startuje lokalny serwer Flask w trybie debugowania. Zmiany w kodzie mogą automatycznie go restartować, a błędy są wyświetlane szczegółowo.  

## 1. Najważniejsza różnica między mod_python a Flask

W mod_python.publisher można było napisać:

```python
def index(req, name=''):
    ...
```

Parametr `name` był automatycznie pobierany z żądania HTTP i przekazywany do funkcji.

We Flasku trzeba pobrać go samodzielnie:

```python
name = request.args.get("name", "")
```

`request.args` przechowuje parametry GET przesłane w adresie URL.

Przykładowo:

```text
/welcome?name=Jan
```

Spowoduje, że:

```python
name = request.args.get("name", "")
```

ustawi zmienną `name` na `Jan`.

## 2. Pierwszy program — co się zmieniło?

### Oryginał

Formularz:

```html
<form action="welcome.py" method="GET">
    <input type="text" name="name">
    <input type="submit" value="Send">
</form>
```

Wysyłał dane do pliku `welcome.py`.

### Flask

Zmieniliśmy adres na:

```html
<form action="/welcome" method="GET">
```

Dlaczego?

Ponieważ we Flasku nie wywołujemy bezpośrednio pliku Python. Zamiast tego definiujemy trasę:

```python
@app.route("/welcome")
def welcome():
```

To oznacza, że wejście na `/welcome` uruchomi funkcję `welcome()`.

### Pobieranie parametru

```python
name = request.args.get("name", "")
```

Odpowiednik automatycznego przekazania argumentu `name` w mod_python.publisher.

### Generowanie odpowiedzi

```python
html = "<html>"
html += "Hello " + name
html += "<p>Nice to meet you..</p>"
html += "</html>"

return html
```

Logika pozostała taka sama jak w oryginale.

Flask po prostu zwraca wygenerowany HTML do przeglądarki.

## 3. Drugi program — co się zmieniło?

### 3.1. Formularz logowania

Oryginalnie formularz był zapisany bezpośrednio w zmiennej:

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

We Flasku przenieśliśmy go do osobnego pliku:

```text
templates/login.html
```

A następnie wyświetlamy go za pomocą:

```python
return render_template("login.html")
```

`render_template()` służy do wyświetlania plików HTML znajdujących się w katalogu `templates`.

### 3.2. Pobieranie danych formularza

W mod_python:

```python
def index(req, user='', text=''):
```

Parametry `user` i `text` były przekazywane automatycznie.

We Flasku:

```python
user = request.args.get("user", "")
text = request.args.get("text", "")
```

Oba parametry są przesyłane metodą GET, dlatego korzystamy z `request.args`.

### 3.3. Sprawdzanie użytkownika

Oryginał:

```python
if user == '':
    return login_form
```

Flask:

```python
if user == "":
    return render_template("login.html")
```

Logika jest identyczna. Jeżeli użytkownik nie poda nazwy, wyświetlamy formularz.

### 3.4. Dodawanie komentarza

Oryginał:

```python
if text != "":
    wall.append((user, text))

    f = open("/tmp/wall.json", "w")
    json.dump(wall, f)
```

Flask:

```python
if text != "":
    wall.append((user, text))

    f = open("/tmp/wall.json", "w")
    json.dump(wall, f)
```

Tutaj praktycznie nic się nie zmieniło.

- `wall.append()` dodaje komentarz do listy.
- `open()` otwiera plik do zapisu.
- `json.dump()` zapisuje listę do pliku JSON.

### 3.5. Wyświetlanie komentarzy

Oryginał:

```python
for post in wall:
    html += post[0] + " - " + post[1] + "<br/>"
```

We Flasku pozostaje dokładnie tak samo.

`post` jest krotką zawierającą:

```python
(user, text)
```

Dlatego:

- `post[0]` oznacza autora komentarza.
- `post[1]` oznacza treść komentarza.

### 3.6. Formularz dodawania komentarzy

Oryginał:

```python
html += "<form>"
html += '<p><input type=text name=text><input type=submit value=comment>'
html += "<input type=hidden name=user value=" + user + ">"
```

We Flasku:

```python
html += "<form action='/wall' method='GET'>"
html += '<p><input type="text" name="text">'
html += '<input type="submit" value="comment">'
html += "<input type='hidden' name='user' value=" + user + ">"
html += "</form>"
```

Dodaliśmy:
- `action='/wall'` — formularz wysyła dane do trasy `/wall`.
- `method='GET'` — dane zostaną przesłane w adresie URL.

Pole:

```html
<input type="hidden" name="user">
```

nadal przekazuje nazwę użytkownika razem z komentarzem.

### 3.7. Wyjście z tablicy

Oryginał:

```html
<a href="wall.py">Exit</a>
```

Flask:

```html
<a href="/">Exit</a>
```

Po kliknięciu użytkownik wraca na stronę główną, gdzie znajduje się formularz podania nazwy.

## 4. Porównanie mod_python i Flask

| mod_python | Flask | Znaczenie |
|---|---|---|
| `def index(req, name='')` | `def welcome():` | Funkcja obsługująca żądanie. |
| Automatyczne argumenty funkcji | `request.args.get()` | Pobieranie parametrów GET. |
| Zwracanie HTML przez `return` | Zwracanie HTML przez `return` | Odpowiedź dla przeglądarki. |
| HTML zapisany w zmiennej | `render_template()` | Wyświetlanie szablonu HTML. |
| Adres pliku `.py` | `@app.route()` | Definiowanie adresu aplikacji. |

## 5. Jak uruchomić programy?

1. Zainstaluj Flask:

```bash
pip install flask
```

2. Utwórz odpowiednią strukturę katalogów:

```text
projekt/
├── app.py
└── templates/
    └── welcome.html
```

Dla drugiego programu zamiast `welcome.html` potrzebujesz `login.html`.

3. Uruchom aplikację:

```bash
python app.py
```

4. Otwórz przeglądarkę:

```text
http://127.0.0.1:5000/
```

## 6. Ważna uwaga dotycząca oryginalnej logiki

Oba programy zostały przepisane bez dodawania zabezpieczeń.

Oznacza to, że zachowują również oryginalne problemy:

- Pierwszy program bezpośrednio wstawia `name` do HTML.
- Drugi program bezpośrednio wstawia `user` i `text` do HTML.
- Drugi program przechowuje nazwę użytkownika w ukrytym polu formularza.
- Nazwa użytkownika nie jest w żaden sposób uwierzytelniana.
- Dane komentarzy są zapisywane i później wyświetlane, więc drugi program może być podatny na Stored XSS.

To celowe — chodzi o zachowanie prostoty i oryginalnego działania przykładów, aby można było porównać je z wersjami opartymi na mod_python.