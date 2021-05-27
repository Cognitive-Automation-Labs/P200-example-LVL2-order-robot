"""Template robot with Python."""

# libraries
import Browser
from Browser.utils.data_types import SelectAttribute
from RPA.Dialogs import Dialogs
from RPA.PDF import PDF
from RPA.FileSystem import FileSystem
from RPA.HTTP import HTTP
from RPA.Archive import Archive
from RPA.Robocloud.Secrets import Secrets
import os
import json
import csv
import datetime

# variables
website_url = "https://robotsparebinindustries.com/#/robot-order" #"https://usyd.starrezhousing.com/StarRezWeb/"
download_url = "https://robotsparebinindustries.com/orders.csv"
order_form_filename = "orderFile.csv"
run_archive_filepath = os.getcwd() + "\\output\\run_archive"
download_path = os.getcwd() + "\\output\\downloads\\"
session_count = 3
session_complete = False

def set_development_environment_variables():
    with open("./devdata/env.json") as env_in:
        env_file = json.load(env_in)
        for key in env_file:
            os.environ[key] = env_file[key]

def get_and_display_secrets(credential: str):
    secrets = Secrets()
    user_details = secrets.get_secret(credential)["username"]
    print(user_details)

def download_order_file(url: str, filename: str, download_path: str):
    print("___attemting to download order file___")
    try:
        browser = Browser.Browser()
        fileSystem = FileSystem()
        fileSystem.create_directory(download_path)
        browser.new_browser(downloadsPath= download_path)
        browser.new_context(acceptDownloads=True)
        browser.new_page()
        order_file_download = browser.download(url)
        orders_csv_filepath_origin = order_file_download.get("saveAs")
        orders_csv_filepath = download_path + filename
        fileSystem.wait_until_created(orders_csv_filepath_origin)
        fileSystem.copy_file(source= orders_csv_filepath_origin, destination= orders_csv_filepath)
    except Exception as errorMessage:
        print("Unable to download order file: " + str(errorMessage))
    finally:
        browser.close_browser()
    
    print("_____complete download____")
    return(orders_csv_filepath)

def confirm_constitution_response():
    try:
        dialogs = Dialogs()
        dialogs.add_text(text="Before we continue, you must first agree to give your constitutional rights to ROBOTSPAREBIN INDUSTRIES INC.?")
        dialogs.add_drop_down(name="dropdown_selected", options=["OK", "Yep", "I guess so...", "No way!"])
        constitution_response = dialogs.run_dialog(title="Confirmation of Constitutional Rights", width= 480, height= 500)
    except Exception as errorMessage:
        print("Unable to run dialogs: " + str(errorMessage))
    finally:
        dialogs.close_all_dialogs()
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
        fileSystem = FileSystem()
        print(csv_filename)
        with open(csv_filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            if not os.path.exists(run_archive_filepath):
                os.makedirs(run_archive_filepath)   
            else:
                fileSystem.empty_directory(run_archive_filepath) 
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
                        robot_previous_filepath = run_archive_filepath + "\\robot_preview_image_" + str(row[0]) + ".png"
                        browser.wait_for_elements_state(selector="id=robot-preview-image")
                        browser.take_screenshot(selector="id=robot-preview-image",  filename= robot_previous_filepath, fullPage= True)
                        receipt_file_path = run_archive_filepath + "\\receipt_file_"+str(row[0])
                        pdf.html_to_pdf(receipt_html_text, receipt_file_path + ".pdf")
                        browser.click(selector="id=order-another")
                        fileSystem.wait_until_created(robot_previous_filepath)
                        browser.click(selector=button_response)
                        pdf.add_watermark_image_to_pdf(image_path= robot_previous_filepath, output_path= receipt_file_path + "_robot_image.pdf", source_path= receipt_file_path + ".pdf")
                        fileSystem.wait_until_created(path= receipt_file_path + "_robot_image.pdf")
                        print("Order complete")
                    except Exception as errorMessage:
                        try:
                            error_message = browser.get_text(selector='xpath=//div[@class="alert alert-danger"]')
                        except:
                            error_message = errorMessage
                        finally:
                            print("Failed to process order: " + str(error_message))
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

def archive_files(folder_path: str):
    print(folder_path)
    archive = Archive()
    archive.archive_folder_with_zip(folder=folder_path, archive_name= ".\\output\\run-archive-" + str(datetime.date.today()) +".zip", recursive=True)


def end_session():
    print("Goodbye world")

if __name__ == "__main__":
    while session_complete == False:
        try:
            print('STARTED: session '+str(session_count)+' started')
            print()
            set_development_environment_variables()
            get_and_display_secrets(credential= "robotsparebin_cred")
            download_order_file(url=download_url, filename=order_form_filename, download_path= download_path)
            constitution_response = confirm_constitution_response()
            cons_response_selected = constitution_response.get('dropdown_selected')
            assert cons_response_selected != "No way!", "Unable to continue as user selected 'No way!' on constitution form."
            open_and_complete_form(website_url, constitutional_response=cons_response_selected, csv_filename= download_path+order_form_filename)
            archive_files(folder_path= run_archive_filepath)
            print("COMPLETED: all tasks completed")
            session_complete == True
            break
        except Exception as err:
            print('''TERMINATED: failed with error message= "''' + str(err) + '''"''')
        finally:
            session_count = session_count + 1
            if session_count > 3:
                session_complete == True
                break
            print("ENDED: session "+str(session_count)+" ended")
            end_session()




