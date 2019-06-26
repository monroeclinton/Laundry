from umdlaundry.model.driver import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = Driver().create()

    """
    Returns:
        username
    """
    def username(self):
        return self.username

    """
    Returns:
        password
    """
    def password(self):
        return self.password

    """    
    Returns:
        selenium headless driver
    """
    def driver(self):
        return self.driver

    """
    users selenium to login user
    and stores the state
    """
    def login(self):
        self.driver.get("https://shib.idm.umd.edu/cas/login?service=https://login.umd.edu/demo/")

        self.driver.find_element_by_id("username").send_keys(self.username)
        self.driver.find_element_by_id("password").send_keys(self.password)

        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "username")))

        self.driver.find_element_by_name("_eventId_proceed").click()

        # if not redirected, then login unsuccessful
        if not self.status():
            sys.exit("Wrong username or password.")

    """
    Checks if user is logged in

    Returns:
        true if user logged in
        false if user not logged in
    """
    def status(self):
        self.driver.get("https://terpwash.umd.edu/student/laundry/room_summary_srv.php")

        if self.driver.current_url != "https://terpwash.umd.edu/student/laundry/room_summary_srv.php":
            return False

        return True
