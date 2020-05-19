from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time 

def check_login(driver):
    driver.get("https://odyssey.wildcodeschool.com")
    try:
        WebDriverWait(driver, 5).until(EC.title_contains("Odyssey"))
    except TimeoutException:
        return False
    return driver.title == "Odyssey · My journey"

def login(driver, user_name, password):
    """ We got alread redirected here: "https://login.wildcodeschool.com/" """
    driver.find_element_by_id("login-email").send_keys(user_name)
    driver.find_element_by_id("login-password").send_keys(password)
    driver.find_element_by_id("login-submit").click()

def get_challenges(user_name, password, debug = False):

    chrome_options = Options()
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument("user-data-dir=selenium") 
    if not debug:
        chrome_options.add_argument("--headless")
    with webdriver.Chrome(options=chrome_options) as driver:

        # Login
        if not check_login(driver):
            print("try login")
            login(driver, user_name, password)

        try:
            WebDriverWait(driver, 5).until(EC.title_is("Odyssey · My journey"))
        except TimeoutException:
            return []
        driver.get("https://odyssey.wildcodeschool.com/corrections")
        pages = driver.find_elements_by_css_selector("div.ui.pagination.menu a")[-1].get_attribute('href').rsplit('=')[1]
        print(pages)
        codewars_links = []
        other_links = []
        uncommented_links = []
        for page_number in range(1, int(pages)):
            driver.get("https://odyssey.wildcodeschool.com/corrections?page=" + str(page_number))
            elements = driver.find_element_by_class_name("list").find_elements_by_class_name("item")
            for e in elements:
                entry = e.find_element_by_class_name("content").find_element_by_class_name("title")
                link = entry.find_element_by_tag_name("a").get_attribute('href')
                if "commented" not in e.get_attribute('class'):
                    uncommented_links.append(link)
                if 'codewars' in entry.text.lower():
                    codewars_links.append(link)
                else:
                    other_links.append(link)

    print(len(codewars_links))
    print(len(other_links))
    print(len(uncommented_links))
    return uncommented_links

if __name__ == "__main__":
    user_name = "paul.bauriegel@web.de"
    password = input("Password: ")
    login_cookie = "pENG5hhzarBARWHLOgJ%2BW%2F6E2%2FxCHz88L3u9kncId0cKIk%2FMKqOMTd6O6bJgUZUnsi36bukdNkeis0LUHg%2Bf3h3dw19UD8VoFvEEKXutNr5ba75l2LbdK6rRhpDLgUuU%2Bl47gJvUPgLW9FiHPkU%3D--Edp%2BKKa1XHUtd3OR--VcyRvfhVS9A1X%2FSwxkEGAA%3D%3D"
    get_challenges(login_cookie, True, user_name, password)