import logging
import time
from selenium.webdriver.common.keys import Keys

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from random import randint
from time import sleep

# use creds to create a client to interact with the Google Drive API
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('API Project-Key.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Conexiones")
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
        contacts_today = 0
        max_today = 75 #Max number of contacts to fetch

        email_col = 3
        linkedin_col = 4
        twitter_col = 5
        education_col = 6
        birth_col = 7
        phone_col = 8

        for entry in self.input_list[n:]:
            if contacts_today >= max_today:
                print("Max limit reached. Closing...")
                return

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
                contacts_today += 1
                logging.info('Requests today: %s', contacts_today)
                logging.info('.')                

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
#                    driver.find_element_by_xpath("/html/body/header/div/form/div/div/div/div/div[2]/button").click()

                    time.sleep(2)
                    driver.find_element_by_xpath("//input[@type='text']").send_keys(Keys.DOWN);
                    driver.find_element_by_xpath("//input[@type='text']").send_keys(Keys.RETURN);
#                    driver.find_element_by_xpath(
#                        "(.//*[normalize-space(text()) and normalize-space(.)='{}'])[1]/following::span[3]".format(
#                            entry)).click() # Todo: this does not work for all names
                    time.sleep(4)

#                    driver.find_element_by_xpath("//*/text()[normalize-space(.)='Contact info']/parent::*").click()
#                    time.sleep(2)

                    try:
                        education = driver.find_element_by_xpath("//a[@data-control-name='education_see_more']/span")
                        logging.info('education: %s', education.text)
                        write_cells(n, education_col, education.text)

                    except Exception as e:
#                        write_cells(n, email_col, "no_edu")
                        logging.error(e)
                        pass

#                    driver.find_element_by_xpath("//*/text()[normalize-space(.)='Contact info']/parent::*").click()
                    driver.find_element_by_xpath("//*/text()[normalize-space(.)='Información de contacto']/parent::*").click()
                    time.sleep(2)

                    try:
                        email = driver.find_element_by_xpath("//a[starts-with(@href, 'mailto')]")
                        logging.info('Email: %s', email.text)
                        write_cells(n, email_col, email.text)

                    except Exception as e:
                        write_cells(n, email_col, "N/A")                        
                        logging.error(e)
                        pass

                    try:
                        twitter = driver.find_element_by_xpath("//a[starts-with(@href, 'https://twitter.com/')]")
                        logging.info('Twitter: %s', twitter.text)
                        write_cells(n, twitter_col, twitter.text)

                    except Exception as e:
                        logging.error(e)
                        pass


                    try:
                        linkedin = driver.find_element_by_xpath("//a[starts-with(@href, 'https://www.linkedin.com/')]")
                        logging.info('Linkedin: %s', linkedin.text)
                        write_cells(n, linkedin_col, linkedin.text)

                    except Exception as e:
                        logging.error(e)
                        pass

                    try:

                        birth = driver.find_element_by_xpath('//section[contains(@class, "ci-birthday")]//div//span')
                        logging.info('Birth: %s', birth.text)
                        write_cells(n, birth_col, birth.text)

                    except Exception as e:
                        logging.error(e)
                        pass

                    try:

                        phone = driver.find_element_by_xpath('//section[contains(@class, "ci-phone")]//ul//li//span')
                        logging.info('Phone: %s', phone.text)
                        write_cells(n, phone_col, phone.text)

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

                #Sleep between requests
                delay = randint(5,30)
                print("Sleep: " + str(delay))
                sleep(delay)

        return
