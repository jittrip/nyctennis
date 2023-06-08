from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


prefix = 'https://www.nycgovparks.org'
reserve_link = ''
file_path = "parameters.txt"  # Path to your text file

# Read the contents of the txt file and stores it in parameters
parameters = {}
with open(file_path, "r") as file:
    for line in file:
        key, value = line.strip().split("=")
        parameters[key.strip()] = value.strip()

# Define the XPATHs for the driver to interact
confirm_xpath = '//*[@id="no_account"]/div/input'
singles_xpath = '//*[@id="num_people"]/div/div/label[1]'
doubles_xpath = '//*[@id="num_people"]/div/div/label[2]'
permits_2_xpath = '//*[@id="num_permits"]/div/div/label[3]'
permits_4_xpath = '//*[@id="num_permits"]/div/div/label[5]'
name_xpath = '//*[@id="name"]'
email_xpath = '//*[@id="email"]'
address_xpath = '//*[@id="address"]'
apt_xpath = '//*[@id="address2"]'
city_xpath = '//*[@id="city"]'
zip_xpath = '//*[@id="zip"]'
phone_xpath = '//*[@id="phone"]'
continue_payment_xpath = '//*[@id="form_with_validation"]/input[2]'
ccnum_xpath = '//*[@id="cardNum"]'
expdate_xpath = '//*[@id="expiryDate"]'
cvv_xpath = '//*[@id="cvv"]'
pay_xpath = '//*[@id="payBtn"]'

# Assigns the data stored in parametersto variables
place = parameters['place']
date = parameters['date']
timeslot = parameters['timeslot']
play_type = parameters['play_type']
date_monitor_freq = int(parameters['date_monitor_freq'])
timeslot_monitor_freq = int(parameters['timeslot_monitor_freq'])
name = parameters['name']
email = parameters['email']
address = parameters['address']
apt = parameters['apt']
city = parameters['city']
zipcode = parameters['zipcode']
phone_number = parameters['phone_number']
ccnum = parameters['ccnum']
month = parameters['expdate'].split('/')[0]
year = parameters['expdate'].split('/')[1]
cvv = parameters['cvv']

# Opens webdriver to desired site
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36')
driver = webdriver.Chrome(options=options)
driver.get(place)

soup=BeautifulSoup(driver.page_source, 'html.parser')
# Checks if date is available and clicks on the tab. Else it waits 
works = True
while works:
    try:
        soup.find('a', {'href': date})
        break
    except:
        time.sleep(date_monitor_freq)
        driver.refresh()
        continue

# Parses the HTML and returns the tab table of the date. If timeslot is available, directs driver to reserve link. Otherwise, monitors the page until slot is available
while not reserve_link:
    table_element = soup.find('div', {'id': date}).find_all('tr')
    for index, row in enumerate(table_element):
        if timeslot in row.text and 'Reserve this time' in row.text:
            if play_type == 'singles':
                link = row.find('a')['href']
                reserve_link = prefix + link
                driver.get(reserve_link)
                break
            elif play_type == 'doubles':
                cells = row.find_all('td')
                for place, cell in enumerate(cells):
                    if 'Reserve this time' in cell.text and 'Reserve this time' in table_element[index+1].find_all('td')[place].text:
                        print('2', table_element[index+1].find_all('td')[place])
                        link = cell.find('a')['href']
                        reserve_link = prefix + link
                        driver.get(reserve_link)
                        break
    if not reserve_link:
        time.sleep(timeslot_monitor_freq)
        driver.refresh()

# Fills out reservation details
driver.find_element(By.XPATH, confirm_xpath).click()
if play_type == 'doubles':
    driver.find_element(By.XPATH, doubles_xpath).click()
    driver.find_element(By.XPATH, permits_4_xpath).click()
elif play_type == 'singles':
    driver.find_element(By.XPATH, singles_xpath).click()
    driver.find_element(By.XPATH, permits_2_xpath).click()

driver.find_element(By.XPATH, name_xpath).send_keys(name)
driver.find_element(By.XPATH, email_xpath).send_keys(email)
driver.find_element(By.XPATH, address_xpath).send_keys(address)
driver.find_element(By.XPATH, apt_xpath).send_keys(apt )
driver.find_element(By.XPATH, city_xpath).send_keys(city)
driver.find_element(By.XPATH, zip_xpath).send_keys(zipcode)
driver.find_element(By.XPATH, phone_xpath).send_keys(phone_number)
driver.find_element(By.XPATH, continue_payment_xpath).click()
time.sleep(5)
driver.switch_to.frame(1)

# Enter CC information and pay
try:
    driver.find_element(By.XPATH, ccnum_xpath).send_keys(ccnum)
    driver.find_element(By.XPATH, expdate_xpath).send_keys(month+year)
    driver.find_element(By.XPATH, cvv_xpath).send_keys(cvv)
    driver.find_element(By.XPATH, pay_xpath).click()
except:
    driver.find_element(By.XPATH, '//*[@id="cc_number"]').send_keys(ccnum)
    driver.find_element(By.XPATH, '//*[@id="expdate_month"]').send_keys(month)
    driver.find_element(By.XPATH, '//*[@id="expdate_year"]').send_keys(year)
    driver.find_element(By.XPATH, '//*[@id="cvv2_number"]').send_keys(cvv)
    driver.find_element(By.XPATH, '//*[@id="btn_pay_cc"]').click()

