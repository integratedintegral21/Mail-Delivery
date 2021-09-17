import sys
import numpy as np
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Letter:
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki,
                 ilosc_dni_roboczych, on_time):
        self.data_wyslania = data_wyslania  # 0
        self.data_dotarcia = data_dotarcia  # 1
        self.miejsce_wysylki = miejsce_wysylki  # 2
        self.miejsce_celu = miejsce_celu  # 3
        self.typ = typ  # 4
        self.numer_przesylki = numer_przesylki  # 5
        self.ilosc_dni_roboczych = ilosc_dni_roboczych  # 6
        self.on_time = on_time  # 0 - spozniony, 1 - na czas, 2 - nie wiadomo jeszcze

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


class Letter_ext(Letter):
    def __init__(self, data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki,
                 ilosc_dni_roboczych, on_time, dystans, czas):
        super().__init__(data_wyslania, data_dotarcia, miejsce_wysylki, miejsce_celu, typ, numer_przesylki,
                         ilosc_dni_roboczych, on_time)
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
        line = str(self.data_wyslania) + ';' + str(self.data_dotarcia) + ';' + str(self.miejsce_wysylki) + ';' + str(
            self.miejsce_celu) + ';' + str(self.typ) + ';' + str(self.numer_przesylki) + ';' + str(
            self.on_time) + ';' + str(self.ilosc_dni_roboczych) + ';' + str(self.dystans) + ';' + str(self.czas)
        return line


def split_data(text):  # dostawanie ze stringa daty
    day_and_hour = text.split(" ")
    day = day_and_hour[0].split("-")
    hour = day_and_hour[1].split(":")
    y = datetime.datetime(int(day[0]), int(day[1]), int(day[2]), int(hour[0]), int(hour[1]))
    return y


INPUT_DATA_FILENAME = 'data2.csv'
SAVE_FILENAME = 'wyniki5.txt'

'''
    Plan dzialania:
    0) Argument pozycyjny: nr listu od którego zacząć
    1) Wczytaj data2.csv do obiektu pd.DataFrame
    2) Utwórz listę obiektów klasy Letter na podstawie DataFrame z pkt. 2 
    3) Rozdziel wszystkie listy na zestawy po 30 listow
    4) Iteracja po wszystkich zestawach:
        - Dla każdego obiektu przypisz czas przejazdu i dystans
        - Zestaw zapisz do pliku (doklej na koniec)

'''


# wczytuje dany fragment pliku i zwraca zestaw listow
def get_letters_from_id(text_filename: str, start_id: str, batch_size=4) -> np.array:
    df = pd.read_csv(text_filename, sep=';')
    # print(df)
    df_in_numpy = df.to_numpy()
    # print('-----------------------------------------')
    # print(df_in_numpy)
    # print('**************************************')
    # print(df_in_numpy[0])
    return df_in_numpy[start_id:start_id + batch_size]


# Pobiera pojedyńczy zestaw listów, przypisuje do nich dystans i czas i zwraca je
def get_distance_and_time(mail_batch: np.array) -> np.array:
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get(
        "https://www.google.pl/maps/dir/Warszawa/Kielce/@51.0773044,20.9078341,8.5z/data=!4m14!4m13!1m5!1m1!1s0x471ecc669a869f01:0x72f0be2a88ead3fc!2m2!1d21.0122287!2d52.2296756!1m5!1m1!1s0x47178818af891105:0x5025d8b8c0cdcdf3!2m2!1d20.6285676!2d50.8660773!3e0"
    )

    # przeklikujemy zgode na cookies
    agr1 = WebDriverWait(driver, 3).until(
        # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
        EC.presence_of_element_located((By.CLASS_NAME, "AIC7ge"))
    )
    bt1 = agr1.find_elements_by_tag_name("button")
    bt1[1].click()
    # przeklikujemy zgode na cookies

    listOfDEliveredLetters = []

    for line in mail_batch:
        print("line[0]:", line[0])
        l = Letter(split_data(line[0]), split_data(line[1]), line[2], line[3], line[4], line[5], line[7], line[6])

        fi = WebDriverWait(driver, 3).until(
            # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
            EC.presence_of_element_located((By.CLASS_NAME, "tactile-searchbox-input"))
        )
        fields = driver.find_elements_by_class_name("tactile-searchbox-input")

        tab1 = l.miejsce_wysylki.split()
        tab2 = l.miejsce_celu.split()

        if (tab1[1] == tab2[1]):
            letter_delivered = Letter_ext(l.data_wyslania, l.data_dotarcia, l.miejsce_wysylki, l.miejsce_celu, l.typ,
                                          l.numer_przesylki, l.ilosc_dni_roboczych, l.on_time, 0, 0)
            listOfDEliveredLetters.append(letter_delivered)
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
        # time.sleep(0.4)

        try:  # najpierw probuje po dokladnym adresie, jesli sie nie uda, to wyrzuca blad i idzie do excepta, gdzie zrobi szukanie ogolne
            time.sleep(2)
            block = WebDriverWait(driver, 3).until(
                # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
                EC.presence_of_element_located((By.CLASS_NAME, 'xB1mrd-T3iPGc-trip-duration delay-light'))
            )
            time_bl = block.find_element_by_tag_name("span")
            time1 = time_bl.text
            print(time1)

            dist_block = WebDriverWait(driver, 3).until(
                # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'xB1mrd-T3iPGc-trip-tUvA6e xB1mrd-T3iPGc-trip-K4efff-text'))
            )
            tab2 = dist_block.find_elements_by_tag_name("div")
            distance = tab2[1].text
            print(distance)

            letter_delivered = Letter_ext(l.data_wyslania, l.data_dotarcia, l.miejsce_wysylki, l.miejsce_celu, l.typ,
                                          l.numer_przesylki, l.ilosc_dni_roboczych, l.on_time, time1, distance)
            letter_delivered.self_print()

            listOfDEliveredLetters.append(letter_delivered)
        except:
            try:  # tutaj probujemy adres pomiedzy samymiu tylko miejscowosciami
                field_1.clear()
                field_1.send_keys(tab1[1])
                field_2.clear()
                field_2.send_keys(tab2[1])
                field_2.send_keys(Keys.RETURN)
                # time.sleep(0.4)

                block = WebDriverWait(driver, 3).until(
                    # try-except, przy odnajdowaniu tablicy z info o liscie, bo nie ma 100% pewnosci, ze to dobry numerek
                    EC.presence_of_element_located((By.CLASS_NAME, "section-directions-trip-numbers"))
                )

                time_bl = block.find_element_by_tag_name("span")
                time1 = time_bl.text
                print(time1)

                tab2 = block.find_elements_by_tag_name("div")
                distance = tab2[1].text
                print(distance)

                letter_delivered = Letter_ext(l.data_wyslania, l.data_dotarcia, l.miejsce_wysylki, l.miejsce_celu,
                                              l.typ, l.numer_przesylki, l.ilosc_dni_roboczych, l.on_time, time1,
                                              distance)
                letter_delivered.self_print()

                listOfDEliveredLetters.append(letter_delivered)

            except:
                continue
    print(
        "--------------------------------------------------------------------------------------------------------------")
    print("Lista:", listOfDEliveredLetters)
    numpy_batch = np.array(listOfDEliveredLetters)
    print(
        "--------------------------------------------------------------------------------------------------------------")
    print("Numpy_batch: ", numpy_batch)
    return numpy_batch


def append_batch_to_file(filename: str, mail_batch: np.array) -> None:
    f_2 = open(filename, "a", encoding='utf-8')
    for letter in mail_batch:
        line = letter.to_file()
        f_2.write(line)
        f_2.write('\n')
    f_2.close()
    return None


def main(args):
    start_id = args[1]
    batch = get_letters_from_id(INPUT_DATA_FILENAME, start_id)
    batch_with_distance = get_distance_and_time(batch)
    print(batch_with_distance)
    append_batch_to_file(SAVE_FILENAME, batch_with_distance)


if __name__ == "__main__":
    main(sys.argv)
