from selenium import webdriver
from time import sleep
from pathlib import Path
import os
from selenium.webdriver.firefox.service import Service as FirefoxService

ROOT_PATH = Path(__file__).parent.parent

GECKODRIVER_NAME = 'geckodriver'
GECKODRIVER_PATH = ROOT_PATH / 'bin' / GECKODRIVER_NAME

def make_firefox_browser(*options):
    browser_options = webdriver.FirefoxOptions()
    profile = webdriver.FirefoxProfile()
    
    browser_options.profile = profile
    
    if options is not None:
        for option in options:
            browser_options.add_argument(option)
            
    if os.environ.get('SELENIUM_HEADLESS'):
        browser_options.add_argument('--headless')
    
    service = FirefoxService()
    browser = webdriver.Firefox(service=service, 
                                options=browser_options)
    return browser

if __name__ == '__main__':
    browser = make_firefox_browser()
    browser.get('http://www.udemy.com')
    sleep(1)
    browser.quit()