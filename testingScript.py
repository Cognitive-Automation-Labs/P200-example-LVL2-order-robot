import os
import Browser
import shutil
import time


order_form_filename = "orderFileTest.csv"

browser = Browser.Browser()
print("___attemting to download order file___")
browser.new_browser(headless=False, executablePath=".\\", downloadsPath=".\\")
browser.new_context(acceptDownloads=True)
browser.new_page()
#download_wait_promise = browser.wait_for_download(saveAs=".\\")
order_file_download = browser.download("https://robotsparebinindustries.com/orders.csv")
time.sleep(10)
#browser.wait_for(download_wait_promise)
#os.replace((order_file_download.get("saveAs") + "\\" + order_file_download.get("suggestedFilename")).replace("\\\\", "\\"), ".\\" + order_form_filename)
origin_path = order_file_download.get("saveAs") + "\\" + order_file_download.get("suggestedFilename")
print(origin_path)
destination_path = ".\\" + order_form_filename
print(destination_path)
#shutil.move(origin_path, destination_path)
browser.close_browser()
