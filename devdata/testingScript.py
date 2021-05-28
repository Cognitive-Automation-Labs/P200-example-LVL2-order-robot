import Browser

try:
    browser = Browser.Browser()
    browser.open_browser()
except Exception as errorMessage:
    print("Unable to download order file: " + str(errorMessage))
finally:
    browser.playwright.close()
