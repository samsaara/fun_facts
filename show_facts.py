import sys
import requests
import subprocess as sp

from time import sleep
from bs4 import BeautifulSoup as bs


FETCH_PAUSE_SECONDS   = 0.1 # in seconds
CHECK_EVERY_MINUTES   = 15  # in minutes
POPUP_DISPLAY_SECONDS = 10  # in seconds


def check_ubuntu():
    if 'linux' in sys.platform:
        p = sp.Popen('lsb_release -i'.split(), stdout=sp.PIPE).lower()
        if 'ubuntu' in p:
            return True

    return False


assert check_ubuntu, "only works on ubuntu..."


def return_fact():
    cont = requests.get('http://randomfunfacts.com/')
    sleep(FETCH_PAUSE_SECONDS)
    resp = cont.content.decode(errors='ignore')
    soup = bs(resp, 'html.parser')
    fact = soup.findChildren('td')[1].find_all('i')[0].contents[0].strip()
    
    return fact


def main():

    while True:
        fact = return_fact()
        body = fact + "\n\n check more facts on randomfunfacts.com"
        sp.call(f'notify-send -t {POPUP_DISPLAY_SECONDS}000 "Fun Fact" "{body}"', shell=True)
        sleep(CHECK_EVERY_MINUTES * 60)


if __name__ == "__main__":
    main()
