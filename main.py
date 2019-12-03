import logging
import os

from pyvirtualdisplay import Display
from selenium import webdriver

from login import LoginTarget
from scrape import ScrapeList

logging.getLogger().setLevel(logging.INFO)

BASE_URL = 'https://www.linkedin.com'


def firefox():
    display = Display(visible=0, size=(1200, 900))
    display.start()
    logging.info('Initialized virtual display..')

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('browser.download.folderList', 2)
    firefox_profile.set_preference('browser.download.manager.showWhenStarting', False)
    firefox_profile.set_preference('browser.download.dir', os.getcwd())
    firefox_profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    logging.info('Prepared firefox profile..')

    # Initialize
    browser = webdriver.Firefox(firefox_profile=firefox_profile)
    logging.info('Initialized firefox browser..')

    # Access target site
    browser.get(BASE_URL)
    logging.info('Accessed %s..', BASE_URL)
    logging.info('Page title: %s', browser.title)

    # Login
    LoginTarget(browser)
    logging.info('Page title: %s', browser.title)

    # Information Retrieval
    ScrapeList(browser)

    # Logout
    browser.get(BASE_URL + '/m/logout/')
    logging.info('Logout..')

    # Close session
    browser.quit()
    display.stop()


if __name__ == '__main__':
    firefox()
