Pakiet jest już przygotowany do uruchomienia na Ubuntu. Nie musisz samodzielnie pisać Dockerfile ani konfigurować obrazu Apache. 
Trzeba zainstalować Docker Engine i Docker Compose, rozpakować archiwum, a następnie zbudować i uruchomić kontener.

# Etap 1. Instalacja Dockera w Ubuntu

Otwórz terminal Ubuntu (`Ctrl + Alt + T`).

1\. Zaktualizuj listę pakietów:

```
sudo apt update
sudo apt upgrade -y
```

2\. Zainstaluj narzędzia potrzebne do instalacji Dockera:

```
sudo apt install ca-certificates curl -y
```

3\. Dodaj oficjalny klucz repozytorium Docker:

```
sudo install -m 0755 -d /etc/apt/keyrings
```

```
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
```

```
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

4\. Dodaj oficjalne repozytorium Dockera:

```
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

5\. Zaktualizuj listę pakietów:

```
sudo apt update
```

6\. Zainstaluj Docker Engine, Compose i pozostałe wymagane komponenty:

```
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

7\. Uruchom usługę Docker:

```
sudo systemctl enable --now docker
```

8\. Sprawdź, czy Docker działa:

```
sudo docker version
```

Powinieneś zobaczyć informacje o wersji klienta i serwera Docker.

Sprawdź też Compose:

```
sudo docker compose version
```

Powinna pojawić się wersja Docker Compose.

9\. Umożliw uruchamianie Dockera bez `sudo`:

Wykonaj:

```
sudo usermod -aG docker $USER
```

Następnie:

```
newgrp docker
```

To odświeży członkostwo w grupie w nowej sesji terminala.

Sprawdź:

```
docker run hello-world
```

Oczekiwany wynik

Powinien pojawić się komunikat:

```
Hello from Docker!
```

Uwaga: członkostwo w grupie `docker` daje uprawnienia zbliżone do administratora systemu. Dodawaj do niej tylko zaufane konta.

Wszystkie dalsze polecenia wykonuj właśnie w katalogu z compose.yaml, ponieważ `compose.yaml` odwołuje się do plików względem bieżącego katalogu.

# Etap 3. Budowanie kontenera

15\. Sprawdź wersję Dockera:

```
docker version
```

16\. Sprawdź wersję Docker Compose:

```
docker compose version
```

17\. Zbuduj obraz serwera WWW:

```
docker compose build web
```

Co się teraz wydarzy?

- Docker pobierze obraz bazowy `httpd:2.4-alpine`.
- Zainstaluje w nim Python 3.
- Skopiuje konfigurację Apache.
- Skopiuje pliki strony WWW.
- Skopiuje katalog `cgi-bin`.
- Przygotuje katalog `/lab-data/` i ustawi odpowiednie prawa dostępu.

Przy pierwszym budowaniu wymagane jest połączenie z Internetem. Budowanie może potrwać kilka minut.

# Etap 4. Uruchomienie kontenera

18\. Uruchom serwer Apache w tle:

```
docker compose up -d web
```

Powinien pojawić się komunikat informujący o uruchomieniu kontenera.

19\. Sprawdź, czy kontener działa:

```
docker compose ps
```

Powinieneś zobaczyć usługę `web` ze statusem `Up`.

20\. Sprawdź poprawność konfiguracji Apache:

```
docker compose exec web httpd -t
```

Oczekiwany wynik

```
Syntax OK
```

Jeżeli otrzymasz ten wynik, konfiguracja Apache jest poprawna składniowo.

# Etap 5. Testowanie serwera

21\. Wyślij zapytanie HTTP do serwera:

```
curl -i http://127.0.0.1:8080/
```

Powinieneś otrzymać odpowiedź zawierającą:

```
HTTP/1.1 200 OK
```

oraz treść strony:

```
<h1>Laboratorium 5: serwer WWW działa</h1>
```

To oznacza, że serwer Apache prawidłowo obsługuje żądania HTTP.

22\. Sprawdź logi serwera:

```
docker compose logs --tail 30 web
```

Zobaczysz między innymi informacje o obsłużonych zapytaniach HTTP.

23\. Sprawdź wersję Apache:

```
docker compose exec web httpd -v
```

24\. Sprawdź wersję Pythona w kontenerze:

```
docker compose exec web python3 --version
```

Python powinien być zainstalowany i dostępny jako `python3`.

# Etap 6. Sprawdzenie w przeglądarce

Otwórz Firefox lub Chrome i wpisz:

Adres lokalnego serwera

http://127.0.0.1:8080  
(nwm czy na końcu jest / czy nie)  
Otwórz stronę  

Powinna wyświetlić się strona:

## Laboratorium 5: serwer WWW działa

Materiały ćwiczeniowe do konfiguracji dostępu w Apache.

- Materiały
- Wewnętrzne
- Panel

# Etap 7. Zatrzymywanie kontenera

Kiedy skończysz pracę, możesz zatrzymać środowisko:

```
docker compose down
```

Ważne: to polecenie zatrzyma i usunie kontener, ale nie usunie Twoich plików projektu, konfiguracji ani lokalnej bazy ćwiczeniowej.

Następnym razem uruchomisz go ponownie poleceniem:

```
docker compose up -d web
```

Nie musisz ponownie budować obrazu, jeżeli nie zmieniałeś plików wymagających przebudowania.

# Kontrola końcowa

Pamiętaj, że `docker compose down` wykonaj dopiero po testach, ponieważ zatrzymuje serwer.

## Dwie ważne uwagi dotyczące Twojego pakietu

1. Plik `konfiguracja/dostep.conf` jest celowo pusty poza komentarzem. Reguły dostępu będziesz dopisywać podczas laboratorium.
2. Katalog `cgi-bin` nie zawiera jeszcze programu `uprawnienia.cgi`. Masz go napisać samodzielnie podczas zajęć. To nie jest błąd instalacji.

Dokumentacja instalacji: [Docker Engine – Ubuntu](https://docs.docker.com/engine/install/ubuntu/?utm_source=chatgpt.com).
