from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from DataConfigurations import Config, TxtUtils
from PageObjects.BasePageObject import BasePageObject
from DataConfigurations.Job import Job
import time


class PO_gxrc(BasePageObject):
    """广西人才网page object"""
    url = "http://www.gxrc.com/"  # 广西人才网

    def get_data(self, my_driver):
        """获取职位数据"""
        html = BeautifulSoup(my_driver.page_source, "html.parser")  # BS解析页面内容
        list_div = html.find_all(
            "div", {"class": "posDetailWrap"})  # 获取所有的职位列表div

        if len(list_div) <= 0:  # 当列表没有职位时结束操作
            return

        div = list_div[0]
        list_job_div = div.find_all("div")  # 得到所有工作div标签

        for div in list_job_div:  # 循环便利并取出职位信息
            ls_posDetailUL = div.find_all(
                "ul", {"class": "posDetailUL clearfix"})  # work

            if len(ls_posDetailUL) <= 0:
                continue

            posDetailUL = ls_posDetailUL[0]
            w1 = posDetailUL.find_all("li", {"class": "w1"})[0]
            str_job_name = w1.find_all("a")[0].get_text()  # 职位名称
            str_job_link = w1.find_all("a")[0].get("href")  # 职位链接
            w3 = div.find_all("li", {"class": "w3"})[0]
            str_job_salary = w3.get_text().strip()  # 职位薪资
            w5 = div.find_all("li", {"class": "w5"})[0]
            str_job_release_time = w5.get_text()  # 职位发布时间
            w2 = div.find_all("li", {"class": "w2"})[0]  # corp
            str_job_company = w2.find_all(
                "a", {"class": "entName"})[0].get_text()  # 发布公司名称
            str_job_type = div.find_all("ul", {"class": "qitaUL"})[
                0].get_text()  # 职位类型
            job_desc = div.find_all("div", {"class": "info"})[0]
            str_job_desc = job_desc.find_all("span", {"class": "posInfo"})[
                0].get_text()  # 职位职责描述
            self.count += 1
            job = Job(str(self.count), str_job_name, str_job_salary, str_job_company, str_job_release_time, str_job_type,
                      str_job_desc, str_job_link)  # 封装对象
            self.list_job.append(job)  # 存入职位列表

    def find_your_jobs(self):
        """开始爬取"""
        self.open()  # 开始加载页面
        self.driver.find_element_by_id("txt_Keyword").send_keys(
            Config.JOB_KEYWORD)  # 找到输入框，输入职位信息
        self.driver.find_element_by_id("txt_city").click()  # 选择地区
        div_cityBox = self.driver.find_element_by_xpath('//*[@id="cityBox"]')
        a_city_3 = div_cityBox.find_element_by_id("city_3")
        a_city_3.find_element_by_class_name("icon-checkbox").click()
        div_cityBox.find_element_by_class_name("btn-ok").click()
        self.driver.find_element_by_id("btn_Search").click()  # 找到搜索按钮并点击
        new_window = self.driver.window_handles[1]
        self.driver.close()
        self.driver.switch_to.window(new_window)

        while True:
            try:
                self.get_data(self.driver)  # 获取职位信息
                li_next = self.driver.find_element_by_class_name(
                    "PagedList-skipToNext")  # 找到下一页按钮
                a_next = li_next.find_element_by_tag_name("a")
                a_next.click()  # 点击下一页按钮
            except NoSuchElementException:  # 当下一页按钮无法找到时结束循环
                break

        self.show_jobs()  # 打印获取到的职位
        self.driver.quit()  # 退出浏览器
        now = time.strftime(' %Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
        file_name = r"E:/xy/test/eclipse_python/cx/workspace/find_your_jobs/src/jobs/" + \
            now + "_jobs_gxrc.txt"
        TxtUtils.writeToTxt(file_name, self.count,
                            self.list_job)  # 将获取到的职位写入txt文档


if __name__ == "__main__":
    po = PO_gxrc()  # 创建桂聘人才网page object
    po.find_your_jobs()  # 开始爬取数据
