Zadanie 1 - szyfr cezara:    
k= 230  ocena = 1.0  początek tekstu = b'Wkh#Qljkw#Ihuu|\r\rWkh#qljkw#ihuu|#ohiw#wkh#kduerxu#'  
k= 233  ocena = 1.0  początek tekstu = b'The Night Ferry\n\nThe night ferry left the harbour '  
k= 228  ocena = 0.9947534102833159  początek tekstu = b'Ymj%Snlmy%Kjww~\x0f\x0fYmj%snlmy%kjww~%qjky%ymj%mfwgtzw%'  
k= 229  ocena = 0.9947534102833159  początek tekstu = b'Xli$Rmklx$Jivv}\x0e\x0eXli$rmklx$jivv}$pijx$xli$levfsyv$'  
k= 231  ocena = 0.9947534102833159  początek tekstu = b'Vjg"Pkijv"Hgtt{\x0c\x0cVjg"pkijv"hgtt{"nghv"vjg"jctdqwt"'  
  
Przesunięcie wynosiło k = 233. Trzeba było popatrzeć czy otrzymaliśmy prawdziwe słowa, żeby wybrać poprawne spośród najwyżej ocenianych wyników. Sama entropia nie jest w stanie rozstrzygnąć, które przesunięcie jest poprawne, ponieważ częstotliwość występowania poszczególnych bajtów się nie zmienia, jedynie ich "wartość" jest inna - tzn np. "abbb" ma taką samą entropię jak "cddd" i "efff".  
<br>  
Zadanie 2 - szyfr Vigenere'a:  
Zgodność pliku po zaszyfrowaniu i odszyfrowaniu: True  
Test dla pustych danych: True  
Test dla bajtów 0 i 255: True  
  
Klucz: SZYFR  
Hex: 95ac9a939395ac9a939395ac9a9393  
95ac9a9393  
95ac9a9393  
95ac9a9393  
  
Klucz: KOD  
Hex: 8da1859890869d90918c91968c9c85  
8da1859890  
869d90918c  
91968c9c85  

W pierwszym przypadku powtarzają się całe pięciobajtowe fragmenty kryptogramu, ponieważ klucz SZYFR ma taką samą długość jak zapętlone słowo BRAMA w szyfrowanym tekście, przez co za każdym razem te same litery słowa SZYFR są używane do szyfrowania tych samych liter słowa BRAMA. Klucz KOD ma 3 litery, więc nie pasuje równo do 5-literowej BRAMA  
<br>  
Zadanie 3 - szyfr RC4:  
Zgodność po zaszyfrowaniu i odszyfrowaniu: True  

Ponowne szyfrowanie może odtworzyć kryptogram również dla błędnego klucza, ponieważ RC4 wykorzystuje operację XOR, a ona jest odwracalna.
