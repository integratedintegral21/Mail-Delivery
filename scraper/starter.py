import sys
import time

from scraper import better_google_maps_scraper

'''
    google maps scraper should be called for small subsets of data instead of the whole dataset
    in order to prevent the website from lagging
'''


def main():
    start_line = int(sys.argv[1])
    batch_size = int(sys.argv[2])
    for line_nr in range(start_line, 68670, batch_size):
        print("Scraper call nr: ", line_nr // batch_size)
        better_google_maps_scraper.main(line_nr, batch_size)
        # cooldown
        time.sleep(0.1)


if __name__ == "__main__":
    main()
