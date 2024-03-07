# all essential functions
from datetime import datetime
from uuid import uuid4
import os
import requests
import time
import random
import string
import pathlib
import json
from bs4 import BeautifulSoup
import os
import requests
# global variables
cwd = os.getcwd()
def Cclear():
    os.system('cls' if os.name == 'nt' else 'clear')
def ctime(wdm="both"): #current datetime
    now = datetime.now()
    dts = now.strftime("%d/%m/%Y %H:%M:%S")
    if wdm == "time":
        return dts.split(" ")[1]
    elif wdm == "date":
        return dts.split(" ")[0]
    else:
        return dts
def clog(comment: str, error: str = None):
    configclog = {
        "log_printout" : "True",
        "errorlog_dir": "test.txt",
        "log_dir": "log.txt"

    }
    # print(clogconfig)
    logStr = f"[+][{ctime()}][{comment}] {('Error: '+error) if error else ''}"
    if configclog["log_printout"] == "True":
        print(logStr)
    if error is not None:
        log_dir = configclog['errorlog_dir']
    else:
        log_dir = cwd+configclog["log_dir"]
    try:
        with open(log_dir, "a") as clog_writer:
            clog_writer.write(logStr+"\n")
            clog_writer.close()
    except Exception as error:
        print(error)

def tid_gen(length:int = 7):

    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return str(res)

def notice_scrapper():
    if "noticeboard.html" not in os.listdir():
        html_doc = requests.get("https://daffodilvarsity.edu.bd/noticeboard").text
        with open("noticeboard.html", "w") as datawriter:
            datawriter.write(html_doc)
            datawriter.close()
    else:
        html_doc = open("noticeboard.html", "r").read()
    soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())
# print(soup.find_all('a'))
    mydivs = soup.find_all("div", {"class": "row full-notice mb-2"})
    departmental_notices = {}
    # print(mydivs)
    counter = 1
    for i in mydivs:
        # print(i)
        # print("\n")
        department_name = i.find("div", {"class": "depart-short"}).get_text().strip()
        if department_name == "cse":
            # print(department_name)
            # print(i)
            notice_link = i.find("div", {"class": "notice-btn"}).a.get("href")
            notice_date = i.find("div", {"class": "col-md-3"}).get_text()
            notice_title = i.find("div", {"class": "notice-btn"}).strong.get_text()

            departmental_notices[f'notices_{counter}'] = {
                "dept_name": department_name,
                "notice_link": notice_link,
                "notice_title": notice_title,
                "notice_date": notice_date
            }
            counter+=1
            break
    #print(departmental_notices)
    departmental_notices = departmental_notices.get("notices_1")

    response = f"""
    <b>Departmental Notices: {departmental_notices.get("dept_name")}</b>\n
    <b>Title</b>: {departmental_notices.get("notice_title")}\n
    <b>Date</b>: {departmental_notices.get("notice_date")}\n
    <b>Link</b>: {departmental_notices.get("notice_link")}\n
    
    """
    return response

if __name__ == "__main__":

    pass