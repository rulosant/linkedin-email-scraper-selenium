import logging
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('API Project-Key.json', scope)
client = gspread.authorize(creds)
sheet = client.open("LinkedIn_Connections")
ws = sheet.get_worksheet(0)


def get_list():
    """
    Gets two columns from spreadsheet and join to new list.
    """
    first_names = ws.col_values(1)
    last_names = ws.col_values(2)
    full_names = list(map(lambda x, y: x + ' ' + y, first_names, last_names))

    return full_names


def email_present_in_row(row):
    """
    Checks if there is an entry for the input row.
    """
    if ws.cell(row, 3).value is not '':
        try:
            return True
        except gspread.exception.APIError as e:
            logging.error(e)
            time.sleep(100)
        finally:
            return True


def write_cells(row, col, string):
    """
    Writes to spreadsheet cells.
    """
    ws.update_cell(row, col, string)
    return


def delete_row(row):
    """
    Deletes spreadsheet cells.
    """
    ws.delete_row(row)
    return


class ScrapeList:

    def __init__(self, driver):
        self.input_list = get_list()
        self.scrape_mail(driver)

    def scrape_mail(self, driver):
        """
        Scrapes the GUI for specific data via selenium.
        """
        n = 1
        email_col = 3

        for entry in self.input_list[n:]:

            if n % 100 == 0:
                logging.info('Preventing search limit constraints, by throttling to idle state for 10 min..')
                time.sleep(600)

            if email_present_in_row(n+1):
                n += 1
                logging.info('Email exists..')
                logging.info('Skipping..')
                logging.info('Current row: %s', n)

            elif not email_present_in_row(n+1):
                n += 1
                logging.info('Empty Email cell..')
                logging.info('Current row: %s', n)
                logging.info('Checking entry: %s', entry)

                if len(entry) <= 4:
                    delete_row(n)
                    n -= 1

                try:

                    driver.find_element_by_xpath("//input[@type='text']").click()
                    driver.find_element_by_xpath("//input[@type='text']").clear()
                    driver.find_element_by_xpath("//input[@type='text']").send_keys(entry)
                    driver.find_element_by_xpath("/html/body/header/div/form/div/div/div/div/div[2]/button").click()
                    time.sleep(2)
                    driver.find_element_by_xpath(
                        "(.//*[normalize-space(text()) and normalize-space(.)='{}'])[1]/following::span[3]".format(
                            entry)).click() # Todo: this does not work for all names
                    time.sleep(2)
                    driver.find_element_by_xpath("//*/text()[normalize-space(.)='Contact info']/parent::*").click()
                    time.sleep(2)

                    try:
                        email = driver.find_element_by_xpath("//a[starts-with(@href, 'mailto')]")
                        logging.info('Email: %s', email.text)
                        write_cells(n, email_col, email.text)

                    except Exception as e:
                        logging.error(e)
                        pass

                    time.sleep(2)
                    # close the contact modal
                    driver.find_element_by_css_selector("button.artdeco-modal__dismiss").click()

                    logging.info('Proceeding to next..')

                except Exception as e:
                    logging.error(e)
                    pass

        return
