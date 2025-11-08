import argparse
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', r'C:\Windows\Fonts\arial.ttf'))

RZEDY = 5
KOLUMNY = 3
ETYKIETY_PER_PAGE = RZEDY*KOLUMNY
SZER_NAKLEJKI = 63 * mm
WYS_NAKLEJKI = 54 * mm
MARGINES_X = 10 * mm
MARGINES_Y = 15 * mm
SZEROKOSC_STRONY, WYSOKOSC_STRONY = A4

ETYKIETY_PLIK = 'etykiety_dane.json'
PDF_WYJSCIOWY = 'etykiety.pdf'

PUSTA_ETYKIETA = {
    'Lek': ['', '', ''],
    'Dr.': '',
    'Wyk': '',
    'Dnia': '',
    'Exp': '',
    'Przechowywać': '',
    'Sposób użycia': '',
    'D.S': ''
}

INF_APTEKI = {
    'nazwa': '',
    'adres_ul': '',
    'adres_kod': '',
    'telefon': ''
}

def zaladowanie_danych():
    '''
    Otwieranie danych z pliku json 'ETYKIETY_PLIK', zwracanie danych do 'etykiety' oraz danych 'apteki' dla
    poszczególnej naklejki.
    '''
    if os.path.exists(ETYKIETY_PLIK):
        with open(ETYKIETY_PLIK, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'etykiety': [PUSTA_ETYKIETA.copy() for _ in range(ETYKIETY_PER_PAGE)],
        'apteka': INF_APTEKI.copy()
    }

def zapis_danych(dane):
    '''
    Zmiana danych w pliku json 'ETYKIETY_PLIK' jeżeli zostały one zmienione za pomocą konsoli przez
    funkję 'aktualizuj_etykiete'.

    dane: dict[str, Any], zmienne opisujące informacje na temat leku oraz pola głównego naklejki.
    '''
    with open(ETYKIETY_PLIK, 'w', encoding='utf-8') as f:
        json.dump(dane, f, indent=2, ensure_ascii=False)

def pisanie_danych_naklejki(c, x, y, dane, apteka):
    '''
    Funkcja odpowiedzialna za pisanie rozmieszczenie oraz pisanie tekstu dla pola głównego, nazwy i informacji
    dotyczących danego leku oraz danych apteki  dla poszczególnej naklejki.

    c: Any,   canvas.Canvas(PDF_WYJSCIOWY, pagesize=A4)
    x: float, MARGINES_X + kolumna * SZER_NAKLEJKI
    y: float, WYSOKOSC_STRONY - MARGINES_Y - (rzad + 1) * WYS_NAKLEJKI
    dane: dict, dane do pola głównego oraz inf na temat leku załadowane z pliku json
    apteka dict, dane apteki załadowne z pliku json
    '''
    c.setFont('Arial', 8)
    c.rect(x, y, SZER_NAKLEJKI, WYS_NAKLEJKI)

    wypelnienie = 5
    wysokosc_linijki = 9
    przesuniecie_y = WYS_NAKLEJKI - wypelnienie - wysokosc_linijki

    # Pola główne (7 linijek)
    for pole in ['Dr.', 'Wyk', 'Dnia', 'Exp', 'Przechowywać', 'Sposób użycia', 'D.S']:
        zawartosc = dane.get(pole, '')
        c.drawString(x + 5, y + przesuniecie_y, f'{pole} {zawartosc}') 
        przesuniecie_y -= wysokosc_linijki

    # Ramka na dane apteki (4 linijki) + 1 linia
    c.line(x, y+ przesuniecie_y, x + SZER_NAKLEJKI, y+ przesuniecie_y)
    przesuniecie_y -= wysokosc_linijki
    c.drawString(x + 5, y + przesuniecie_y, apteka.get('nazwa', ''))
    c.drawString(x + 5, y + przesuniecie_y - wysokosc_linijki, apteka.get('adres_ul', ''))
    c.drawString(x + 5, y + przesuniecie_y - 2 * wysokosc_linijki, apteka.get('adres_kod', ''))
    c.drawString(x + 5, y + przesuniecie_y - 3 * wysokosc_linijki, apteka.get('telefon', ''))

    # Ramka na nazwę leku (3 linijki) + 1 linia
    przesuniecie_y = przesuniecie_y - 4 * wysokosc_linijki
    c.line(x, y+przesuniecie_y, x + SZER_NAKLEJKI, y+ przesuniecie_y)
    przesuniecie_y -= wysokosc_linijki
    for line in dane.get('Lek', ['', '', '']):
        c.drawString(x + 5, y + przesuniecie_y, line)
        przesuniecie_y -= wysokosc_linijki

def stworz_etykiety_pdf(etykiety, apteka):
    '''
    Tworzenie pliku pdf naklejka po naklejce.

    etykiety: dict[str, Any]
    apteka: dict[str, str]
    '''
    if os.path.exists(PDF_WYJSCIOWY):
        os.remove(PDF_WYJSCIOWY)
    c = canvas.Canvas(PDF_WYJSCIOWY, pagesize=A4)
    for i in range(ETYKIETY_PER_PAGE):
        rzad = i // KOLUMNY
        kolumna = i % KOLUMNY
        x = MARGINES_X + kolumna * SZER_NAKLEJKI
        y = WYSOKOSC_STRONY - MARGINES_Y - (rzad + 1) * WYS_NAKLEJKI
        pisanie_danych_naklejki(c, x, y, etykiety[i], apteka)
    c.save()
    print(f'✅ Wygenerowano plik PDF: {PDF_WYJSCIOWY}')

def aktualizuj_etykiete(etykiety, dane, start, koniec):
    '''
    Aktualizuje zmienną przechowującą dane poszczególnej naklejki.

    etykety: list[dict[str, Any]], [PUSTA_ETYKIETA.copy() for _ in range(ETYKIETY_PER_PAGE)]
    dane: dict[str, Any], zmienna przechowujące zmienne dane dla naklejki
    start: int, numer o 1 mniejszy niż pierwszy numer naklejki dla jakiej zmieniamy zmienne dane
    koniec: int, numer o 1 mniejszy niż końcowy numer naklejki dla jakiej zmieniamy zmienne dane
    '''
    for i in range(start, koniec + 1):
        if 0 <= i < ETYKIETY_PER_PAGE:
            etykiety[i] = dane.copy()
    return etykiety

def main():
    parser = argparse.ArgumentParser(
        description='Generator naklejek do leków recepturowych w rozmiarze A4 w pdf w pliku etykiety.pdf. '
        'Przez uruchomienie aplikacji bez flag generowany jest plik na podstawie danych w pliku etykiety_dane.json.'
        'Dane do etykiet można zmienić w pliku etykiety_dane.json, jeżeli on jeszcze nie istnieje, jest tworzony. ' 
        'Domyślnie edytowane są wszytskie naklejki na stronie przy ustawieniu jakiekolwiek danej zmienne. '
        'Przykładowa komenda: '
        fr'python stickers.py --lek "0,1% sol";"Atropini sulfurici";"10 minimsów" --pos_start 5 --pos_koniec 12 '
        fr'--dr "Dorota Kowalska" --wyk "Anna Nowak" --d "08.11.2025" --exp "30 dni" --p "lodówka"'
    )
    parser.add_argument(
        '--lek',
        type=str,
        default='',
        help='Pole do wypełnienia (3 linie tekstu rozdzielone średnikiem). '
        'Dane dotyczących leku (stężenie, składnik(i) aktywny/e, ilość).',
    )
    parser.add_argument('--dr', type=str, default='', help='Pojedyńcze pole do wypełnienia. Osoba przypisująca lek.')
    parser.add_argument('--wyk', type=str, default='', help='Pojedyńcze pole do wypełnienia. Termin przeterminowania lek.')
    parser.add_argument('--d', type=str, default='', help='Pojedyńcze pole do wypełnienia. Dzień wytworzenia leku.')
    parser.add_argument('--exp', type=str, default='', help='Pojedyńcze pole do wypełnienia. Termin przeterminowania leku.')
    parser.add_argument('--p', type=str, default='', help='Pojedyńcze pole do wypełnienia. Sposób przechowywania leku.')
    parser.add_argument('--s', type=str, default='', help='Pojedyńcze pole do wypełnienia. Sposób użycia leku.')
    parser.add_argument('--ds', type=str, default='', help='Pojedyńcze pole do wypełnienia. Sposób stosowania leku.')
    parser.add_argument('--pos_start', type=int, default=None, help='Pojedyńcze pole do wypełnienia. Numer pierwszej naklejki, jaka ma być zmieniana.')
    parser.add_argument('--pos_koniec', type=int, default=None, help='Pojedyńcze pole do wypełnienia. Numer ostatniej naklejki, jaka ma być zmieniana.')
    parser.add_argument('--reset', action='store_true', help='Brak pola do wypełnienia. Wyczyść wszystkie etykiety')

    args = parser.parse_args()

    dane = zaladowanie_danych()
    etykiety = dane['etykiety']
    apteka = dane.get('apteka', INF_APTEKI.copy())

    if args.reset:
        etykiety = [PUSTA_ETYKIETA.copy() for _ in range(ETYKIETY_PER_PAGE)]
        dane['etykiety'] = etykiety
        print('ℹ️ Wszystkie etykiety zostały wyczyszczone.')

    linie_leku = args.lek.split(';') if args.lek else ['', '', '']
    while len(linie_leku) < 3:
        linie_leku.append('')

    # Dane dla poszczególnej etykiety, które można zmienić za pomocą konsoli
    dane_etykiety = {
        'Lek': linie_leku[:3],
        'Dr.': args.dr,
        'Wyk': args.wyk,
        'Dnia': args.d,
        'Exp': args.exp,
        'Przechowywać': args.p,
        'Sposób użycia': args.s,
        'D.S': args.ds
    }

    if args.pos_start is not None:
        start = args.pos_start - 1
        koniec = (args.pos_koniec - 1) if args.pos_koniec else start
        etykiety = aktualizuj_etykiete(etykiety, dane_etykiety, start, koniec)
        dane['etykiety'] = etykiety

    zapis_danych(dane)
    stworz_etykiety_pdf(etykiety, apteka)

if __name__ == '__main__':
    main()
