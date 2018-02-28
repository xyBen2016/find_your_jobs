from PageObjects import webdriver


class BasePageObject:
    list_job = []
    count = 0
    url = ""

    def __init__(self):
        self.driver = webdriver.PhantomJS()

    def open(self):
        self.driver.get(self.url)
