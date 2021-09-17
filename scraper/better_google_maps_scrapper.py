import sys
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
    return mail_df

# section-directions-trip-0


def get_distance_and_time(sending_location, delivery_location, driver) -> (float, float):
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
        result = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'xB1mrd-T3iPGc-trip-duration delay-light'))
        )
        time_div = result.find_element_by_class_name('xB1mrd-T3iPGc-trip-duration delay-light')
        pass

    except TimeoutException:
        print("Searching for " + sending_location + ", " + delivery_location + " timed out")
        return -1, -1

    return 0, 0


def add_distance_and_time(batch_df: pd.DataFrame):
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
    for locations in batch_df[['sending_location', 'delivery_location']].values:
        sending_location = locations[0]
        delivery_location = locations[1]
        distance, vehicle_time = get_distance_and_time(sending_location, delivery_location, driver)


def main():
    beg_line = int(sys.argv[1])
    batch_size = int(sys.argv[2])
    batch = get_batch(beg_line, batch_size)
    add_distance_and_time(batch)


if __name__ == "__main__":
    main()
