from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from DataConfigurations import Config, TxtUtils
from PageObjects.BasePageObject import BasePageObject
from DataConfigurations.Job import Job
import time


class PO_51job(BasePageObject):
    """51job前程无忧 page object"""
    url = "http://www.51job.com/"  # 51job前程无忧

    def get_data(self, my_driver):
        """获取职位数据"""
        html = BeautifulSoup(my_driver.page_source, "html.parser")  # BS解析页面内容
        list_div = html.find_all("div", {"id": "resultList"})  # 获取所有的职位列表div

        if len(list_div) <= 0:  # 当列表没有职位时结束操作
            return

        div = list_div[0]
        list_job_div = div.find_all("div", {"class": "el"})  # 得到所有工作div标签
        for div in list_job_div:  # 循环便利并取出职位信息
            ls_p_t1 = div.find_all("p", {"class": "t1"})  # [0]  # work

            if len(ls_p_t1) <= 0:
                continue

            p_t1 = ls_p_t1[0]
            p_t1_a = p_t1.find_all("a")[0]
            str_job_name = p_t1_a.get_text()  # 职位名称
            str_job_link = str(p_t1_a.get("href"))  # 职位链接

            str_job_salary = div.find_all("span", {"class": "t4"})[
                0].get_text()  # 职位薪资
            str_job_release_time = div.find_all("span", {"class": "t5"})[
                0].get_text()  # 职位发布时间
            str_job_company = div.find_all("span", {"class": "t2"})[
                0].get_text()  # 发布公司名称
            str_job_type = div.find_all("span", {"class": "t3"})[
                0].get_text()  # 职位类型
            str_job_desc = "无"  # 职位职责描述
            self.count += 1
            job = Job(str(self.count), str_job_name, str_job_salary, str_job_company, str_job_release_time, str_job_type,
                      str_job_desc, str_job_link)  # 封装对象
            self.list_job.append(job)  # 存入职位列表

    def find_your_jobs(self):
        """开始爬取"""
        self.open()  # 开始加载页面
        self.driver.find_element_by_id("kwdselectid").send_keys(
            Config.JOB_KEYWORD)  # 找到输入框，输入职位信息
        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[1]/div/button').click()  # 找到搜索按钮并点击
        while True:
            try:
                self.get_data(self.driver)  # 获取职位信息
                div_next = self.driver.find_element_by_class_name(
                    "dw_page")  # 找到下一页按钮
                a_next = div_next.find_element_by_link_text("下一页")
                a_next.click()  # 点击下一页按钮
            except NoSuchElementException:  # 当下一页按钮无法找到时结束循环
                break

        self.show_jobs()  # 打印获取到的职位
        self.driver.quit()  # 退出浏览器
        now = time.strftime(' %Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        file_name = r"E:/xy/test/eclipse_python/cx/workspace/find_your_jobs/src/jobs/" + \
            now + "_jobs_51job.txt"
        TxtUtils.writeToTxt(file_name, self.count,
                            self.list_job)  # 将获取到的职位写入txt文档


if __name__ == "__main__":
    po = PO_51job()  # 创建51job page object
    po.find_your_jobs()  # 开始爬取数据
