from selenium import webdriver


class BasePageObject:
    """page object 基类"""
    list_job = []  # 职位列表
    count = 0  # 职位数
    url = ""  # 网站地址

    def __init__(self):
        self.driver = webdriver.PhantomJS()  # 初始化时创建driver
#         self.driver = webdriver.Chrome(
# executable_path="C:/Program
# Files(x86)/Google/Chrome/Application/chromedriver")

    def open(self):
        self.driver.get(self.url)  # 打开并加载页面

    def show_jobs(self):
        """打印职位列表的所有信息"""
        print("共找到" + str(self.count) + "个适合您的岗位:")

        for job in self.list_job:  # 循环展示列表中所有工作的信息
            job.show_info()

        print("共找到%s个合适岗位" % len(self.list_job))
