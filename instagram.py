import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from typing import List
import hashtags

def setup(extensions: List[str] = None):
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    chrome_options = Options()
    chrome_options.add_argument("--disable-web-security")

    if extensions is not None:
        for extension in extensions:
            chrome_options.add_extension(extension)

    driver = webdriver.Chrome(desired_capabilities=caps, executable_path='./chromedriver', options=chrome_options)
    driver.get('https://www.instagram.com/')

    return driver


driver = setup([
    # 'Allow CORS Access-Control-Allow-Origin 0.1.6.0.crx',
    'WeCanInstagramPostsExporter-v2.4.crx',
])


def accept_all():
    accept_all_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Accept All"]'))
    )
    accept_all_box.click()


def login(username, password):

    username_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username_box.clear()
    username_box.send_keys(username)
    password_box.clear()
    password_box.send_keys(password)

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    except:
        time.sleep(4)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()


def not_now():
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()


def search(keyword):
    searchbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()
    searchbox.send_keys('#' + keyword)
    # time.sleep(5)
    WebDriverWait(driver, 10)\
        .until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/explore/tags/{}/"]/parent::div'.format(keyword))))\
        .click()

    # searchbox.send_keys(Keys.ENTER)
    # time.sleep(3)
    # searchbox.send_keys(Keys.ENTER)
    # time.sleep(5)


def loop(parentElement: WebElement = None):
    root = parentElement
    cnt = 0
    while parentElement is not None:

        element = parentElement.find_element(By.XPATH, "./div")
        while element is not None:

            try:
                element.find_element(By.XPATH, "./a")
            except:
                return cnt

            element.click()
            cnt +=1

            time.sleep(5)

            driver.find_element_by_xpath('//*[local-name() = "svg"][@aria-label="Close"]').click()

            try:

                p = element.find_element(By.XPATH, "./following::div").find_element(By.XPATH, './parent::div')
                if p.id != parentElement.id:
                    element = None
                else:
                    element = element.find_element(By.XPATH, "./following::div")
            except:
                element = None

        try:
            parentElement = parentElement.find_element(By.XPATH, "./following::div")
        except:

            try:
                driver.execute_script("window.scrollTo(0, 4000);")
                # parentElement = parentElement.find_element(By.XPATH, "./following::div")

                p2 = parentElement.find_element(By.XPATH, "./following::div").find_element(By.XPATH, './parent::div')
                if p2.id != root.id:
                    parentElement = None
                else:
                    parentElement = parentElement.find_element(By.XPATH, "./following::div")
            except:
                parentElement = None
    return cnt


def check_top_posts():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//h2/div[contains(text(), "Top posts")]/following::div/div')))

    try:
        parentElement = driver.find_element_by_xpath('//h2/div[contains(text(), "Top posts")]/following::div/div/div')
    except:
        parentElement = None

    return loop(parentElement)


def check_recent_posts():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(), "Most recent")]/following::div/div')))

    try:
        parentElement = driver.find_element_by_xpath('//h2[contains(text(), "Most recent")]/following::div/div/div')
    except:
        parentElement = None

    return loop(parentElement)


def scroll():
    SCROLL_PAUSE_TIME = 10
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# accept_all()
# login()




login('shahrad__azimi', '09210837687')
# login('wecan_co', '11315366666')


not_now()


for hash_tag in hashtags.get_hashtags():
    search(hash_tag)
    scroll()

    # print(check_top_posts() + check_recent_posts())

