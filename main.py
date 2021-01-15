from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import configparser
import os.path
import time

# ==============
config = configparser.RawConfigParser()
configFilePath = r'config.ini'
config.read(configFilePath)
# ==============
profile = FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.showWhenStarting', config['download']['showWhenStart'])
profile.set_preference('browser.download.dir', config['download']['location'])
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
opts = Options()
opts.headless = bool(config['browser']['headless'])
opts.profile = profile
browser = Firefox(options=opts)
browser.get(config['browser']['initURL'])

def focusInputElement(element):
    element.click()
    element.clear()


def clickLoginButton():
    loginButton = WebDriverWait(browser, float(config['speedtest']['interactWait'])).until(
        EC.presence_of_element_located((By.CLASS_NAME, config['speedtest']['loginButtonClass'])))
    loginButton.click()
    print("> Login button clicked")


def accountAuthenticate():
    [user, password] = WebDriverWait(browser, float(config['speedtest']['interactWait'])).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'input')))
    WebDriverWait(browser, float(config['speedtest']['interactWait'])).until(EC.visibility_of(user))
    WebDriverWait(browser, float(config['speedtest']['interactWait'])).until(EC.visibility_of(password))
    focusInputElement(user)
    user.send_keys(config['speedtest']['accountUser'])
    focusInputElement(password)
    password.send_keys(config['speedtest']['accountPassword'])
    print("> Account successfully filled")
    submitButton = WebDriverWait(browser, float(config['speedtest']['interactWait'])).until(
        EC.presence_of_element_located((By.TAG_NAME, 'button')))
    submitButton.click()
    print("> Successfully submit account")


def clickReportingButton():
    [dashboard, configuration, reporting] = WebDriverWait(browser, float(config['speedtest']['pageWait'])).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, config['speedtest']['reportButtonClass'])))
    reporting.click()
    print("> Successfully clicked Reporting Button")


def clickExportButton():
    exportButton = WebDriverWait(browser, float(config['speedtest']['interactWait'])).until(
        EC.presence_of_element_located((By.CLASS_NAME, config['speedtest']['exportButtonClass'])))
    lesserMonth = "0" if time.gmtime().tm_mon < 10 else ""
    path = '{}/speedtest-results-{}-{}{}-{}.csv'.format(config['download']['location'], time.gmtime().tm_year, lesserMonth, time.gmtime().tm_mon, time.gmtime().tm_mday)
    while not os.path.exists(path):
        ActionChains(browser).move_to_element(exportButton).click().perform()
        print("> Successfully clicked Export Button")
        time.sleep(float(config['speedtest']['downloadSleep']))
        if os.path.isfile(path):
            browser.close()
            break
    print("> Download success")


try:
    clickLoginButton()
    accountAuthenticate()
    clickReportingButton()
    clickExportButton()
except TimeoutException:
    print("An error has been occurred")
