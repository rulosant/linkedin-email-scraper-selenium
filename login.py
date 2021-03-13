# -*- coding: utf-8 -*-

import logging
from credentials import username, password

class LoginTarget:

    def __init__(self, driver):
        self.login(driver)

    def login(self, driver):
        """
        Login as main user for automated scraping
        :param driver:
        :return:
        """

        login_creds = username
        login_passwd = password

        driver.find_element_by_link_text("Sign in").click()
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(login_creds)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(login_passwd)
#        driver.find_element_by_xpath(
#            "(.//*[normalize-space(text()) and normalize-space(.)='Show'])[1]/following::button[1]").click()
        driver.find_element_by_xpath('//button[contains(text(),"Sign in")]').click()
        logging.info('Login..')
