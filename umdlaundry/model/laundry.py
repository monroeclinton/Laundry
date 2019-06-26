import time
from bs4 import BeautifulSoup
from umdlaundry.model.user import User
from time import gmtime, strftime

# How many seconds to wait between each check
LOOP_ITERATION_WAIT_SECONDS = 60


class Laundry:

    """
    Gets laundry from site
    """
    def __init__(self, username, password):
        self.user = User(username, password)
        self.laundry = []

    def run(self):
        while True:
            # first check to see if logged in
            if not self.user.status():
                self.user.login()

            self.user.driver.get("https://terpwash.umd.edu/student/laundry/room_summary_srv.php")
            soup = BeautifulSoup(self.user.driver.page_source, "html.parser")
            rows = [tr.findAll("td") for tr in soup.findAll("tr")][3:]

            self.laundry = []
            for dorm in rows:
                print(dorm)
                name = BeautifulSoup(str(dorm.pop(0)), "html.parser").find("a").text.lower().replace(" ", "-")

                # split the number available and number in use
                washer = BeautifulSoup(str(dorm.pop(1)), "html.parser").text.split("/")
                drier = BeautifulSoup(str(dorm.pop(2)), "html.parser").text.split("/")

                print(washer)

                # format into dictionary
                self.laundry.append({
                    "dorm": name,
                    "washer": {
                        "available": int(washer[0][:-1]),
                        "total": int(washer[1][1:]),
                    },
                    "drier": {
                        "available": int(drier[0][:-1]),
                        "total": int(drier[1][1:]),
                    }
                })

            print(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": Laundry Update")

            time.sleep(LOOP_ITERATION_WAIT_SECONDS)

    """
    Returns:
        Array of dorms and the status of laundry in them
    """
    def get(self):
        return self.laundry
