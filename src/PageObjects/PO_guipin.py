from PageObjects import BeautifulSoup, NoSuchElementException
from DataConfigurations import Config, TxtUtils
from PageObjects.BasePageObject import BasePageObject
from DataConfigurations.Job import Job
import time


class PO_guipin(BasePageObject):
    """桂聘人才网page object"""
    url = "http://www.vvjob.com/gl/"  # 桂聘人才网

    def get_data(self, my_driver):
        """获取职位数据"""
        html = BeautifulSoup(my_driver.page_source, "html.parser")  # BS解析页面内容
        list_div = html.find_all("div", {"class": "jobs-list"})  # 获取所有的职位列表div

        if len(list_div) <= 0:  # 当列表没有职位时结束操作
            return

        div = list_div[0]
        list_dd = div.find_all("dd")  # 得到所有工作dd标签

        for dd in list_dd:  # 循环便利并取出职位信息
            p1 = dd.find_all("p", {"class": "job-name"})[0]  # work
            str_job_name = p1.find_all("a")[0].get_text()  # 职位名称
            str_job_salary = p1.find_all("span")[0].get_text().strip()  # 职位薪资
            p_time = dd.find_all("p", {"class": "time-btn"})[0]
            str_job_release_time = p_time.find_all(
                "span")[0].get_text()  # 职位发布时间
            p2 = dd.find_all("p", {"class": "corp-name"})[0]  # corp
            str_job_company = p2.find_all(
                "a", {"class": "corpName"})[0].get_text()  # 发布公司名称
            str_job_type = dd.find_all(
                "p", {"class": "type-info"})[0].get_text()  # 职位类型
            str_job_desc = dd.find_all("p", {"class": "describe"})[
                0].get_text()  # 职位职责描述
            self.count += 1
            job = Job(str(self.count), str_job_name, str_job_salary, str_job_company, str_job_release_time, str_job_type,
                      str_job_desc)  # 封装对象
            self.list_job.append(job)  # 存入职位列表

    def find_your_jobs(self):
        """开始爬取"""
        self.open()  # 开始加载页面
        self.driver.find_element_by_id(
            "search_jobs").send_keys(Config.JOB_KEYWORD)  # 找到输入框，输入职位信息
        self.driver.find_element_by_xpath(
            '//*[@id="search"]/div[4]/div[1]/form/input[3]').click()  # 找到搜索按钮并点击

        while True:
            try:
                self.get_data(self.driver)  # 获取职位信息
                li_next = self.driver.find_element_by_class_name(
                    "next")  # 找到下一页按钮
                a_next = li_next.find_element_by_tag_name("a")
                a_next.click()  # 点击下一页按钮
            except NoSuchElementException:  # 当下一页按钮无法找到时结束循环
                break

        self.show_jobs()  # 打印获取到的职位
        self.driver.quit()  # 退出浏览器
        now = time.strftime(' %Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        file_name = r"E:/xy/test/eclipse_python/cx/workspace/find_your_jobs/src/jobs/" + \
            now + "_jobs_guipin.txt"
        TxtUtils.writeToTxt(file_name, self.count,
                            self.list_job)  # 将获取到的职位写入txt文档


if __name__ == "__main__":
    po = PO_guipin()  # 创建桂聘人才网page object
    po.find_your_jobs()  # 开始爬取数据
