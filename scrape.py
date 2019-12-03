import logging
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_list():
    # use creds to create a client to interact with the Google Drive API
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('API-KEY.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("LinkedIn_Connections")

    # Extract and print all of the values
    ws = sheet.get_worksheet(0)
    first_names = ws.col_values(1)
    last_names = ws.col_values(2)
    full_names = list(map(lambda x, y: x + ' ' + y, first_names, last_names))

    return full_names


def write_cells(row, col, string):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('API-KEY.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("LinkedIn_Connections")

    # Extract and print all of the values
    ws = sheet.get_worksheet(0)
    ws.update_cell(row, col, string)
    print(row, col, string)


def delete_row(row):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('API-KEY.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("LinkedIn_Connections")

    # Extract and print all of the values
    ws = sheet.get_worksheet(0)
    ws.delete_row(row)


class ScrapeList:

    def __init__(self, driver):
        self.input_list = get_list()
        self.scrape_mail(driver)

    def scrape_mail(self, driver):
        # print(self.input_list[1:])

        row = 1  # Start on index 2, below header
        col = 3  # C 'Email Address'

        for entry in self.input_list[1:]:
            row += 1

            if len(entry) <= 4:
                delete_row(row)
                row = row - 1

            else:
                try:
                    driver.find_element_by_xpath("//input[@type='text']").click()
                    driver.find_element_by_xpath("//input[@type='text']").clear()
                    driver.find_element_by_xpath("//input[@type='text']").send_keys(entry)
                    logging.info('Entry: %s', entry)
                    driver.find_element_by_xpath("/html/body/header/div/form/div/div/div/div/div[2]/button").click()

                    time.sleep(2)
                    driver.find_element_by_xpath(
                        "(.//*[normalize-space(text()) and normalize-space(.)='{}'])[1]/following::span[3]".format(
                            entry)).click()

                    time.sleep(2)
                    driver.find_element_by_xpath("//*/text()[normalize-space(.)='Contact info']/parent::*").click()

                    time.sleep(2)
                    try:
                        email = driver.find_element_by_xpath("//a[starts-with(@href, 'mailto')]")
                        logging.info('Email: %s', email.text)
                        write_cells(row, col, email.text)
                    except Exception as e:
                        logging.error(e)
                        pass

                    time.sleep(2)
                    # close the contact modal
                    driver.find_element_by_css_selector("button.artdeco-modal__dismiss").click()

                except Exception as e:
                    logging.error(e)
                    pass
