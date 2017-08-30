from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import getpass
import time

portalURL = "https://sjsu.okta.com/login/login.htm?fromURI=%2Fhome%2Ftemplate_sps%2F0oa1hgzk5dRQaDNSu0x7%2F2355"

def getUserDetails():
    global studentID
    global password
    global department
    global courseNumber

    studentID = input("Enter your SJSU ID: ")
    password = getpass.getpass("Enter your my.sjsu password: ")

    department = input("Enter the course department: ")
    courseNumber = input("Enter the course number: ")

def automateBrowser():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 12)

    # Login Page
    driver.get(portalURL)

    element = driver.find_element_by_name("username")
    element.send_keys(studentID)

    element = driver.find_element_by_name("password")
    element.send_keys(password)

    element.submit()

    # Home Page
    try:
        wait.until(EC.element_to_be_clickable((By.NAME, "DERIVED_SSS_SCR_SSS_LINK_ANCHOR1")))

    except TimeoutException:
        driver.quit()
        return

    time.sleep(1)
    element = driver.find_element_by_name("DERIVED_SSS_SCR_SSS_LINK_ANCHOR1")
    element.click()

    # Course Search Page
    try:
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "TargetContent")))

    except TimeoutException:
        driver.quit()
        return

    try:
        element = wait.until(EC.visibility_of_element_located((By.NAME, "SSR_CLSRCH_WRK_SUBJECT$0")))

    except TimeoutException:
        driver.quit()
        return

    element.send_keys(department)

    element = driver.find_element_by_name("SSR_CLSRCH_WRK_CATALOG_NBR$1")
    element.send_keys();
    time.sleep(1)

    element = driver.find_element_by_name("SSR_CLSRCH_WRK_CATALOG_NBR$1")
    element.send_keys(courseNumber);

    element = driver.find_element_by_name("CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH")
    element.click()


    # Course Section Selection Page
    try:
        element = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "44749")))

    except TimeoutException:
        driver.quit()
        return

    element.click()


    # Course Section Info Page
    try:
        enrollmentTotal = wait.until(EC.visibility_of_element_located((By.ID, "SSR_CLS_DTL_WRK_ENRL_TOT"))).text

    except TimeoutException:
        driver.quit()
        return

    print("Current enrollment: " + enrollmentTotal)
    driver.quit()

def main():

    getUserDetails()

    while True:
        automateBrowser()

if __name__ == '__main__':
    main()