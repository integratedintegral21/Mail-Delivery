# -*- coding: utf-8 -*-
# v10 nowe podejscie, duze zmiany

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from pandasgui import show
import datetime
import time
import sys, os

start_time = time.time()

# nr przesyłki: nr_placówki:0001-1000:cyfra_kontrolna


def split_data(date_text):  # dostawanie ze stringa daty
    day_and_hour = date_text.split(" ")
    day = day_and_hour[0].split("-")
    hour = day_and_hour[1].split(":")
    y = datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(hour[0]), int(hour[1]))
    return y


def count_working_days(date1, date2):  # liczenie dni roboczych wedlug zasad poczty
    date = date1
    counter = 0

    if date.day == date2.day:
        return counter

    while 1:
        date += datetime.timedelta(days=1)
        if date.weekday() < 5:
            counter += 1
        if date.day == date2.day:
            return counter


def check_if_on_time(letter):
    delta = count_working_days(letter.data_wyslania, letter.data_dotarcia)  # roznica dni roboczych
    if letter.typ == 'List polecony ekonomiczny':  # ten ma isc 3 dni
        if delta <= 3:
            return 1  # zdazyl na czas
        else:
            return 0  # spoziony
    elif letter.typ == 'List polecony priorytetowy':  # ten ma isc 1 dzien
        if delta <= 1:
            return 1  # zdazyl na czas
        elif delta == 2 and letter.data_wyslania.hour >= 15:
            return 1
        else:
            return 0  # spoziony
    elif letter.typ == 'Przesyłka firmowa polecona zamiejscowa':
        if delta <= 4:
            return 1
        else:
            return 0
    else:  # jesli to jest inny typ listu, to jest to jakis niestandardowy, nie wiem ile on ma isc, wiec nie bedzie
        # liczony do statystyki
        return 2


def check_if_on_time_2(letter):
    delta = count_working_days(letter.data_wyslania, datetime.date.today())  # roznica dni roboczych
    if letter.typ == 'List polecony ekonomiczny':  # ten ma isc 3 dni
        if delta <= 3:
            return 2  # zdazyl na czas
        else:
            return 0  # spoziony
    elif letter.typ == 'List polecony priorytetowy':  # ten ma isc 1 dzien
        if delta <= 1:
            return 2  # zdazyl na czas
        elif delta == 2 and letter.data_wyslania.hour >= 15:
            return 2
        else:
            return 0  # spoziony
    elif letter.typ == 'Przesyłka firmowa polecona zamiejscowa':
        if delta <= 4:
            return 2
        else:
            return 0
    else:  # jesli to jest inny typ listu, to jest to jakis niestandardowy, nie wiem ile on ma isc, wiec nie bedzie
        # liczony do statystyki
        return 2


def checksum(kod):
    tab = list(kod)
    parity = 1
    suma = 0

    for i in range(2, 19, 1):
        c = int(tab[i])
        if parity:  # zachodzi gdy parity = 1, czyli nieparzysta pozycja
            suma = suma + c * 3
            parity = 0
        else:
            suma = suma + c * 1
            parity = 1
        d = suma % 10

    if d == 0:
        return 0
    else:
        return 10 - d


def create_existing_number(base, number):
    if len(str(number)) == 1:  # gdy mamy jednocyfrowa liczbe
        kod = base + '00' + str(number)
    elif len(str(number)) == 2:  # gdy mamy dwucyfrowa liczbe
        kod = base + '0' + str(number)
    else:  # tu zostaje tylko przypadek trzycyfrowej
        kod = base + str(number)

    kod = kod + str(checksum(kod))
    return kod


def get_inf_1(row, letter_1):
    if row[0].text == "Rodzaj przesyłki" or row[0].text == "Rodzaj przesyłki: ":
        letter_1.typ = row[1].text
    if row[0].text == "Urząd nadania" or row[0].text == "Urząd nadania: ":
        letter_1.miejsce_wysylki = row[1].text

    return letter_1


def get_inf_2(row, letter_1):
    if row[0].text == "Nadanie":
        letter_1.data_wyslania = split_data(row[1].text)
    if (row[0].text == "Doręczono" or row[0].text == "Awizo - przesyłka do odbioru w placówce" or row[
        0].text == "Odebrano w placówce" or row[0].text == "Próba doręczenia" or row[
        0].text == "Decyzja o zwrocie przesyłki" or row[0].text == "Próba doręczenia - dosłanie"):
        if letter_1.miejsce_celu == "nie doszedl":
            letter_1.data_dotarcia = split_data(row[1].text)
            letter_1.miejsce_celu = row[2].text

    return letter_1


class Letter:
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki):
        self.data_wyslania = data_wyslania
        self.data_dotarcia = data_dotarcia
        self.miejsce_wysylki = miejsce_wysylki
        self.miejsce_celu = miejsce_celu
        self.typ = typ
        self.numer_przesylki = numer_przesylki
        self.ilosc_dni_roboczych = 99
        self.on_time = 2  # 0 - spozniony, 1 - na czas, 2 - nie wiadomo jeszcze

    def self_print(self):
        print(self.data_wyslania)
        print(self.data_dotarcia)
        print(self.miejsce_wysylki)
        print(self.miejsce_celu)
        print(self.typ)
        print(self.numer_przesylki)
        print(self.on_time)
        print(self.ilosc_dni_roboczych)
        print("-------------------------------")

    def to_dict(self):
        return {
            'data_wyslania': self.data_wyslania,
            'data_dotarcia': self.data_dotarcia,
            'ilosc_dni_roboczych': self.ilosc_dni_roboczych,
            'czy_na_czas': self.on_time,
            'typ': self.typ,
            'numer_przesylki': self.numer_przesylki,
            'miejsce_wysylki': self.miejsce_wysylki,
            'miejsce_celu': self.miejsce_celu
        }

    def to_file(self):
        line = str(self.data_wyslania) + ';' + str(self.data_dotarcia) + ';' + str(self.miejsce_wysylki) + ';' + str(
            self.miejsce_celu) + ';' + str(self.typ) + ';' + str(self.numer_przesylki) + ';' + str(
            self.on_time) + ';' + str(self.ilosc_dni_roboczych)
        return line


PATH = "/home/wojciech/chromedriver/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://emonitoring.poczta-polska.pl/")

listOfLetters = []

# ------------------------------------------------------- czytyanie dotychczasowego zbioru
f = open('office_bases.txt', 'r')
text = f.read()
f.close()
print(text)
table = text.split(',')
print(table)
list_of_bases = []
for t in table:
    list_of_bases.append(t)
# ------------------------------------------------


for s in list_of_bases:
    base = s  # dla kazdej bazy ze zbioru
    i = 0
    if (
            time.time() - start_time > 600):  # ograniczenie czasowe na 2h, wyrzuci teraz z tej petli while i wroci
        # do glownej po secie, gdzie znowu warunek na 2h
        print("Skonczono po 2h, najblizsza nieprzeobiona baza to:", base)
        break
    while 1:

        number = create_existing_number(base, i)
        field = driver.find_element_by_id("searchInputPostalDelivery")
        field.clear()
        field.send_keys(number)
        field.send_keys(Keys.RETURN)

        i += 1
        if i > 999:  # warunek, zeby wszystkie numery byly prawidlowe
            break

        try:
            time.sleep(0.1)
            info = WebDriverWait(driver, 4).until(
                # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
                EC.presence_of_element_located((By.ID, "infoTable"))
            )
            count = 0  # gdy trafiamy na zajety numerek, trzeba zrestartowac licznik
            letter_1 = Letter(None, "nie doszedl", None, "nie doszedl", None, number)

            # zdobywanie inf o przesylce -------------------------------------------------------------------------------------------------------------------------
            tab = info.find_elements_by_tag_name("tr")  # tablica z inf o przesylce
            for row_number in range(1,
                                    len(tab)):  # dla kazdego wiersza tabeli sprawdzamy czy zawiera potrzebna informacje(poza zerowym, bo on jest jakis dziwny)
                row = tab[row_number].find_elements_by_tag_name("td")
                letter_1 = get_inf_1(row, letter_1)
            # zdobywanie inf o przesylce -------------------------------------------------------------------------------------------------------------------------

            # zdobywanie inf o statusie przesyki -----------------------------------------------------------------------------------------------------------------
            try:  # nie wiadomo czy juz doszlo, stad try-except
                table_tracking = driver.find_element_by_id("eventsTable")
                tab = table_tracking.find_elements_by_tag_name("tr")

                for row_number in range(1,
                                        len(tab)):  # dla kazdego wiersza tabeli sprawdzamy czy zawiera potrzebna
                    # informacje(poza zerowym, bo on jest jakis dziwny)
                    row = tab[row_number].find_elements_by_tag_name("td")
                    letter_1 = get_inf_2(row, letter_1)
                letter_1.ilosc_dni_roboczych = count_working_days(letter_1.data_wyslania, letter_1.data_dotarcia)
                letter_1.on_time = check_if_on_time(letter_1)
                listOfLetters.append(letter_1)

            except Exception as e:
                print('Taki blad: ' + str(e))
                letter_1.on_time = check_if_on_time_2(letter_1)
                listOfLetters.append(letter_1)
                continue
            # zdobywanie inf o statusie przesyki -----------------------------------------------------------------------------------------------------------------

        except Exception as e:  # znaczy, ze pusty numer, poczta nic tu nie przypisala, idziemy do kolejnego
            print('Taki blad: ' + str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            continue

good_l = 0
all_l = 0
good_l_ek = 0
all_l_ek = 0
good_l_pr = 0
all_l_pr = 0
good_fir = 0
all_fir = 0

for x in listOfLetters:
    if x.on_time != 2:  # jesli nie ma 2, to znaczy ze doszedl i trzeba go uwzglednic
        good_l += x.on_time  # jesli doszedl na czas, to on_time jest rowny 1, w przeciwnym razie 0 i wszystko ok
        all_l += 1

        if x.typ == 'List polecony ekonomiczny':
            good_l_ek += x.on_time
            all_l_ek += 1
        if x.typ == 'List polecony priorytetowy':
            good_l_pr += x.on_time
            all_l_pr += 1
        if x.typ == 'Przesyłka firmowa polecona zamiejscowa':
            good_fir += x.on_time
            all_fir += 1

if all_l != 0 and all_l_ek != 0 and all_l_pr != 0:
    print("Na", all_l, "listow ktore powinnny juz byly dojsc,", good_l, "trafilo do adresata")
    print("Skutecznosc poczty:", 100 * good_l / all_l, "%")

    print("Na", all_l_ek, "listow ekonomicznych ktore powinnny juz byly dojsc,", good_l_ek, "trafilo do adresata")
    print("Skutecznosc poczty:", 100 * good_l_ek / all_l_ek, "%")

    print("Na", all_l_pr, "listow priorytetowych ktore powinnny juz byly dojsc,", good_l_pr, "trafilo do adresata")
    print("Skutecznosc poczty:", 100 * good_l_pr / all_l_pr, "%")

print("--- %s seconds ---" % (time.time() - start_time))

f_2 = open("data2.txt", "a", encoding='utf-8')
for l in listOfLetters:
    line = l.to_file()
    f_2.write(line)
    f_2.write('\n')
f_2.close()

df = pd.DataFrame.from_records([l.to_dict() for l in listOfLetters])
show(df)
