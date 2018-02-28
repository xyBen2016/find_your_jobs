from PageObjects import BeautifulSoup, TxtUtils, NoSuchElementException
from PageObjects.BasePageObject import BasePageObject
from DataConfigurations.Job import Job


class PO_guipin(BasePageObject):

    url = "http://www.vvjob.com/gl/"

    def get_data(self, my_driver):
        html = BeautifulSoup(my_driver.page_source, "html.parser")
        list_div = html.find_all("div", {"class": "jobs-list"})

        if len(list_div) <= 0:
            return

        div = list_div[0]
        list_dd = div.find_all("dd")

        for dd in list_dd:
            p1 = dd.find_all("p", {"class": "job-name"})[0]  # work
            str_job_name = p1.find_all("a")[0].get_text()
            str_job_salary = p1.find_all("span")[0].get_text().strip()  # i
            p_time = dd.find_all("p", {"class": "time-btn"})[0]
            str_job_release_time = p_time.find_all("span")[0].get_text()
            p2 = dd.find_all("p", {"class": "corp-name"})[0]  # corp
            str_job_company = p2.find_all(
                "a", {"class": "corpName"})[0].get_text()
            str_job_type = dd.find_all(
                "p", {"class": "type-info"})[0].get_text()  # info
            str_job_desc = dd.find_all("p", {"class": "describe"})[
                0].get_text()  # jobInfo
            self.count += 1
            job = Job(str(self.count), str_job_name, str_job_salary, str_job_company, str_job_release_time, str_job_type,
                      str_job_desc)
            self.list_job.append(job)

    def show_jobs(self):
        print("共找到" + str(self.count) + "个适合您的岗位:")

        for job in self.list_job:
            job.show_info()

        print("共找到%s个合适岗位" % len(self.list_job))

    def find_your_jobs(self):
        self.open()
        self.driver.find_element_by_id("search_jobs").send_keys("软件测试")
        self.driver.find_element_by_xpath(
            '//*[@id="search"]/div[4]/div[1]/form/input[3]').click()

        while True:
            try:
                self.get_data(self.driver)
                li_next = self.driver.find_element_by_class_name("next")
                a_next = li_next.find_element_by_tag_name("a")
                a_next.click()
            except NoSuchElementException:
                break

        self.show_jobs()
        self.driver.quit()

        TxtUtils.writeToTxt(self.count, self.list_job)


if __name__ == "__main__":
    po = PO_guipin()
    po.find_your_jobs()
