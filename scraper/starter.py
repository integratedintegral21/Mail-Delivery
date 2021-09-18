import os

BATCH_SIZE = 8
START = 0


def main():
    for batch_nr in range(68670 // BATCH_SIZE):
        print("start wywolania", batch_nr)
        cmd = 'python3 better_google_maps_scrapper.py ' + str(batch_nr * BATCH_SIZE) + ' ' + str(BATCH_SIZE)
        os.system(cmd)


if __name__ == "__main__":
    main()
