def writeToTxt(file_name, count, list_job):
    """txt写入工具类"""
    f_txt = open(file_name, "a", encoding='utf-8')  # 打开文件
    f_txt.write("共找到" + str(count) + "个适合您的岗位:")  # 写入总职位数
    f_txt.write("\n")

    for job in list_job:  # 循环写入所有工作列表的职位信息
        f_txt.write(
            "*******************************************************************************************************")
        f_txt.write("\n")
        f_txt.write("岗位id：" + job.job_id)
        f_txt.write("\n")
        f_txt.write("岗位名称：" + job.job_name)
        f_txt.write("\n")
        f_txt.write("岗位薪资：" + job.job_salary)
        f_txt.write("\n")
        f_txt.write("公司名称：" + job.job_company)
        f_txt.write("\n")
        f_txt.write("发布时间：" + job.job_release_time)
        f_txt.write("\n")
        f_txt.write("职位类型：" + job.job_type)
        f_txt.write("\n")
        f_txt.write("职责描述：" + job.job_desc)
        f_txt.write("\n")
        f_txt.write("职位链接：" + job.job_link)
        f_txt.write("\n")
        f_txt.write(
            "*******************************************************************************************************")

    f_txt.close()  # 关闭文件
