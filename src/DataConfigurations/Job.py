class Job:
    job_id = ""  # 职位id
    job_name = ""  # 职位名称
    job_salary = ""  # 薪资
    job_company = ""  # 招聘公司
    job_release_time = ""  # 职位发布时间
    job_type = ""  # 职位类型
    job_desc = ""  # 岗位职责描述

    def __init__(self, job_id, job_name, job_salary, job_company, job_release_time, job_type, job_desc):
        self.job_id = job_id
        self.job_name = job_name
        self.job_salary = job_salary
        self.job_company = job_company
        self.job_release_time = job_release_time
        self.job_type = job_type
        self.job_desc = job_desc

    def show_info(self):
        print("职位id:%s" % self.job_id)
        print("职位名称:%s" % self.job_name)
        print("薪资:%s" % self.job_salary)
        print("招聘公司:%s" % self.job_company)
        print("职位发布时间:%s" % self.job_release_time)
        print("职位类型:%s" % self.job_type)
        print("岗位职责描述:%s" % self.job_desc)
        print("----------------------------------------------")
