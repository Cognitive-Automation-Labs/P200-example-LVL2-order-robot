"""Template robot with Python."""

# libraries
import Browser
from Browser.utils.data_types import SelectAttribute
from RPA.Dialogs import Dialogs
from RPA.PDF import PDF
import time
import os
import csv

# variables
url = "https://robotsparebinindustries.com/#/robot-order" #"https://usyd.starrezhousing.com/StarRezWeb/"
order_form_filename = "orderFile.csv"
run_archive_filepath = ".\\output\\run_archive\\"
session_count = 3
active_session = True

def download_order_file(filename: str):
        browser = Browser.Browser()
        print("___attemting to download order file___")
        browser.new_browser(downloadsPath=".\\")
        browser.new_context(acceptDownloads=True)
        browser.new_page()
        download_wait_promise = browser.promise_to_wait_for_download(".\\")
        order_file_download = browser.download("https://robotsparebinindustries.com/orders.csv")
        browser.wait_for(download_wait_promise)
        os.replace(order_file_download.get("suggestedFilename"), ".\\" + filename)
        browser.close_browser()
        return(order_file_download)
    


def confirm_constitution_response():
    dialogs = Dialogs()
    dialogs.create_form()
    dialogs.add_title(title="Confirmation of Constitutional Rights")
    dialogs.add_text(value="Before we continue, you must first confirm the below with regards to the order form that the bot completes.")
    dialogs.add_dropdown(element_id="dropdown_selected", label="BY USING THIS ORDER FORM, I GIVE UP ALL MY CONSTITUTIONAL RIGHTS FOR THE BENEFIT OF ROBOTSPAREBIN INDUSTRIES INC.", options=["OK", "Yep", "I guess so...", "No way!"])
    constitution_response = dialogs.request_response()
    return(constitution_response)

def ingest_csv_form_data(filename: str):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'Column values are {", ".join(row)}')
                line_count += 1
        print(f'Processed {line_count} lines.')
        return(csv_reader)

def open_and_complete_form(url: str, constitutional_response: str, csv_filename: str):
    try:
        browser = Browser.Browser()
        browser.open_browser(url)
        button_response = "text=" + constitutional_response
        browser.click(selector=button_response)
        pdf = PDF()
        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            if not os.path.exists(run_archive_filepath):
                os.makedirs(run_archive_filepath)                
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    try:
                        print("Completing order " + row[0])
                        #browser.click(selector="id=head")
                        #time.sleep(2)
                        #browser.keyboard_key(action="press", key="ArrowDown")
                        #browser.keyboard_key(action="press", key="Enter")
                        #browser.press_keys('id=head', "Arrowdown 2", "Enter")
                        #browser.click(selector='xpath=//select/option[@value="'+row[1]+'"]')
                        browser.click(selector='xpath=//form/div/div/div/label[@for="id-body-'+row[2]+'"]')
                        browser.fill_text(selector='xpath=//div/input[@placeholder="Enter the part number for the legs"]', txt=row[3])
                        browser.fill_text(selector="id=address", txt=row[4])
                        browser.select_options_by("id=head", SelectAttribute["value"], str(row[1]))
                        browser.click(selector="id=preview")
                        browser.click(selector="id=order")
                        receipt_html_text = browser.get_text(selector="id=receipt")
                        browser.take_screenshot(selector="id=robot-preview-image", filename="robot-preview-image-"+str(row[0]))
                        pdf.html_to_pdf(receipt_html_text, run_archive_filepath+"receipt_file_"+str(row[0]))
                        browser.click(selector="id=order-another")
                        browser.click(selector=button_response)
                        print("Order complete")
                    except:
                        try:
                            error_message = browser.get_text(selector='xpath=//div[@class="alert alert-danger"]')
                        except:
                            error_message = "unknown error message"
                        finally:
                            print("Failed to process order: " + error_message)
                        browser.close_browser()
                        browser.open_browser(url)
                        button_response = "text=" + constitutional_response
                        browser.click(selector=button_response)
                    finally:
                        print("Getting next order...")
                    
    finally:
        try:
            browser.close_browser()
        finally:
            print("all orders complete")

def end_session():
    print("Goodbye world")

if __name__ == "__main__":
    while active_session == True:
        try:
            print('STARTED: session '+str(session_count)+' started')
            print()
            #download_order_file(filename=order_form_filename)
            #constitution_response = confirm_constitution_response()
            cons_response_selected = "OK" #constitution_response.get('dropdown_selected')
            assert cons_response_selected != "No way!", "Unable to continue as user selected 'No way!' on constitution form."
            open_and_complete_form(url, constitutional_response=cons_response_selected, csv_filename=order_form_filename)
            print()
            print("COMPLETED: all tasks completed")
            active_session == False
            break
        except Exception as err:
            print('''TERMINATED: failed with error message= "''' + str(err) + '''"''')
        finally:
            session_count = session_count + 1
            if session_count > 3:
                active_session == False
                break
            print("ENDED: session "+str(session_count)+" ended")
            end_session()




