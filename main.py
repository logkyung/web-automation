import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet('가는 편')
ws.append(['항공사', '출발 시각', '도착 시각', '소요 시간', '가격'])

driver = webdriver.Chrome()
driver.implicitly_wait(3)

url = 'https://flight.naver.com/'
driver.get(url)
time.sleep(1)

# Close popup
popup = driver.find_element_by_css_selector('div.popup_travelclub')
btns = popup.find_elements_by_css_selector('button.btn')
btns[0].click()
time.sleep(1)

# Select departure airport
driver.find_element_by_css_selector('.tabContent_route__1GI8F.select_City__2NOOZ.start').click()
driver.find_element(By.XPATH, '//button[text() = "국내"]').click()
driver.find_element(By.XPATH, '//i[text() = "김해국제공항"]').click()

# Select arrival airport
driver.find_element_by_css_selector('.tabContent_route__1GI8F.select_City__2NOOZ.end').click()
driver.find_element(By.XPATH, '//button[text() = "국내"]').click()
driver.find_element(By.XPATH, '//i[contains(text(), "제주국제공항")]').click()

# Select date
driver.find_element(By.XPATH, '//button[text() = "가는 날"]').click()
time.sleep(3)
driver.find_element(By.XPATH, '//b[text() = "20"]').click()
driver.find_element(By.XPATH, '//b[text() = "24"]').click()

# Search
driver.find_element_by_css_selector('.searchBox_txt__3RoCw').click()
time.sleep(3)

# Full page scroll
last_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if last_height == new_height:
        break
    last_height = new_height

# Scraping top 10 data
flight_list = driver.find_elements_by_css_selector('.domestic_Flight__sK0eA.result')

for i in range(10):
    flight = flight_list[i]
    flight_name = flight.find_element_by_css_selector('b.name').text
    departure_time = flight.find_element(By.XPATH, './/*[@class="route_Route__2UInh"]/span[1]/b').text
    arrival_time = flight.find_element(By.XPATH, './/*[@class="route_Route__2UInh"]/span[2]/b').text
    time_taken = flight.find_element_by_css_selector('i.route_info__1RhUH').text
    price = flight.find_element_by_css_selector('b.domestic_price__1qAgw').text

    ws.append([
        flight_name,
        departure_time,
        arrival_time,
        time_taken,
        price,
    ])


wb.save('부산_제주_항공편.xlsx')

driver.quit()
