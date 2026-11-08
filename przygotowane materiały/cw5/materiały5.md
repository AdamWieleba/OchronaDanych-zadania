# Bezpieczeństwo serwera usług WWW

## 1. Żądanie i odpowiedź HTTP

### Czym jest HTTP?

HTTP (Hypertext Transfer Protocol) to protokół komunikacyjny wykorzystywany do przesyłania danych pomiędzy klientem (np. przeglądarką) a serwerem WWW (np. Apache).

Komunikacja odbywa się według modelu:
1. Klient wysyła żądanie HTTP (request).
2. Serwer odbiera żądanie i wykonuje odpowiednie operacje.
3. Serwer zwraca odpowiedź HTTP (response).

### Adres URL

URL (Uniform Resource Locator) określa lokalizację zasobu w sieci.

Przykład:

`http://127.0.0.1:8080/katalog/plik.html`

Składa się z:
- `http` – protokół komunikacji.
- `127.0.0.1` – adres serwera (localhost, czyli komputer lokalny).
- `8080` – port, na którym nasłuchuje serwer.
- `/katalog/plik.html` – ścieżka do żądanego zasobu.

### Żądanie HTTP (request)

Przykładowe żądanie:

```http
GET /index.html HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: Mozilla/5.0
Accept: text/html
```

Elementy żądania:
- **GET** – metoda HTTP określająca, że klient chce pobrać zasób.
- **/index.html** – ścieżka do zasobu.
- **HTTP/1.1** – wersja protokołu.
- **Host** – nazwa lub adres serwera, do którego kierowane jest żądanie.
- **User-Agent** – informacja o kliencie.
- **Accept** – typy danych akceptowane przez klienta.

Najważniejsze metody HTTP:
- `GET` – pobieranie zasobu.
- `POST` – przesyłanie danych do serwera.
- `PUT` – tworzenie lub zastępowanie zasobu.
- `DELETE` – usuwanie zasobu.
- `HEAD` – pobranie samych nagłówków odpowiedzi, bez treści.

### Odpowiedź HTTP (response)

Przykład:

```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 45

<html><body>Witaj!</body></html>
```

Elementy odpowiedzi:
- Wersja protokołu.
- Kod statusu i jego opis.
- Nagłówki odpowiedzi.
- Pusta linia oddzielająca nagłówki od treści.
- Treść odpowiedzi (body), np. HTML, tekst lub obraz.

### Najważniejsze kody odpowiedzi HTTP

| Kod | Nazwa | Znaczenie |
|---|---|---|
| 200 | OK | Żądanie zakończone sukcesem. |
| 401 | Unauthorized | Brak poprawnego uwierzytelnienia. Serwer może zażądać podania danych logowania. |
| 403 | Forbidden | Serwer rozumie żądanie, ale odmawia dostępu do zasobu. |
| 404 | Not Found | Żądany zasób nie istnieje lub serwer nie może go znaleźć. |
| 500 | Internal Server Error | Wewnętrzny błąd serwera, np. błąd wykonania skryptu CGI. |

Ważne rozróżnienie:
- **401** – użytkownik nie został poprawnie uwierzytelniony.
- **403** – dostęp jest zabroniony, nawet jeśli użytkownik został uwierzytelniony.
- **404** – zasób nie został znaleziony.
- **500** – problem wystąpił po stronie serwera.

### Nagłówki HTTP

Nagłówki przekazują dodatkowe informacje o żądaniu lub odpowiedzi.

Przykłady:
- `Host` – wskazuje serwer.
- `Content-Type` – określa typ przesyłanych danych.
- `Content-Length` – określa długość treści.
- `Authorization` – przekazuje dane uwierzytelniające.
- `WWW-Authenticate` – informuje klienta o wymaganym sposobie uwierzytelnienia.
- `User-Agent` – identyfikuje klienta.

Przydatne polecenie:

```bash
curl -i http://127.0.0.1:8080/
```

Opcja `-i` powoduje wyświetlenie nagłówków odpowiedzi HTTP razem z treścią.

---

## 2. Apache HTTP Server 2.4

### Czym jest Apache?

Apache HTTP Server to serwer WWW obsługujący żądania HTTP i udostępniający zasoby, np. strony HTML, pliki oraz aplikacje działające po stronie serwera.

W laboratorium Apache uruchamiany jest w kontenerze Docker.

### DocumentRoot

`DocumentRoot` określa główny katalog, z którego Apache udostępnia pliki przez HTTP.

Przykład:

```apache
DocumentRoot /var/www/html
```

Oznacza to, że adres:

`http://localhost/index.html`

odpowiada plikowi:

`/var/www/html/index.html`

Natomiast adres:

`http://localhost/test/plik.txt`

odpowiada plikowi:

`/var/www/html/test/plik.txt`

DocumentRoot nie jest tym samym co katalog główny systemu plików. Określa jedynie katalog bazowy udostępnianych zasobów.

### Sekcje Directory

Sekcja `<Directory>` pozwala określić zasady działania Apache dla konkretnego katalogu systemu plików.

Przykład:

```apache
<Directory /var/www/html>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

Najważniejsze dyrektywy:

**Options** – określa dodatkowe funkcje dostępne w katalogu.

- `Indexes` – pozwala na wyświetlanie listy plików katalogu, jeśli nie ma pliku indeksowego.
- `FollowSymLinks` – pozwala Apache podążać za dowiązaniami symbolicznymi.
- `ExecCGI` – pozwala na wykonywanie skryptów CGI (przy odpowiedniej konfiguracji obsługi CGI).
- `Includes` – umożliwia obsługę Server Side Includes.

**AllowOverride** – określa, czy ustawienia mogą być nadpisywane przez pliki `.htaccess`.

- `None` – pliki `.htaccess` nie mogą nadpisywać konfiguracji.
- `All` – zezwala na nadpisywanie wszystkich kategorii dyrektyw, które obsługują tę funkcję.

**Require** – określa, kto może uzyskać dostęp do zasobu.

- `Require all granted` – dostęp dla wszystkich.
- `Require all denied` – dostęp zabroniony dla wszystkich.
- `Require valid-user` – dostęp dla poprawnie uwierzytelnionych użytkowników.

Przykład całkowitego zablokowania dostępu do katalogu:

```apache
<Directory /var/www/secret>
    Require all denied
</Directory>
```

### Pliki konfiguracyjne Apache

Główny plik konfiguracyjny nazywa się najczęściej `httpd.conf` lub `apache2.conf`.

W systemach Debian/Ubuntu konfiguracja jest zwykle podzielona na kilka plików i katalogów:

- `/etc/apache2/apache2.conf` – główny plik konfiguracyjny.
- `/etc/apache2/sites-enabled/` – aktywne konfiguracje witryn.
- `/etc/apache2/mods-enabled/` – aktywne moduły Apache.
- `/etc/apache2/ports.conf` – konfiguracja portów nasłuchiwania.

Przykład ustawienia portu:

```apache
Listen 8080
```

Przykład konfiguracji witryny:

```apache
<VirtualHost *:8080>
    DocumentRoot /var/www/html
</VirtualHost>
```

### Logi Apache

Logi pozwalają analizować działanie serwera i diagnozować problemy.

Najważniejsze rodzaje:

**access_log** – zapisuje informacje o żądaniach klientów, m.in.:
- adres IP klienta,
- datę i godzinę,
- metodę HTTP i żądany URL,
- kod odpowiedzi HTTP,
- rozmiar odpowiedzi.

**error_log** – zapisuje błędy i ostrzeżenia serwera, np.:
- błędy konfiguracji,
- brak uprawnień do plików,
- problemy z uruchomieniem CGI,
- błędy wewnętrzne serwera.

Przykładowe lokalizacje:

```text
/var/log/apache2/access.log
/var/log/apache2/error.log
```

Wyświetlenie logów na bieżąco:

```bash
tail -f /var/log/apache2/access.log
tail -f /var/log/apache2/error.log
```

W Dockerze można również wykorzystać:

```bash
docker compose logs -f
```

Logi są szczególnie przydatne, gdy serwer zwraca kod 403 lub 500.

---

## 3. Listowanie katalogu a dostęp do pliku o znanej nazwie

To bardzo ważne rozróżnienie związane z bezpieczeństwem serwera WWW.

### Options Indexes

Dyrektywa `Indexes` pozwala Apache wyświetlać zawartość katalogu, jeżeli nie znajduje się w nim plik indeksowy, np. `index.html`.

Przykład:

```apache
<Directory /var/www/html/files>
    Options Indexes (to samo co +Indexes, "+" jest opcjonalny)
    Require all granted
</Directory>
```

Po wejściu na:

`http://localhost/files/`

serwer może wyświetlić listę plików znajdujących się w katalogu.

### Wyłączenie listowania

```apache
<Directory /var/www/html/files>
    Options -Indexes
    Require all granted
</Directory>
```

Znak `-` oznacza wyłączenie danej opcji.

Po tej zmianie Apache nie wyświetli listy plików katalogu, jeśli nie ma pliku indeksowego.

### Czy plik nadal jest dostępny?

Tak!

Wyłączenie `Indexes` nie blokuje bezpośredniego dostępu do plików.

Przykład:

- Wejście na `http://localhost/files/` – lista plików nie zostanie wyświetlona.
- Wejście na `http://localhost/files/tajne.txt` – plik nadal może zostać pobrany.

Dzieje się tak, ponieważ `Indexes` kontroluje wyłącznie automatyczne listowanie zawartości katalogu, a nie dostęp do poszczególnych plików.

### Jak rzeczywiście zablokować dostęp?

Należy zastosować odpowiednią regułę dostępu:

```apache
<Directory /var/www/html/files>
    Options -Indexes
    Require all denied
</Directory>
```

Teraz:
- nie można wyświetlić listy plików,
- nie można pobrać plików z tego katalogu przez HTTP.

**Do zapamiętania:** wyłączenie listowania katalogu nie oznacza ukrycia znajdujących się w nim plików przed osobą znającą ich adres URL.

---

## 4. Uwierzytelnianie i autoryzacja

Są to dwa różne mechanizmy bezpieczeństwa.

### Uwierzytelnianie (authentication)

Uwierzytelnianie polega na sprawdzeniu, kim jest użytkownik.

Przykład: użytkownik podaje login i hasło, a serwer sprawdza, czy są poprawne.

### Autoryzacja (authorization)

Autoryzacja polega na określeniu, do jakich zasobów użytkownik ma prawo dostępu.

Przykład: użytkownik został poprawnie zalogowany, ale może mieć dostęp tylko do określonego katalogu.

W skrócie:
- Uwierzytelnianie – kim jesteś?
- Autoryzacja – do czego masz dostęp?

### HTTP Basic Authentication

HTTP Basic to prosty mechanizm uwierzytelniania HTTP.

Klient przesyła login i hasło w nagłówku:

```http
Authorization: Basic dXNlcjpwYXNz
```

Wartość po słowie `Basic` to dane `login:hasło` zakodowane algorytmem Base64.

**Ważne:** Base64 nie jest szyfrowaniem! Dane można łatwo zdekodować.

Dlatego HTTP Basic powinien być używany razem z HTTPS, które szyfruje transmisję pomiędzy klientem a serwerem.

### Konfiguracja Basic Authentication w Apache

Przykład:

```apache
<Directory /var/www/html/private>
    AuthType Basic
    AuthName "Strefa prywatna"
    AuthUserFile /etc/apache2/.htpasswd
    Require valid-user
</Directory>
```

Znaczenie dyrektyw:

- `AuthType Basic` – wybiera metodę uwierzytelniania HTTP Basic.
- `AuthName` – ustawia nazwę obszaru chronionego, wyświetlaną np. w oknie logowania.
- `AuthUserFile` – wskazuje plik zawierający bazę użytkowników i ich zahashowane hasła.
- `Require valid-user` – pozwala wejść każdemu użytkownikowi, który poprawnie się uwierzytelnił.

Jeżeli użytkownik nie poda danych logowania lub poda niepoprawne dane, serwer zwykle zwróci odpowiedź `401 Unauthorized`.

Jeżeli użytkownik zostanie poprawnie uwierzytelniony, ale nie spełni wymagań dostępu, może otrzymać `403 Forbidden`.

---

## 5. Program htpasswd – baza użytkowników i haseł

`htpasswd` to narzędzie Apache służące do tworzenia i modyfikowania plików zawierających użytkowników oraz ich zahashowane hasła.

Przykładowe utworzenie bazy użytkowników:

```bash
htpasswd -B -c /etc/apache2/.htpasswd student
```

Program poprosi o wpisanie i potwierdzenie hasła użytkownika `student`.

### Znaczenie opcji

**-c (create)**

Tworzy nowy plik bazy użytkowników.

Bardzo ważne: opcja `-c` nadpisuje istniejący plik!

Dlatego używa się jej tylko podczas pierwszego tworzenia bazy.

Dodanie kolejnego użytkownika:

```bash
htpasswd -B /etc/apache2/.htpasswd student2
```

Nie podajemy już `-c`, aby nie usunąć istniejących wpisów.

**-B**

Wybiera algorytm bcrypt do haszowania haseł.

Bcrypt jest algorytmem przeznaczonym do bezpiecznego przechowywania haseł. Jest znacznie lepszym wyborem niż przechowywanie haseł w postaci jawnej.

Wyświetlenie zawartości bazy:

```bash
cat /etc/apache2/.htpasswd
```

Zobaczymy wpisy zawierające loginy i zahashowane hasła, a nie hasła w postaci jawnej.

### Dlaczego baza haseł powinna znajdować się poza DocumentRoot?

Przykład prawidłowej lokalizacji:

```text
/etc/apache2/.htpasswd
```

Nie należy umieszczać bazy np. w:

```text
/var/www/html/.htpasswd
```

DocumentRoot jest katalogiem udostępnianym przez HTTP. Umieszczenie w nim bazy haseł może doprowadzić do jej pobrania przez klienta, jeżeli konfiguracja serwera nie zablokuje takiego dostępu.

Plik `.htpasswd` powinien być poza DocumentRoot, mieć odpowiednie uprawnienia systemowe i być dostępny do odczytu dla procesu Apache.

Dodatkowo można zablokować dostęp do plików konfiguracyjnych i ukrytych:

```apache
<FilesMatch "^\.ht">
    Require all denied
</FilesMatch>
```

### Bezpieczeństwo haseł

Do testów laboratoryjnych należy używać specjalnego, testowego hasła.

Nie należy używać haseł wykorzystywanych w prawdziwych usługach, ponieważ:
- baza może zostać przypadkowo ujawniona,
- plik może trafić do repozytorium,
- konfiguracja laboratoryjna może zawierać błędy.

Pliku `.htpasswd` nie należy umieszczać w repozytorium GitHub. Warto dodać go do `.gitignore`.

---

## 6. Uprawnienia systemu plików Linux

Apache i skrypty CGI działają jako procesy systemowe. Ich możliwości zależą m.in. od uprawnień przypisanych do plików i katalogów.

W systemie Linux uprawnienia są określane dla trzech kategorii:

1. **u (user)** – właściciel pliku.
2. **g (group)** – grupa przypisana do pliku.
3. **o (others)** – pozostali użytkownicy.

### Rodzaje uprawnień

| Symbol | Nazwa | Znaczenie dla pliku |
|---|---|---|
| r | read | Odczyt zawartości pliku. |
| w | write | Modyfikowanie zawartości pliku. |
| x | execute | Wykonywanie pliku. |

W przypadku katalogów:
- `r` – możliwość odczytania listy nazw plików.
- `w` – możliwość tworzenia, usuwania i zmieniania nazw wpisów w katalogu (z uwzględnieniem pozostałych uprawnień).
- `x` – możliwość przechodzenia przez katalog i uzyskiwania dostępu do jego elementów, jeśli pozwalają na to pozostałe uprawnienia.

### Sprawdzanie uprawnień

```bash
ls -l
```

Przykładowy wynik:

```text
-rw-r--r-- 1 student www-data 1200 index.html
```

Interpretacja:

- `-` – zwykły plik.
- `rw-` – właściciel może czytać i modyfikować.
- `r--` – grupa może tylko czytać.
- `r--` – pozostali mogą tylko czytać.
- `student` – właściciel.
- `www-data` – grupa.

### Zmiana uprawnień

Polecenie `chmod` służy do zmiany uprawnień.

Przykłady:

```bash
chmod 644 index.html
chmod 755 skrypt.py
chmod 640 .htpasswd
```

Znaczenie:
- `644` – właściciel ma odczyt i zapis, pozostali odczyt.
- `755` – właściciel ma pełne uprawnienia, pozostali odczyt i wykonanie.
- `640` – właściciel ma odczyt i zapis, grupa odczyt, pozostali brak dostępu.

Zmiana właściciela:

```bash
chown www-data:www-data plik
```

Zmiana grupy:

```bash
chgrp www-data plik
```

### Dlaczego uprawnienia są ważne?

Nawet jeżeli Apache pozwala na dostęp do zasobu przez HTTP, proces serwera musi mieć odpowiednie uprawnienia systemu plików, aby odczytać dany plik.

Warto pamiętać, że katalogi nadrzędne również muszą pozwalać procesowi na przechodzenie przez nie (`x`).

---

## 7. CGI – wykonywanie programów po stronie serwera

### Czym jest CGI?

CGI (Common Gateway Interface) to mechanizm umożliwiający uruchamianie programów po stronie serwera WWW.

W przeciwieństwie do zwykłych plików HTML, które Apache jedynie odczytuje i przesyła klientowi, program CGI jest wykonywany przez serwer.

Program może być napisany np. w:
- Pythonie,
- powłoce systemowej `sh`,
- innym języku obsługiwanym przez odpowiedni interpreter.

Przykładowe zastosowania:
- generowanie dynamicznych stron,
- przetwarzanie formularzy,
- wykonywanie operacji na danych,
- zwracanie informacji o systemie.

### Konfiguracja CGI w Apache

Przykładowa konfiguracja:

```apache
<Directory /var/www/html/cgi-bin>
    Options +ExecCGI
    Require all granted
</Directory>

AddHandler cgi-script .py
```

Wymagany jest również odpowiedni moduł CGI, np. `mod_cgi` lub `mod_cgid`, zależnie od środowiska.

### Budowa skryptu CGI

Skrypt CGI musi zwracać odpowiedź zgodną z wymaganiami CGI.

Przykład w Pythonie:

```python
#!/usr/bin/env python3

print("Content-Type: text/plain; charset=utf-8")
print()
print("Witaj! To jest odpowiedz CGI.")
```

Najważniejsze elementy:

**1. Pierwszy wiersz – interpreter**

```python
#!/usr/bin/env python3
```

To tzw. shebang. Informuje system, jakiego interpretera użyć do uruchomienia skryptu.

**2. Nagłówek Content-Type**

```python
print("Content-Type: text/plain; charset=utf-8")
```

Informuje klienta, jaki typ danych zostanie zwrócony.

Przykłady:
- `text/plain` – zwykły tekst.
- `text/html` – dokument HTML.
- `application/json` – dane JSON.

**3. Pusta linia**

```python
print()
```

Oddziela nagłówki CGI od treści odpowiedzi. Jest obowiązkowa.

**4. Treść odpowiedzi**

```python
print("Witaj!")
```

To zawartość, którą otrzyma klient.

### Uprawnienia skryptu CGI

Skrypt musi mieć prawo wykonywania.

Przykład:

```bash
chmod 755 /var/www/html/cgi-bin/test.py
```

Jeżeli interpreter nie może uruchomić skryptu lub skrypt ma nieprawidłowy format, Apache może zwrócić błąd 500.

Skrypty CGI należy zapisywać z końcami wierszy LF, szczególnie w środowisku Linux. Końce wierszy CRLF z Windows mogą powodować problemy z interpretacją shebanga.

---

## 8. Tożsamość procesu – UID i GID

### Czym są UID i GID?

W systemie Linux każdy proces działa z określoną tożsamością użytkownika i grupy.

- **UID (User ID)** – identyfikator użytkownika.
- **GID (Group ID)** – identyfikator grupy.

Ważne są również:
- rzeczywisty UID/GID – identyfikują użytkownika i grupę, z którymi proces jest związany;
- efektywny UID/GID – określają tożsamość wykorzystywaną przede wszystkim przy sprawdzaniu uprawnień procesu.

W praktyce przy analizie uprawnień procesu szczególnie istotny jest efektywny UID i GID.

### Z jakimi uprawnieniami działa Apache?

W typowej konfiguracji Debian/Ubuntu:

```apache
User www-data
Group www-data
```

Procesy robocze Apache działają jako użytkownik `www-data` i grupa `www-data`.

Proces główny Apache może być uruchomiony z wyższymi uprawnieniami (często jako root), np. aby otworzyć porty i zarządzać procesami. Obsługę żądań realizują jednak procesy robocze z ograniczonymi uprawnieniami.

### Czy zalogowanie użytkownika Basic zmienia UID procesu?

**Nie!**

To bardzo ważne zagadnienie.

Uwierzytelnienie HTTP Basic:
- sprawdza login i hasło użytkownika,
- pozwala lub nie pozwala na dostęp do zasobu,
- nie zmienia użytkownika systemowego, z którym działa proces Apache lub CGI.

Przykład:

Użytkownik HTTP `student` poprawnie loguje się do chronionego katalogu. Skrypt CGI uruchomiony przez Apache nadal działa z uprawnieniami procesu obsługującego CGI, np. `www-data`.

Użytkownik HTTP nie staje się automatycznie użytkownikiem systemowym Linux.

### Sprawdzenie UID i GID w Pythonie

Można wykorzystać moduł `os`:

```python
#!/usr/bin/env python3

import os

print("Content-Type: text/plain; charset=utf-8")
print()

print("UID:", os.getuid())
print("EUID:", os.geteuid())
print("GID:", os.getgid())
print("EGID:", os.getegid())
```

Najważniejsze funkcje:
- `os.getuid()` – zwraca rzeczywisty UID.
- `os.geteuid()` – zwraca efektywny UID.
- `os.getgid()` – zwraca rzeczywisty GID.
- `os.getegid()` – zwraca efektywny GID.

W ten sposób można sprawdzić, z jakimi uprawnieniami rzeczywiście działa program CGI.

---

## 9. Zakaz dostępu przez HTTP a brak prawa odczytu przez CGI

To dwa różne mechanizmy, których nie należy ze sobą mylić.

### Blokada dostępu HTTP

Przykład:

```apache
<Directory /var/www/html/private>
    Require all denied
</Directory>
```

Oznacza, że Apache nie pozwala klientom pobierać zasobów z tego katalogu przez HTTP.

Jednak nie oznacza to automatycznie, że proces Apache lub CGI nie może odczytać znajdujących się tam plików.

Dyrektywa `Require` kontroluje dostęp na poziomie serwera WWW.

### Brak prawa odczytu przez CGI

Jeżeli plik ma uprawnienia:

```bash
chmod 600 /var/www/html/private/secret.txt
```

i jego właścicielem jest `root`, a skrypt CGI działa jako `www-data`, to skrypt nie będzie mógł odczytać pliku, ponieważ nie ma odpowiednich uprawnień systemowych.

Jest to ograniczenie na poziomie systemu operacyjnego.

### Najważniejsza różnica

| Mechanizm | Co kontroluje? |
|---|---|
| `Require all denied` | Dostęp klientów przez HTTP. |
| Uprawnienia `chmod` | Możliwości odczytu, zapisu i wykonania przez procesy systemowe. |

Możliwe są więc dwie sytuacje:

1. Apache blokuje dostęp przez HTTP, ale skrypt CGI nadal może odczytać plik, ponieważ ma odpowiednie uprawnienia systemowe.
2. Apache zezwala na dostęp przez HTTP, ale proces nie może odczytać pliku z powodu braku uprawnień systemowych.

**Wniosek:** bezpieczeństwo serwera WWW wymaga zarówno odpowiedniej konfiguracji Apache, jak i prawidłowego ustawienia uprawnień systemu plików.

---

## 10. Przydatne polecenia do laboratorium

| Polecenie | Zastosowanie |
|---|---|
| `docker compose up -d --build` | Budowanie obrazu i uruchomienie kontenerów. |
| `docker compose down` | Zatrzymanie i usunięcie kontenerów. |
| `docker compose logs -f` | Wyświetlanie logów kontenerów. |
| `curl -i http://127.0.0.1:8080/` | Żądanie HTTP z wyświetleniem nagłówków odpowiedzi. |
| `curl -u student http://127.0.0.1:8080/private/` | Logowanie HTTP Basic; program poprosi o hasło. |
| `htpasswd -B -c .htpasswd student` | Utworzenie bazy użytkowników z bcrypt. |
| `htpasswd -B .htpasswd student2` | Dodanie kolejnego użytkownika. |
| `ls -l` | Sprawdzenie uprawnień plików. |
| `chmod 755 skrypt.py` | Nadanie uprawnień wykonywania. |
| `chown www-data:www-data plik` | Zmiana właściciela i grupy. |
| `tail -f error.log` | Śledzenie logów błędów. |
| `tail -f access.log` | Śledzenie żądań HTTP. |

Uwaga: ścieżki do logów, konfiguracji i plików zależą od obrazu Docker i konfiguracji kontenera.

---

## 11. Najważniejsze zagadnienia – podsumowanie do zapamiętania

1. **HTTP request** to żądanie klienta, a **HTTP response** to odpowiedź serwera.
2. Kod `200` oznacza sukces, `401` brak poprawnego uwierzytelnienia, `403` odmowę dostępu, `404` brak zasobu, a `500` błąd serwera.
3. `DocumentRoot` określa katalog, z którego Apache udostępnia pliki.
4. Sekcja `<Directory>` pozwala ustalać zasady działania serwera dla określonych katalogów.
5. `Options Indexes` umożliwia listowanie plików katalogu, natomiast `Options -Indexes` wyłącza tę funkcję.
6. Wyłączenie `Indexes` NIE blokuje dostępu do pliku, którego nazwę i URL użytkownik zna.
7. `Require all denied` blokuje dostęp przez HTTP, a `Require all granted` zezwala wszystkim.
8. Uwierzytelnianie odpowiada na pytanie „kim jesteś?”, a autoryzacja „do czego masz dostęp?”.
9. HTTP Basic przesyła login i hasło zakodowane Base64. Base64 nie jest szyfrowaniem, dlatego potrzebny jest HTTPS.
10. `AuthType Basic` włącza Basic Authentication, `AuthUserFile` wskazuje bazę użytkowników, a `Require valid-user` wymaga poprawnego logowania.
11. `htpasswd -B -c` tworzy bazę z hasłami haszowanymi bcrypt. Opcję `-c` stosuje się tylko przy pierwszym tworzeniu pliku, ponieważ nadpisuje istniejącą bazę.
12. Baza `.htpasswd` powinna znajdować się poza DocumentRoot i nie może być umieszczana w repozytorium.
13. `r` oznacza odczyt, `w` zapis, a `x` wykonanie pliku lub możliwość przechodzenia przez katalog.
14. CGI umożliwia wykonywanie programów po stronie serwera.
15. Skrypt CGI musi zawierać interpreter w pierwszym wierszu, nagłówek `Content-Type`, pustą linię i treść odpowiedzi.
16. Proces CGI działa z uprawnieniami systemowymi procesu, który go uruchamia, a nie z uprawnieniami zalogowanego użytkownika HTTP.
17. Efektywny UID/GID mają zasadnicze znaczenie przy sprawdzaniu uprawnień procesu.
18. Blokada `Require` i uprawnienia systemu plików to dwa niezależne poziomy kontroli dostępu.

---

## 12. Odpowiedzi na pytania z samokontroli

**1. Czy wyłączenie listowania ukrywa plik przed osobą znającą jego URL?**

Nie. `Options -Indexes` wyłącza jedynie automatyczne wyświetlanie listy plików katalogu. Jeżeli dostęp do pliku jest dozwolony, można go nadal pobrać, znając jego dokładny URL. Aby rzeczywiście zablokować dostęp, należy zastosować np. `Require all denied`.

**2. Dlaczego baza htpasswd nie powinna być dostępna przez HTTP?**

Ponieważ zawiera loginy i zahashowane hasła użytkowników. Osoba, która uzyska dostęp do tego pliku, może próbować odzyskać hasła lub przeprowadzić ataki słownikowe i brute force na ich skróty. Dlatego baza powinna znajdować się poza DocumentRoot, mieć odpowiednie uprawnienia i nie być udostępniana klientom.

**3. Czy poprawne logowanie Basic zmienia UID procesu obsługującego żądanie?**

Nie. Basic Authentication jedynie weryfikuje tożsamość użytkownika na poziomie HTTP. Nie zmienia tożsamości systemowej procesu Apache ani CGI. Proces nadal działa np. jako `www-data`, a jego uprawnienia wynikają z UID/GID oraz uprawnień systemu plików.

---

## 13. Źródła

Podstawą opracowania są materiały do Laboratorium 5 – „Bezpieczeństwo serwera usług WWW” oraz oficjalna dokumentacja Apache HTTP Server 2.4:

- Kontrola dostępu: https://httpd.apache.org/docs/2.4/howto/access.html
- Uwierzytelnianie i autoryzacja: https://httpd.apache.org/docs/2.4/howto/auth.html
- CGI: https://httpd.apache.org/docs/2.4/howto/cgi.html
- Program htpasswd: https://httpd.apache.org/docs/2.4/programs/htpasswd.html
- Dyrektywy Apache: https://httpd.apache.org/docs/2.4/mod/core.html

**Uwaga dotycząca kryptografii:** W przedstawionym zakresie nie ma potrzeby samodzielnego implementowania algorytmów kryptograficznych w Pythonie. Hasła obsługuje narzędzie `htpasswd` z bcrypt (`-B`), dlatego nie ma potrzeby używania ani `hashlib`, ani PyCryptodome.