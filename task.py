"""Template robot with Python."""

# libraries
import Browser
import time
import os

# variables
browser = Browser.Browser()
url = "http://rpachallenge.com/" #"https://usyd.starrezhousing.com/StarRezWeb/"

def download_order_file():
    print("___attemting to download order file___")
    browser.new_context(acceptDownloads=True)
    browser.new_page()
    order_file_download = browser.download("https://robotsparebinindustries.com/orders.csv")
    os.replace(order_file_download, ".\\orderFile.csv")
    browser.close_browser()
    print("___order file downloaded___")
    print()
    return(order_file_download)


def open_the_website(url: str):
    browser.open_browser(url)

def complete_form():
    address = "hello world"
    email = "tb@tylorbunting.com"
    lastName = "Bunting"
    phoneNumber = "04104010234"
    companyRole = "Developer"
    firstName = "Tylor"
    company = "CA Labs"
    browser.fill_text('xpath=//input[@ng-reflect-name="labelAddress"]', address)
    browser.fill_text('xpath=//input[@ng-reflect-name="labelLastName"]', lastName)
    browser.fill_text('xpath=//input[@ng-reflect-name="labelEmail"]', email)
    browser.fill_text('xpath=//input[@ng-reflect-name="labelPhone"]', phoneNumber)
    browser.fill_text('xpath=//input[@ng-reflect-name="labelRole"]', companyRole)
    browser.fill_text('xpath=//input[@ng-reflect-name="labelFirstName"]', firstName)
    browser.fill_text('xpath=//input[@ng-reflect-name="labelCompanyName"]', company)
    time.sleep(2)
    browser.click('xpath=//input[@value="Submit"]')
    time.sleep(2)


def end_session():
    browser.close_page()
    nothing = 1 + 1

if __name__ == "__main__":
    try:
        print('STARTED: session started')
        print()
        download_order_file()
        #open_the_website(url)
        #complete_form()
        print()
        print("COMPLETED: all tasks completed")
    except Exception as err:
        print('''TERMINATED: failed with error message= "''' + str(err) + '''"''')
    finally:
        print("ENDED: session ended")
        end_session()


