# XSS, SOP, ciasteczka, Flask

## 1. Czym jest XSS?

**XSS (Cross-Site Scripting)** to podatność polegająca na tym, że aplikacja internetowa pozwala potraktować niezaufane dane jako aktywną treść strony, np. kod HTML lub JavaScript.

Najważniejszy model ataku:

1. **Źródło danych (source)** – miejsce, z którego pochodzą niezaufane dane, np. parametr URL, formularz, komentarz.
2. **Miejsce interpretacji (sink)** – miejsce, w którym przeglądarka interpretuje te dane jako HTML lub JavaScript, np. `innerHTML`.
3. **Skutek** – przeglądarka wykonuje niepożądane działanie w kontekście podatnej strony.

Przykład:

```javascript
const dane = new URLSearchParams(location.search).get("tekst");
document.getElementById("wynik").innerHTML = dane;
```

Jeśli użytkownik poda HTML zamiast zwykłego tekstu, przeglądarka może potraktować go jako elementy strony.

**Kluczowe:** problemem nie jest samo przesłanie danych przez użytkownika, ale sposób ich późniejszego wykorzystania.

## 2. Rodzaje XSS

### Reflected XSS (XSS odbity)

Dane z żądania użytkownika są bezpośrednio umieszczane w odpowiedzi serwera.

Przykład:
- Użytkownik otwiera adres z odpowiednio spreparowanym parametrem.
- Serwer odczytuje parametr i umieszcza go w odpowiedzi HTML.
- Przeglądarka interpretuje otrzymaną zawartość.

Atak zwykle wymaga nakłonienia ofiary do otwarcia spreparowanego linku.

### Stored XSS (XSS zapisany)

Złośliwe dane zostają zapisane w aplikacji, np. w bazie danych.

Przykład:
- Atakujący dodaje komentarz zawierający niebezpieczną treść.
- Aplikacja zapisuje komentarz.
- Kolejne osoby otwierające stronę z komentarzami mogą uruchomić niepożądany kod.

Jest szczególnie niebezpieczny, ponieważ nie trzeba każdej ofiary osobno nakłaniać do otwarcia spreparowanego linku.

### DOM-based XSS

Podatność powstaje w kodzie JavaScript wykonywanym po stronie przeglądarki.

Przykład:
- JavaScript pobiera dane z adresu URL.
- Następnie przekazuje je do `innerHTML`.
- Przeglądarka interpretuje je jako HTML.

DOM XSS opisuje przede wszystkim miejsce i sposób powstania podatności. Może współwystępować z XSS odbitym lub zapisanym.

### Kto wykonuje skrypt i z jakimi uprawnieniami?

Skrypt wykonuje **przeglądarka ofiary**, a nie serwer.

Kod działa w kontekście originu podatnej strony, czyli może korzystać z uprawnień dostępnych dla JavaScript tej strony, np.:
- Odczytywać i modyfikować DOM.
- Wysyłać żądania do serwera.
- Odczytywać dane dostępne dla JavaScript w ramach originu.
- Wykonywać działania w imieniu zalogowanego użytkownika.

Nie oznacza to automatycznego dostępu do wszystkich plików, haseł czy danych przeglądarki.

## 3. innerHTML a textContent

To ważne rozróżnienie dotyczące DOM.

```javascript
const dane = '<b>Próba</b>';

const pole = document.createElement('div');

pole.innerHTML = dane;
```

Efekt: przeglądarka utworzy element HTML `<b>`, więc tekst „Próba” będzie pogrubiony.

Porównaj:

```javascript
pole.textContent = dane;
```

Efekt: przeglądarka wyświetli dosłownie:

`<b>Próba</b>`

Nie utworzy elementu HTML.

### Najważniejsza różnica

| Właściwość | Działanie |
|---|---|
| `innerHTML` | Interpretuje zawartość jako HTML. |
| `textContent` | Traktuje zawartość jako zwykły tekst. |

Dlatego przy wyświetlaniu niezaufanych danych tekstowych należy preferować `textContent`.

### Dlaczego `<script>` w innerHTML zwykle się nie wykonuje, ale onerror może?

Przeglądarki mają specjalne zachowanie dotyczące elementów `<script>` tworzonych przez mechanizm `innerHTML`. Tak utworzone skrypty zwykle nie są wykonywane.

Nie oznacza to jednak, że `innerHTML` jest bezpieczne.

Inne elementy HTML mogą zawierać aktywne mechanizmy, np. atrybuty zdarzeń:

- `onerror`
- `onload`
- `onclick`

Przeglądarka może wykonać kod przypisany do takiego zdarzenia, kiedy wystąpi odpowiednia sytuacja.

Przykładowo `onerror` może zostać wywołany, gdy element obrazu nie może załadować zasobu.

**Wniosek:** brak wykonania znacznika `<script>` nie oznacza braku podatności XSS. Nie należy traktować `innerHTML` jako bezpiecznego miejsca do wstawiania niezaufanych danych.

## 4. Same-Origin Policy (SOP)

**SOP (Same-Origin Policy)** to mechanizm bezpieczeństwa przeglądarki ograniczający dostęp do zasobów pochodzących z innych originów.

Origin składa się z trzech elementów:

1. **Scheme (schemat/protokół)** – np. `http`, `https`.
2. **Host (host)** – np. `example.com`, `localhost`.
3. **Port** – np. `80`, `443`, `8000`.

Przykłady:

| Adresy | Ten sam origin? |
|---|---|
| `http://example.com/a` i `http://example.com/b` | TAK |
| `http://example.com` i `https://example.com` | NIE |
| `http://localhost:8000` i `http://localhost:8001` | NIE |
| `https://example.com` i `https://sub.example.com` | NIE |
| `http://example.com` i `http://example.org` | NIE |

Ścieżka (`/a`, `/b`) nie ma znaczenia dla originu.

### A co z ciasteczkami i protokołem?

To ważne: **ciasteczka działają według innych zasad niż Same-Origin Policy.**

Ciasteczka:
- Nie są izolowane według numeru portu.
- Są powiązane z domeną/hostem i ścieżką (`Path`).
- Mogą mieć ograniczenia dotyczące bezpiecznego transportu (`Secure`).
- Nie są zwyczajnie współdzielone pomiędzy różnymi hostami, ale atrybut `Domain` może rozszerzyć ich dostępność na subdomeny.

**Czy ciasteczka ignorują również protokół?**

Nie do końca.

Ciasteczka nie mają osobnego, ogólnego mechanizmu izolacji według protokołu takiego jak SOP. Jednak istnieje atrybut `Secure`.

- Ciasteczko z `Secure` jest wysyłane tylko przez bezpieczne połączenie, zasadniczo HTTPS.
- Ciasteczko bez `Secure` może być wysyłane również przez HTTP.
- Samo `HttpOnly` nie wpływa na protokół ani transport.

Czyli:
- `http://example.com` i `https://example.com` to różne originy.
- Ciasteczko bez `Secure` może być wysyłane zarówno przez HTTP, jak i HTTPS.
- Ciasteczko z `Secure` nie powinno być wysyłane przez HTTP.

**Do zapamiętania:** SOP uwzględnia schemat, host i port. Ciasteczka nie uwzględniają portu, a ograniczenie transportu HTTPS realizuje atrybut `Secure`.

## 5. Ciasteczka i sesje

Ciasteczko (cookie) to niewielka ilość danych przechowywana przez przeglądarkę i wysyłana do serwera przy odpowiednich żądaniach.

Często przechowuje się w nim identyfikator sesji.

### Sesja jako token okaziciela

Przykład:

```text
session_id=abc123
```

Serwer rozpoznaje użytkownika na podstawie identyfikatora sesji.

Taki identyfikator można traktować jak **token okaziciela (bearer token)**.

Oznacza to, że osoba posiadająca token może potencjalnie korzystać z sesji użytkownika.

Dlatego kradzież ciasteczka sesyjnego może umożliwić przejęcie zalogowanej sesji.

### Najważniejsze atrybuty ciasteczek

| Atrybut | Znaczenie |
|---|---|
| `HttpOnly` | Blokuje dostęp do ciasteczka przez JavaScript, np. `document.cookie`. |
| `Secure` | Ogranicza wysyłanie ciasteczka do bezpiecznego transportu HTTPS. |
| `SameSite` | Ogranicza wysyłanie ciasteczka w kontekście żądań cross-site. |

#### HttpOnly

Chroni przed bezpośrednim odczytaniem ciasteczka przez JavaScript.

Nie blokuje jednak XSS jako takiego. Złośliwy skrypt nadal może wykonywać żądania w imieniu użytkownika, a przeglądarka może automatycznie dołączać ciasteczko do odpowiednich żądań.

#### Secure

Zapewnia, że ciasteczko jest przesyłane przez bezpieczne połączenie HTTPS.

Nie chroni przed XSS.

#### SameSite

Ogranicza wysyłanie ciasteczek w żądaniach cross-site.

Najważniejsze wartości:

- `Strict` – ciasteczko jest wysyłane tylko w kontekście same-site.
- `Lax` – dopuszcza część nawigacji cross-site, np. typowe przejście metodą GET.
- `None` – pozwala na wysyłanie w kontekście cross-site; wymaga `Secure`.

SameSite pomaga ograniczać ataki CSRF, ale nie zastępuje innych zabezpieczeń.

**Ważne:** żaden z tych atrybutów nie usuwa podatności XSS.

## 6. Kodowanie danych wyjściowych (Output Encoding)

Podstawowa zasada:

**Niezaufane dane należy kodować odpowiednio do miejsca, w którym zostaną umieszczone.**

Jeśli chcemy wyświetlić tekst zawierający znaki specjalne, musimy zapobiec potraktowaniu go jako HTML.

Przykładowo:

```html
<script>alert(1)</script>
```

Nie powinien zostać zinterpretowany jako skrypt, jeśli ma być wyświetlony jako zwykły tekst.

### Python — html.escape

W Pythonie można użyć:

```python
import html

dane = '<b>Test</b>'

bezpieczne = html.escape(dane)

print(bezpieczne)
```

Wynik:

```text
&lt;b&gt;Test&lt;/b&gt;
```

Najważniejsze zamiany:
- `<` na `&lt;`
- `>` na `&gt;`
- `&` na `&amp;`
- `"` na `&quot;` (domyślnie)
- `'` na `&#x27;` (domyślnie)

Dzięki temu przeglądarka wyświetla znaki zamiast interpretować je jako znaczniki HTML.

### Jinja2 — automatyczne kodowanie

Flask korzysta z silnika szablonów Jinja2.

Przykład:

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", dane="<b>Test</b>")
```

W szablonie:

```html
<p>{{ dane }}</p>
```

Jinja2 w typowej konfiguracji szablonów HTML automatycznie koduje wartości.

Dzięki temu `<b>Test</b>` zostanie wyświetlone jako tekst.

### Filtr |safe

Przykład:

```html
<p>{{ dane|safe }}</p>
```

Filtr `safe` mówi Jinja2, aby nie kodować automatycznie danej wartości.

Przeglądarka może wtedy zinterpretować zawartość jako HTML.

**Nie używaj `|safe` dla niezaufanych danych**, chyba że zostały wcześniej odpowiednio oczyszczone (sanitized) przy użyciu sprawdzonego narzędzia.

## 7. Kontekst wstawienia danych

Samo kodowanie HTML nie wystarcza w każdym przypadku.

Dane należy zabezpieczyć zależnie od miejsca, w którym je umieszczamy.

### Treść HTML

Przykład:

```html
<p>DANE_UŻYTKOWNIKA</p>
```

Tutaj stosujemy kodowanie HTML.

### Atrybut HTML

Przykład:

```html
<input value="DANE_UŻYTKOWNIKA">
```

Wartość musi być odpowiednio kodowana dla atrybutu HTML. Należy również zawsze stosować cudzysłowy wokół wartości atrybutów.

### Kod JavaScript

Przykład:

```html
<script>
    const dane = "DANE_UŻYTKOWNIKA";
</script>
```

Nie należy po prostu wklejać niezaufanych danych do kodu JavaScript.

Kodowanie HTML nie zabezpiecza automatycznie kontekstu JavaScript. Najlepiej przekazywać dane przez bezpieczny mechanizm, np. `tojson` w Jinja2:

```html
<script>
    const dane = {{ dane|tojson }};
</script>
```

### Adres URL

Przykład:

```html
<a href="DANE_UŻYTKOWNIKA">Link</a>
```

Należy:
- Kodować dane odpowiednio do składni URL.
- Sprawdzać, czy schemat adresu jest dozwolony, np. `https` lub `http`.
- Nie dopuszczać niebezpiecznych schematów, np. `javascript:`.

**Wniosek:** kodowanie musi odpowiadać kontekstowi. Nie istnieje jedno uniwersalne kodowanie, które zabezpiecza wszystkie miejsca.

## 8. Content Security Policy (CSP)

**CSP (Content Security Policy)** to dodatkowy mechanizm ochrony strony internetowej, który ogranicza, skąd mogą pochodzić zasoby i jakie skrypty mogą być wykonywane.

CSP jest przekazywane najczęściej przez nagłówek HTTP.

Przykład:

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'
```

Znaczenie dyrektyw:

| Dyrektywa | Znaczenie |
|---|---|
| `default-src` | Domyślna reguła dla wielu rodzajów zasobów. |
| `script-src` | Określa dozwolone źródła skryptów. |
| `object-src` | Określa dozwolone źródła elementów typu object/embed. |
| `base-uri` | Ogranicza dozwolone adresy w znaczniku `<base>`. |

### Co oznacza 'self'?

`'self'` oznacza ten sam origin, czyli ten sam:
- Schemat.
- Host.
- Port.

### Co oznacza 'none'?

`'none'` oznacza, że dane źródło jest zabronione.

### Skrypty inline

Przy polityce:

```http
script-src 'self'
```

Przeglądarka:
- Pozwala na skrypty pochodzące z tego samego originu.
- Blokuje zwykłe skrypty inline, np. `<script>alert(1)</script>`.
- Blokuje atrybuty zdarzeń, np. `onclick`, `onerror`.

Dozwalanie skryptów inline wymagałoby dodatkowych mechanizmów, np. nonce lub hashy, albo niezalecanego `'unsafe-inline'`.

### Czy CSP zastępuje kodowanie?

Nie.

CSP jest dodatkową warstwą zabezpieczeń. Może ograniczyć skutki niektórych ataków XSS, ale nie zastępuje:
- Kodowania wyjścia.
- Walidacji danych.
- Bezpiecznego korzystania z DOM.
- Odpowiedniego projektowania aplikacji.

## 9. Flask — najważniejsze elementy

Flask to lekki framework Pythona do tworzenia aplikacji internetowych.

### Trasy — @app.route

Dekorator określający, pod jakim adresem dostępna jest funkcja.

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Witaj!"
```

Po wejściu na `/` zostanie wywołana funkcja `index()`.

### request.args

Służy do odczytywania parametrów przekazanych w adresie URL metodą GET.

Przykład adresu:

```text
http://localhost:5000/?imie=Jan
```

Kod:

```python
from flask import request

@app.route("/")
def index():
    imie = request.args.get("imie")
    return f"Witaj, {imie}"
```

`request.args.get("imie")` pobiera wartość parametru `imie`.

Pamiętaj, że dane z żądania są niezaufane.

### render_template

Służy do renderowania szablonów HTML przy użyciu Jinja2.

```python
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html", imie="Jan")
```

W szablonie:

```html
<h1>Witaj, {{ imie }}</h1>
```

### session

Służy do przechowywania danych sesji użytkownika.

```python
from flask import session

app.secret_key = "tajny-klucz"

@app.route("/login")
def login():
    session["user"] = "Jan"
    return "Zalogowano"
```

We Flasku domyślna sesja jest przechowywana po stronie klienta w podpisanym ciasteczku.

**Ważne:** podpis zapewnia integralność, ale nie szyfruje zawartości. Nie należy przechowywać w nim poufnych danych.

### app.config

Służy do konfiguracji aplikacji.

Przykład:

```python
app.config["SECRET_KEY"] = "tajny-klucz"
```

Można również ustawiać konfigurację ciasteczek sesyjnych:

```python
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
```

Powyższe ustawienia powinny być dostosowane do środowiska aplikacji. `SESSION_COOKIE_SECURE = True` wymaga HTTPS przy normalnym korzystaniu z ciasteczka.

### @app.after_request

Pozwala wykonać kod po obsłużeniu żądania, ale przed wysłaniem odpowiedzi do klienta.

Można wykorzystać go np. do dodawania nagłówków bezpieczeństwa.

```python
@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "object-src 'none'; "
        "base-uri 'none'"
    )

    return response
```

W ten sposób odpowiedź otrzymuje nagłówek CSP.

## 10. curl — podstawowe parametry

`curl` to narzędzie wiersza poleceń do wysyłania żądań HTTP i HTTPS.

### -i

Pokazuje nagłówki odpowiedzi razem z treścią.

```bash
curl -i http://localhost:5000/
```

Przydatne do sprawdzania:
- Statusu HTTP.
- Nagłówków odpowiedzi.
- Ciasteczek.
- CSP.

### -b

Pozwala wysłać ciasteczko w żądaniu.

```bash
curl -b "session=abc123" http://localhost:5000/
```

Można też podać plik z ciasteczkami:

```bash
curl -b cookies.txt http://localhost:5000/
```

### -d

Wysyła dane w treści żądania, domyślnie metodą POST.

```bash
curl -d "imie=Jan&wiek=20" http://localhost:5000/
```

Domyślnie `curl -d` wysyła dane jako `application/x-www-form-urlencoded`.

## 11. Kodowanie znaków w adresie URL

Adresy URL mają określoną składnię. Niektóre znaki mają w nich specjalne znaczenie, dlatego wartości parametrów należy odpowiednio kodować.

Przykład:

```javascript
const wartosc = "Ala ma kota & psa";

const zakodowana = encodeURIComponent(wartosc);

console.log(zakodowana);
```

Wynik:

```text
Ala%20ma%20kota%20%26%20psa
```

Najważniejsze:
- Spacja zostaje zakodowana jako `%20`.
- `&` zostaje zakodowane jako `%26`.
- `=` zostaje zakodowane jako `%3D`.
- `?` zostaje zakodowane jako `%3F`.

### encodeURIComponent a XSS

`encodeURIComponent()` nie jest zabezpieczeniem przed XSS.

Jego zadaniem jest zakodowanie wartości tak, aby można ją było bezpiecznie umieścić w części parametru URL.

Nie sprawia jednak, że dane są bezpieczne, jeśli później zostaną np. wstawione do `innerHTML`.

Kodowanie URL i kodowanie HTML to dwie różne rzeczy.

---

# 12. Najważniejsze rzeczy do zapamiętania

| Pojęcie | Najważniejsza informacja |
|---|---|
| XSS | Niezaufane dane zostają zinterpretowane jako aktywna treść strony. |
| Reflected XSS | Dane wracają w odpowiedzi na bieżące żądanie. |
| Stored XSS | Dane są zapisane i mogą trafiać do wielu użytkowników. |
| DOM XSS | Podatność powstaje w kodzie JavaScript przeglądarki. |
| Source | Źródło niezaufanych danych. |
| Sink | Miejsce, w którym dane są interpretowane jako kod lub HTML. |
| SOP | Origin = schemat + host + port. |
| Cookies | Nie są izolowane według portu. |
| Secure | Ciasteczko wysyłane przez HTTPS. |
| HttpOnly | JavaScript nie może bezpośrednio odczytać ciasteczka. |
| SameSite | Ogranicza wysyłanie ciasteczek cross-site. |
| innerHTML | Interpretuje zawartość jako HTML. |
| textContent | Traktuje zawartość jako zwykły tekst. |
| html.escape | Koduje znaki specjalne HTML w Pythonie. |
| Jinja2 | Domyślnie koduje dane w typowych szablonach HTML. |
| `\|safe` | Wyłącza automatyczne kodowanie Jinja2. |
| CSP | Ogranicza źródła i sposób wykonywania zasobów. |
| request.args | Pobiera parametry GET we Flasku. |
| render_template | Renderuje szablon HTML. |
| session | Obsługuje sesję użytkownika. |
| app.config | Konfiguruje aplikację Flask. |
| after_request | Pozwala zmodyfikować odpowiedź przed wysłaniem. |
| curl -i | Pokazuje nagłówki i treść odpowiedzi. |
| curl -b | Wysyła ciasteczka. |
| curl -d | Wysyła dane, domyślnie POST. |
| encodeURIComponent | Koduje wartość parametru URL, ale nie zabezpiecza przed XSS. |

## 13. Krótka ściąga — jak myśleć o bezpieczeństwie?

1. **Dane od użytkownika są niezaufane.** Nawet jeśli pochodzą z bazy danych, mogły wcześniej zostać wprowadzone przez atakującego.
2. **Zwracaj uwagę na source i sink.** Samo pobranie danych nie oznacza podatności. Problem pojawia się przy niebezpiecznym wykorzystaniu.
3. **Do tekstu używaj textContent.** Nie wstawiaj niezaufanych danych do innerHTML.
4. **Koduj dane zależnie od kontekstu.** HTML, atrybut, JavaScript i URL wymagają innych metod.
5. **Nie używaj bezmyślnie `|safe`.** Może wyłączyć ważną ochronę Jinja2.
6. **Pamiętaj o SOP.** Schemat, host i port muszą być identyczne, aby originy były takie same.
7. **Pamiętaj o ciasteczkach.** Nie izolują ich porty, a atrybut Secure ogranicza ich wysyłanie do HTTPS.
8. **HttpOnly nie rozwiązuje XSS.** Utrudnia kradzież ciasteczka, ale skrypt nadal może wykonywać działania w imieniu użytkownika.
9. **CSP to dodatkowa ochrona.** Nie zastępuje prawidłowego kodowania i bezpiecznego przetwarzania danych.
10. **Kodowanie URL nie jest ochroną XSS.** `encodeURIComponent()` i `html.escape()` rozwiązują różne problemy.

**Najważniejsza zasada całego tematu: nigdy nie ufaj danym użytkownika i nigdy nie pozwalaj, aby niezaufane dane były bez odpowiedniego zabezpieczenia interpretowane jako kod.**