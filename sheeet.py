import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
#import openpyxl
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

options = Options()
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(executable_path=r"xyz\chromedriver.exe", options=options)
driver.get("https://newtrade.sharekhan.com/skweb/trading/optionchainandtools/optionchain")
time.sleep(2)
driver.maximize_window()

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)


def lmn():
    try:
        driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div/loginpage/div/div/div/div/div/div/div[2]/div[1]/form/md-input/span/input").send_keys("xyz")
        driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div/loginpage/div/div/div/div/div/div/div[2]/div[1]/form/div/button").click()
        time.sleep(2)

        driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div/loginpage/div/div/div/div/div/div/div[2]/div/div[1]/div[1]/form/md-input/span/input").send_keys("xyz")
        driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/div/loginpage/div/div/div/div/div/div/div[2]/div/div[1]/div[1]/form/div[4]/div/button").click()
        time.sleep(5)

        ele=driver.find_element_by_id("rangeOption")
        drp=Select(ele)
        drp.select_by_value("string:All")
        time.sleep(3)

        rows=len(driver.find_elements_by_xpath("//*[@id='sort']/tbody/tr"))
        print("Rows:",rows)

        cols=len(driver.find_elements_by_xpath("//*[@id='sort']/tbody/tr[1]/td"))
        print("Cols:",cols)
        time.sleep(3)
        x=rows
        y=cols
        global countr1, countr2
        countr1=1
        countr2=1

        scope=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds=ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
        client=gspread.authorize(creds)
        sheet=client.open("ShareKh").sheet1

        sheet.delete_rows(2, x+1)

        def xyz():
            try:
                sheet.update_cell(1, 22, "Processing")
                global countr1, countr2
                for r in range(countr1, rows + 2):
                    list = []
                    for c in range(countr2, cols + 1):
                        if r != x+1 and c != y+1:
                            val = driver.find_element_by_xpath("//*[@id='sort']/tbody/tr[" + str(r) + "]/td[" + str(c) + "]").text
                            list.append(val)


                        elif r == x+1:
                            now = datetime.now()
                            dt = now.strftime("%d/%m/%Y %H:%M:%S")
                            sheet.update_cell(1, 1, dt)
                            sheet.update_cell(1, 22, "Done")
                            print("HAHA")
                            time.sleep(100)
                            sheet.delete_rows(2, x+1)
                            countr1 = 1
                            countr2 = 1
                            xyz()


                    countr1 += 1
                    print(r,list)
                    sheet.insert_row(list, r+1)
                    time.sleep(2)
                #workbk.save(path)

            except StaleElementReferenceException as Exception:
                print("new")
                xyz()

        xyz()

    except Exception:
        driver.quit()
        print("oops")
        lmn()

lmn()



