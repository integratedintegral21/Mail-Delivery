import sys
import numpy as np
import pandas as pd

INPUT_DATA_FILENAME = 'data2.txt'
SAVE_FILENAME = 'wyniki4.txt'

'''
    Plan dzialania:
    0) Argument pozycyjny: nr listu od którego zacząć
    1) Wczytaj data2.txt do obiektu pd.DataFrame
    2) Utwórz listę obiektów klasy Letter na podstawie DataFrame z pkt. 2 
    3) Rozdziel wszystkie listy na zestawy po 30 listow
    4) Iteracja po wszystkich zestawach:
        - Dla każdego obiektu przypisz czas przejazdu i dystans
        - Zestaw zapisz do pliku (doklej na koniec)
        
'''


# wczytuje dany fragment pliku i zwraca zestaw listow
def get_letters_from_id(csv_filename: str, start_id: str, batch_size=30) -> np.array:
    return np.array([])


# Pobiera pojedyńczy zestaw listów, przypisuje do nich dystans i czas i zwraca je
def get_distance_and_time(mail_batch: np.array) -> np.array:
    return np.array([])


def append_batch_to_file(filename: str, mail_bacth: np.array) -> None:
    return None


def main(args):
    start_id = args[1]
    batch = get_letters_from_id(INPUT_DATA_FILENAME, start_id)
    batch_with_distance = get_distance_and_time(batch)
    append_batch_to_file(SAVE_FILENAME, batch_with_distance)


if __name__ == "__main__":
    main(sys.argv)
