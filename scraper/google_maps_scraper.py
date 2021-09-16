# -*- coding: utf-8 -*-
import pandas as pd
from pandasgui import show
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

limit = 30


class Letter:
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time):
        self.data_wyslania = data_wyslania     # 0
        self.data_dotarcia = data_dotarcia     # 1
        self.miejsce_wysylki = miejsce_wysylki # 2 
        self.miejsce_celu = miejsce_celu       # 3
        self.typ = typ                         # 4
        self.numer_przesylki = numer_przesylki # 5
        self.ilosc_dni_roboczych = ilosc_dni_roboczych # 6
        self.on_time = on_time # 0 - spozniony, 1 - na czas, 2 - nie wiadomo jeszcze

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
        line = str(self.data_wyslania) + ';' + str(self.data_dotarcia)  + ';' + str(self.miejsce_wysylki) + ';' + str(self.miejsce_celu) + ';' + str(self.typ) + ';' + str(self.numer_przesylki) + ';' + str(self.on_time) + ';' + str(self.ilosc_dni_roboczych)
        return line


class LetterExt(Letter):
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time, dystans, czas):
        super().__init__(data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki, ilosc_dni_roboczych, on_time)
        self.dystans = dystans
        self.czas = czas

    def self_print(self):
        print("-------------------------------")
        print(self.data_wyslania)
        print(self.data_dotarcia)
        print(self.miejsce_wysylki)
        print(self.miejsce_celu)
        print(self.typ)
        print(self.numer_przesylki)
        print(self.on_time)
        print(self.ilosc_dni_roboczych)
        print(self.dystans)
        print(self.czas)
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
            'miejsce_celu': self.miejsce_celu,
            'dystans': self.dystans,
            'czas': self.czas
        }

    def to_file(self):
        line = str(self.data_wyslania) + ';' + str(self.data_dotarcia)  + ';' + str(self.miejsce_wysylki) + ';' + str(self.miejsce_celu) + ';' + str(self.typ) + ';' + str(self.numer_przesylki) + ';' + str(self.on_time) + ';' + str(self.ilosc_dni_roboczych) + ';' + str(self.dystans) + ';' + str(self.czas)
        return line


def split_data(text): # dostawanie ze stringa daty
    day_and_hour = text.split(" ")
    day = day_and_hour[0].split("-")
    hour = day_and_hour[1].split(":")
    y = datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(hour[0]), int(hour[1]))
    return y


def main():
    listOfLetters = []
    set_1 = set()
    listOfLetters2 = []
    # ------------------------------------------------------- czytyanie dotychczasowego zbioru
    f = open('data3.txt', 'r', encoding='utf-8')
    text = f.read()
    text = text[:-1] # pominiecie ostatniego znaku - czyli \n, bo powoduje to martwy wiersz w tabeli  #usuniecie ostatniego znaku, przy zwyklym pliku odkomentowac
    table = text.split('\n')
    f.close()

    ij = 0
    for t in table: # dla kazdego rekordu
        tab_of_line = t.split(';') # podzial wiersza wedlug przecinkow
        if(tab_of_line[1]!='nie doszedl'):
            letter_1 = Letter(split_data(tab_of_line[0]), split_data(tab_of_line[1]), tab_of_line[2], tab_of_line[3], tab_of_line[4], tab_of_line[5], tab_of_line[7], tab_of_line[6])
            a = len(set_1)
            set_1.add(letter_1.numer_przesylki)
            b = len(set_1)
            if b>a:
                listOfLetters.append(letter_1)

        else:
            letter_1 = Letter(split_data(tab_of_line[0]), tab_of_line[1], tab_of_line[2], tab_of_line[3], tab_of_line[4], tab_of_line[5], tab_of_line[7], tab_of_line[6])

    ij = 0
    # table = table[limit:]
    f = open('data3.txt', 'w', encoding='utf-8')
    for l in listOfLetters:
        if ij >= limit: # zostawiamy tylko te jeszcze nieprzeczytane
            line = l.to_file()
            f.write(line)
            f.write('\n')
        ij += 1
    f.close()
    # ------------------------------------------------
    print("start")
    for l in listOfLetters:
        l.self_print()
    print("koniec")

    PATH = "/home/wojciech/chromedriver/chromedriver"
    driver = webdriver.Chrome(PATH)

    driver.get("https://www.google.pl/maps/dir/Warszawa/Kielce/@51.0773044,20.9078341,8.5z/data=!4m14!4m13!1m5!1m1!1s0x471ecc669a869f01:0x72f0be2a88ead3fc!2m2!1d21.0122287!2d52.2296756!1m5!1m1!1s0x47178818af891105:0x5025d8b8c0cdcdf3!2m2!1d20.6285676!2d50.8660773!3e0")
    # spowalnia po ilus zapytaniach, wiec wylaczyc strone, wlaczyc od nowa i kliknac agree, przy czym na biezaco modyfikowac pliki
    i = 0

    agr1 = WebDriverWait(driver,5).until(  # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
        EC.presence_of_element_located((By.CLASS_NAME, "AIC7ge"))
    )

    bt1 = agr1.find_elements_by_tag_name("button")
    bt1[1].click()

    for l in listOfLetters:

        if(i>=limit):
            f_2 = open("wyniki4.txt","a", encoding='utf-8')
            for l in listOfLetters2:
                line = l.to_file()
                f_2.write(line)
                f_2.write('\n')
            f_2.close()
            break
        i += 1
        try:
            # sekcja zdobywania informacji ze sledzenia
            fi = WebDriverWait(driver,6).until(  # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
                EC.presence_of_element_located((By.CLASS_NAME, "tactile-searchbox-input"))
            )

            fields = driver.find_elements_by_class_name("tactile-searchbox-input")

            tab1 = l.miejsce_wysylki.split()
            tab2 = l.miejsce_celu.split()

            if(tab1[1]==tab2[1]):
                letter_2 = LetterExt(l.data_wyslania, l.data_dotarcia, l.miejsce_wysylki, l.miejsce_celu, l.typ, l.numer_przesylki, l.ilosc_dni_roboczych, l.on_time, 0, 0)
                listOfLetters2.append(letter_2)
                continue

            field_1 = fields[0]
            field_1.clear()
            field_1.send_keys(l.miejsce_wysylki)
            print(l.miejsce_wysylki)
            print(l.miejsce_celu)
            field_2 = fields[1]
            field_2.clear()
            field_2.send_keys(l.miejsce_celu)
            field_2.send_keys(Keys.RETURN)
            time.sleep(0.4)
            try:
                bl = WebDriverWait(driver,6).until(  # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
                    EC.presence_of_element_located((By.CLASS_NAME, "section-directions-trip-numbers"))
                )

                block = driver.find_element_by_class_name("section-directions-trip-numbers")
                time_bl = block.find_element_by_tag_name("span")
                time1 = time_bl.text
                print(time1)

                tab2 = block.find_elements_by_tag_name("div")
                distance = tab2[1].text
                print(distance)

                letter_2 = LetterExt(l.data_wyslania, l.data_dotarcia, l.miejsce_wysylki, l.miejsce_celu, l.typ, l.numer_przesylki, l.ilosc_dni_roboczych, l.on_time, time1, distance)
                letter_2.self_print()

                listOfLetters2.append(letter_2)

            except:
                # f1 = field_1.get_attribute("aria-label")
                # f2 = field_2.get_attribute("aria-label")
                tab1 = l.miejsce_wysylki.split()
                tab2 = l.miejsce_celu.split()

                if(tab1[1]==tab2[1]):
                    letter_2 = LetterExt(l.data_wyslania, l.data_dotarcia, l.miejsce_wysylki, l.miejsce_celu, l.typ, l.numer_przesylki, l.ilosc_dni_roboczych, l.on_time, 0, 0)
                    listOfLetters2.append(letter_2)
                    continue
                else:
                    try:
                        field_1.clear()
                        field_1.send_keys(tab1[1])
                        field_2.clear()
                        field_2.send_keys(tab2[1])
                        field_2.send_keys(Keys.RETURN)
                        time.sleep(0.4)

                        bl = WebDriverWait(driver,5).until(  # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
                            EC.presence_of_element_located((By.CLASS_NAME, "section-directions-trip-numbers"))
                        )

                        block = driver.find_element_by_class_name("section-directions-trip-numbers")
                        time_bl = block.find_element_by_tag_name("span")
                        time1 = time_bl.text
                        print(time1)

                        tab2 = block.find_elements_by_tag_name("div")
                        distance = tab2[1].text
                        print(distance)

                        letter_2 = LetterExt(l.data_wyslania, l.data_dotarcia, l.miejsce_wysylki, l.miejsce_celu, l.typ, l.numer_przesylki, l.ilosc_dni_roboczych, l.on_time, time1, distance)
                        letter_2.self_print()

                        listOfLetters2.append(letter_2)

                    except:
                        continue

        except:
            continue

    driver.quit()


if __name__ == "__main__":
    main()