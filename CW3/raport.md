Adam Wieleba 337634, python, https://github.com/AdamWieleba/OchronaDanych-zadania/tree/main/CW3, dla wszystkich programów "python zadanieX.py"

# Zadanie 1  
423ae4427c4cc4c154c340c75699418f 423ae4427c4cc4c154c340c75699418f 423ae4427c4cc4c154c340c75699418f 423ae4427c4cc4c154c340c75699418f  (ECB)  
2bbd342f80af1fd20f37e923081dbb4f 740f32bb8d9673e14fbba4c1f43de9a87 2dc2fe07f56ff4c19708f65f710ef66 65a526b713c0c326a86f7e806f85462e  (CBC)  
Czy tekst po szyfrowaniu i odszyfrowaniu jest taki sam (ECB): True  
Czy tekst po szyfrowaniu i odszyfrowaniu jest taki sam (CBC): True  
  
**W trybie ECB wszystkie 4 bloki są równe (423ae4427c4cc4c154c340c75699418f), natomiast w CBC wszystkie są inne**  
**Wyjaśnienie: w trybie ECB wszystkie bloki są szyfrowane niezależnie (taki sam blok -> taki sam szyfrogram), podczas gdy w CBC szyfrowanie bloku jest zależne od iv / poprzednich bloków**

# Zadanie 2  
Dane = puste dane:  
Dlugosc poczatkowa: 0  
Dlugosc kryptogramu: 16  
Kryptogram: 0d3904c13c79fe8a82fe43e3f881510b  
Czy jest takie samo po odszyfrowaniu: True  
  
Dane = 0123456789ABCDEF:  
Dlugosc poczatkowa: 16  
Dlugosc kryptogramu: 32  
Kryptogram: db9971b4c57dd56a58524bd89e5883e49a512bce0cb1717dbc5bf790f01da718  
Czy jest takie samo po odszyfrowaniu: True  

Dane = wiadomosc.txt:  
Dlugosc poczatkowa: 247  
Dlugosc kryptogramu: 256  
Kryptogram: 934c92e37aeba4ff01fd1eefd32a908fd12654b118d6b31baac394a1b40a96038a1ba897cd52dbf331a1bab339ab709fa7da879884f86a79def38ca489641ffac7514d8 ...
Czy jest takie samo po odszyfrowaniu: True  

Dane = wiadomosc.txt z nową solą i iv:  
Dlugosc poczatkowa: 247  
Dlugosc kryptogramu: 256  
Kryptogram: af3c52c2e0ad982a169a3308bc477d4a342282e44b012370b37d85bbc45b2f3aefaf5799024c03660e01a51a21f201c1af68148dc7f9f784abdce9c17400524095d ...
Czy jest takie samo po odszyfrowaniu: True  

**Widać że mimo tego samego hasła, dla różnych soli i iv kryptogram jest zupełnie inny**  
**Sól służy do zamiany zwykłego ludzkiego hasła w odpowiedni klucz, natomiast iv jest wykorzystywany do szyfrowania w CBC**


# Zadanie 3  
Entropia: 4.4536, znak: m  
Entropia: 7.9472, znak: b  
Entropia: 7.949, znak: x  
Entropia: 7.9493, znak: o  
Entropia: 7.9502, znak: 2  

Najlepszy kandydat - entropia: 4.4536, znak: m
Odszyfrowany tekst: Record 000. The archive contains laboratory notes about symmetric encryption and careful handling of binary files. ...  

**Kluczy jest 36, bo tyle jest zwykłych liter + cyfr**  
**Ranking może zawieść przy danych skompresowanych, ponieważ równomierność rozkładu jest wykorzystywana przez proces kompresji**
