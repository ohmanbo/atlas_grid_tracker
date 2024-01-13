import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def determine_color(value):
    if value.isdigit():
        num = int(value)
        if num == 0:
            return "lightgrey"
        elif num >= 1:
            return "lightblue"  # 밝은 파란색
    return "darkgray"  # 숫자가 아닌 경우

def create_cell_content(cell_name, cell_value):
    color = determine_color(cell_value)
    return f"<div style='background-color: {color}; padding: 10px;'><div>{cell_name}</div><div style='margin-top: 10px;'>{cell_value}</div></div>"

def fetch_data(driver):
    
    WebDriverWait(driver, 300).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-lg-12.gridplayers.noselect.ng-star-inserted"))
    )
    
    data = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".col-lg-12.gridplayers.noselect.ng-star-inserted")
    data = [element.text.strip() for element in elements]
    
    return data 

def main(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    data_history = []

    while True:
        current_data = fetch_data(driver)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_history.append({'time': current_time, 'data': current_data})

        # 오래된 데이터 제거
        if len(data_history) > 180:
            data_history.pop(0)

        # 데이터 파일에 저장
        with open('data.json', 'w') as file:
            json.dump(data_history, file)

        time.sleep(10)

    driver.quit()

main("https://atlas-world.net/cluster/1")