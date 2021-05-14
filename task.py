"""Template robot with Python."""

# libraries
import Browser
from RPA.Dialogs import Dialogs
import time
import os

# variables
url = "https://robotsparebinindustries.com/#/robot-order" #"https://usyd.starrezhousing.com/StarRezWeb/"

def download_order_file():
    try:
        browser = Browser.Browser()
        print("___attemting to download order file___")
        browser.new_context(acceptDownloads=True)
        browser.new_page()
        order_file_download = browser.download("https://robotsparebinindustries.com/orders.csv")
        os.replace(order_file_download, ".\\orderFile.csv")
    finally:
        browser.close_browser()
        print("___order file downloaded___")
        print()
        return(order_file_download)


def confirm_constitution_response():
    dialogs = Dialogs()
    dialogs.create_form()
    dialogs.add_title(title="Confirmation of Constitutional Rights")
    dialogs.add_text(value="Before we continue, you must first confirm the below with regards to the order form that the bot completes.")
    dialogs.add_dropdown(element_id="dropdown_selected", label="BY USING THIS ORDER FORM, I GIVE UP ALL MY CONSTITUTIONAL RIGHTS FOR THE BENEFIT OF ROBOTSPAREBIN INDUSTRIES INC.", options=["OK", "Yep", "I guess so...", "No way!"])
    constitution_response = dialogs.request_response()
    return(constitution_response)

def open_and_complete_form(url: str, constitutional_response: str):
    try:
        browser = Browser.Browser()
        browser.open_browser(url)
        button_response = "text=" + constitutional_response
        browser.click(selector=button_response)
        time.sleep(2)
    finally:
        browser.close_browser()


def complete_form():
    try:
        address = "hello world"
        email = "tb@tylorbunting.com"
        lastName = "Bunting"
        phoneNumber = "04104010234"
        companyRole = "Developer"
        firstName = "Tylor"
        company = "CA Labs"
        browser = Browser.Browser()
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
    except:
        print("___handling for exception___")
    finally:
        print()


def end_session():
    print("Goodbye world")

if __name__ == "__main__":
    try:
        print('STARTED: session started')
        print()
        #download_order_file()
        constitution_response = confirm_constitution_response()
        cons_response_selected = constitution_response.get('dropdown_selected')
        assert cons_response_selected != "No way!", "Unable to continue as user selected 'No way!' on constitution form."
        open_and_complete_form(url, constitutional_response=cons_response_selected)
        print()
        print("COMPLETED: all tasks completed")
    except Exception as err:
        print('''TERMINATED: failed with error message= "''' + str(err) + '''"''')
    finally:
        print("ENDED: session ended")
        end_session()


