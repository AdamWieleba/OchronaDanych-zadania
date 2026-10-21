# Zadanie 1  
423ae4427c4cc4c154c340c75699418f423ae4427c4cc4c154c340c75699418f423ae4427c4cc4c154c340c75699418f423ae4427c4cc4c154c340c75699418f  
2bbd342f80af1fd20f37e923081dbb4f740f32bb8d9673e14fbba4c1f43de9a872dc2fe07f56ff4c19708f65f710ef6665a526b713c0c326a86f7e806f85462e  
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
Kryptogram: 934c92e37aeba4ff01fd1eefd32a908fd12654b118d6b31baac394a1b40a96038a1ba897cd52dbf331a1bab339ab709fa7da879884f86a79def38ca489641ffac7514d86357bdb1dae3dd6019d5f886e324186809378d29b0a699390b32afe056f9332604461efa5172beac7ae068fa74aba2f09840acb83d8cf57d6a15c4efd98e5bc8932a8d5507096479910b568c1cfd94f98eb2f8e6aeebef5aa758324e53d55dc961494b0ebef1f5b3746fd5d7f9db7c90078f34826e360000672c6e17aaad78fca57bcb6ca14d522090b69204251adaa33b6ba22694ad0f6fa84731d5e4c05073a00ceb24253270ec963b446bdb475da44ec6f0cda2ddd3de5695fe176  
Czy jest takie samo po odszyfrowaniu: True  

Dane = wiadomosc.txt z nową solą i iv:  
Dlugosc poczatkowa: 247  
Dlugosc kryptogramu: 256  
Kryptogram: af3c52c2e0ad982a169a3308bc477d4a342282e44b012370b37d85bbc45b2f3aefaf5799024c03660e01a51a21f201c1af68148dc7f9f784abdce9c17400524095ddbe54aabd76cfd4660f76f6de929441270c01d23535f930e557b60f4da505f76c1715c6752fe76756c12da18de30ff42b1e3eddc9d19b8c7fb30758c5bb9440380a80030afef80a15d9401d579debe6db91957f0e56dea56f478c87b5a1eabb58253f445fa75bfd7381b37f91cea5822a4e186ec14d657ff5cdbbc937a696f706546ede96eacda278ca12e0054691c89362a0b747bc3461283e8fbd22ec752bd6395f4bc3f4453f62d36e4a69531c8d2bded2744ce35ce2ec25ffd54c21e8  
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
Odszyfrowany tekst: Record 000. The archive contains laboratory notes about symmetric encryption and careful handling of binary files.[...]  

**Kluczy jest 36, bo tyle jest zwykłych liter + cyfr**  
**Ranking może zawieść przy danych skompresowanych, ponieważ równomierność rozkładu jest wykorzystywana przez proces kompresji**
