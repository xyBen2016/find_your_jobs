import os

if __name__ == "__main__":
    file_path = "E:/xy/test/eclipse_python/cx/workspace/find_your_jobs/src/PageObjects"
    for root, dirs, files in os.walk(file_path):
        for f in files:
            if f[0:3] == "PO_":
                total_file_name = root + "/" + f
                os.system("python " + total_file_name)