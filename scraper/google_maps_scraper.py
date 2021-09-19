import sys
import time

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

MAIL_DATA_PATH = 'data2.csv'
OUTPUT_DATA_PATH = 'data_with_distance.csv'


def get_batch(start_line, batch_size, filename=MAIL_DATA_PATH) -> pd.DataFrame:
    mail_df = pd.read_csv(filename, sep=';').loc[range(start_line, start_line + batch_size)]
    mail_df = mail_df[mail_df['delivery_date'] != 'nie doszedl']
    # values to be typed in the browser
    mail_df['search_sending_location'] = mail_df['sending_location']
    mail_df['search_delivery_location'] = mail_df['delivery_location']
    return mail_df


# section-directions-trip-0


def get_distance_and_time(sending_location, delivery_location, driver) -> (float, float):
    if sending_location == delivery_location:
        return 0, 0
    search = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "omnibox"))
    )
    fields = driver.find_elements_by_class_name("tactile-searchbox-input")
    sending_loc_field = fields[0]
    delivery_loc_field = fields[1]
    sending_loc_field.clear()
    sending_loc_field.send_keys(sending_location)
    delivery_loc_field.clear()
    delivery_loc_field.send_keys(delivery_location)
    delivery_loc_field.send_keys(Keys.RETURN)
    try:
        # wait until old results disappear
        WebDriverWait(driver, 1).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'xB1mrd-T3iPGc-trip-ij8cu'))
        )
        result = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'xB1mrd-T3iPGc-trip-ij8cu'))
        )
        time_div = result.find_element_by_class_name('xB1mrd-T3iPGc-trip-duration')
        duration_str = time_div.find_element_by_tag_name('span').text
        distance_div = result.find_element_by_class_name('xB1mrd-T3iPGc-trip-tUvA6e')
        distance_str = distance_div.find_element_by_tag_name('div').text
        print('Successfully got the distance ' + distance_str +
              ' and trip duration ' + duration_str + ' for ' + sending_location + ", " + delivery_location)
        return distance_str, duration_str

    except TimeoutException:
        print("Searching for " + sending_location + ", " + delivery_location + " timed out")
        return -1, -1

    except Exception as e:
        print("While searching for " + sending_location + ", " + delivery_location + " exception was thrown:" +
              e.__str__())
        return -1, -1


def get_city_from_sending_location(location):
    if ('UP' not in location) and \
            ('PP' not in location) and \
            ('AP' not in location) and \
            ('DER' not in location):
        return location
    post_office_with_city = location.split('(')[0].rstrip()
    city = post_office_with_city.split(' ')[1:]
    # office nr given
    if city[-1].strip().isnumeric():
        return " ".join(city[:-1])
    return " ".join(city)


def get_city_from_delivery_location(location):
    if ('UP' not in location) and \
            ('PP' not in location) and \
            ('AP' not in location) and \
            ('DER' not in location):
        return location
    without_post_office = location.split(' ')[1:]
    # office nr given
    if without_post_office[-1].strip().isnumeric():
        return " ".join(without_post_office[:-1])
    return " ".join(without_post_office)


def add_distance_and_time(batch_df: pd.DataFrame):
    driver = init_scraper()
    distances = []
    durations = []
    batch_arr = batch_df[['search_sending_location', 'search_delivery_location']].to_numpy()
    for index in range(len(batch_arr)):
        locations = batch_arr[index]
        sending_location = locations[0]
        delivery_location = locations[1]
        distance, vehicle_time = get_distance_and_time(sending_location, delivery_location, driver)
        # try only with city names if exact locations failed
        if (distance, vehicle_time) == (-1, -1):
            sending_city = get_city_from_sending_location(locations[0])
            delivery_city = get_city_from_delivery_location(locations[1])
            distance, vehicle_time = get_distance_and_time(sending_city, delivery_city, driver)
            # do not look for these locations again
            batch_df['search_sending_location'].replace(sending_location, sending_city, inplace=True)
            batch_df['search_delivery_location'].replace(delivery_location, delivery_city, inplace=True)
            # update array
            batch_arr = batch_df[['search_sending_location', 'search_delivery_location']].to_numpy()
        distances.append(distance)
        durations.append(vehicle_time)
    batch_df['distance'] = np.array(distances)
    batch_df['vehicle_travel_time'] = np.array(durations)
    driver.close()
    return batch_df


def init_scraper():
    driver_path = '/home/wojciech/chromedriver/chromedriver'
    driver = webdriver.Chrome(driver_path)
    driver.get(
        "https://www.google.pl/maps/dir/Warszawa/Kielce/@51.0773044,20.9078341,8.5z/data=!4m14!4m13!1m5!1m1!1s0x471ecc669a869f01:0x72f0be2a88ead3fc!2m2!1d21.0122287!2d52.2296756!1m5!1m1!1s0x47178818af891105:0x5025d8b8c0cdcdf3!2m2!1d20.6285676!2d50.8660773!3e0"
    )
    # agree for cookies
    agr = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "AIC7ge"))
    )
    agr_button = agr.find_elements_by_tag_name("button")
    agr_button[1].click()
    return driver


def append_batch_to_file(batch):
    batch.drop(columns=['search_sending_location', 'search_delivery_location'])
    batch.to_csv(OUTPUT_DATA_PATH, header=False, mode='a', sep=';')


def main(beg_line, batch_size):
    batch = get_batch(beg_line, batch_size)
    batch = add_distance_and_time(batch)
    print(batch.to_string())
    append_batch_to_file(batch)
