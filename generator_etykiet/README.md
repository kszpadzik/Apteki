Instrukcja: Jak używać programu do generowania naklejek
1. Zainstaluj Python:
- Wejdź na https://www.python.org/downloads/windows/
- Kliknij „Download Python 3.x.x” i uruchom instalator (Polecana wersja 3.11, np. 3.11.5)
- Zaznacz opcję „Add Python to PATH” i kliknij „Install Now”

2. Utwórz folder o nazwie np. „NaklejkiApteka” i skopiuj do niego pliki:
- generator_naklejek.py
- etykiety_dane.json

3. Edytuj dane apteki:
- Otwórz plik etykiety_dane.json i zmien nazwę, adres i telefon apteki (znajduje się on na końcu pliku).

4. Zainstaluj biblioteki do tworzenia PDF:
- Otwórz Wiersz polecenia (Win + R → wpisz 'cmd')
- Wpisz: pip install reportlab

5. Uruchomienie programu:
- Wejdź do folderu, np.: cd Desktop\NaklejkiApteka
python generator_naklejek.py -h
python generator_naklejek.py --reset
python generator_naklejek.py --lek "0,5% sol";"Atropini sulfurici";"10 minimsów" --pos_start 1 --pos_koniec 4 --dr "Adam Dąbrowski" --wyk "Anna Nowak" --d "07.11.2025" --exp "30 dni" --p "lodówka"
python generator_naklejek.py --lek "0,1% sol";"Atropini sulfurici";"10 minimsów" --pos_start 5 --pos_koniec 12 --dr "Dorota Kowalska" --wyk "Anna Nowak" --d "08.11.2025" --exp "30 dni" --p "lodówka"
python generator_naklejek.py --lek "H20";"Woda";"płyn" --pos_start 11 --pos_koniec 15 --dr "Grześ Nowakowski" --wyk "Anna Nowak" --d "07.11.2025" --exp "30 dni" --p "lodówka""

6. Plik etykiety.pdf zostanie utworzony – otwórz i wydrukuj

7. Aby usunąć dane ze wszystkich naklejek:
- Uruchom: python stickers.py --reset (resetuje on również dane poza danymi apteki w pliku "etykiety_dane.json)

Gotowe! Dane do poszczególnych naklejek możesz również wpisać ręcznie w pliku etykiety_dane.json

Do poprawy:

Aktualnie domyślnie przy uruchomieniu "python generator_naklejek.py", bez żadnych flag, kasują się dane z 'etykiety_dane.json', dotyczące danych zmienianych za pomocą flag (np. '--lek', '--d', '--p'). Ostatecznie przy wykonaniu wspomnianej komendy w konsoli, stworzyć się ma plik na podstawie pliku 'etykiety_dane.json' bez jego zmiany.
