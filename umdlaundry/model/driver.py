from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Driver:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options)

    """
    Returns:
        headless selenium browser
    """
    def create(self):
        return self.driver
