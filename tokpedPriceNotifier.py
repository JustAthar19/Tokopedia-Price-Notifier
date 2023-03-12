from selenium import webdriver
import yagmail
import os
import time



def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("disable_infobars")
    options.add_argument("start-maximized")
    options.add_argument("no-sandbox")
    options.add_argument("disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tokopedia.com/gshockoriginal/casio-general-a500wa-1df-a500wa1df-a500wa-original?extParam=ivf%3Dfalse%26src%3Dsearch")
    return driver



def get_price():
    driver = get_driver()
    element = driver.find_element(by="xpath", value="/html/body/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/div[1]")
    output = float(element.text[2:])
    return output


sender = os.getenv('email')
password = os.getenv('password')
receiver = 'putEmailReceiverHere@gmail.com'
subject = "Tokopedia Notifications"
contentUP = "The price has went up !!"
contentDOWN= "The price has went down !!"
yag = yagmail.SMTP(user=sender, password=password, port=465, host='smtp.gmail.com', smtp_ssl=True)
raw_price = get_price()
prices = [raw_price]


"""the way to compare the two value is to put the real values into a list as a first element
    and then we append the list for the comparable value
"""

while True:
    time.sleep(5)
    raw_price = get_price()
    prices.append(raw_price)
    if prices[-2] < prices[-1]:
        yag.send(to=receiver, subject=subject, contents=contentUP)
    elif prices[-2] > prices[-1]:
        yag.send(to=receiver, subject=subject, contents=contentDOWN)
    del prices[-2] # to prevent the list keep appending

    

    
