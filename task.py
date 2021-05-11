"""Template robot with Python."""

# libraries
import Browser
import time

# variables
browser = Browser.Browser()
url = "http://rpachallenge.com/" #"https://usyd.starrezhousing.com/StarRezWeb/"


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
    print("END SESSION")
    browser.close_browser()


if __name__ == "__main__":
    try:
        open_the_website(url)
        complete_form()
        print("COMPLETED: All tasks completed")
    except Exception as err:
        print('''TERMINATED: error message= "''' + str(err) + '''"''')
    finally:
        end_session()


