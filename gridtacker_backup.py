from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd

def interpolate_color(min_val, max_val, val, color_start, color_end):
    """숫자에 따라 지정된 두 색상 사이를 점진적으로 변화시키는 함수"""
    if val < min_val:
        return color_start
    if val > max_val:
        return color_end

    ratio = (val - min_val) / (max_val - min_val)
    r = int(color_start[0] + ratio * (color_end[0] - color_start[0]))
    g = int(color_start[1] + ratio * (color_end[1] - color_start[1]))
    b = int(color_start[2] + ratio * (color_end[2] - color_start[2]))
    return f"rgb({r}, {g}, {b})"

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


def save_to_html(data, filename):
    # 셀 이름 생성
    columns = [f"{chr(65 + i)}{j + 1}" for i in range(9) for j in range(9)]
    
    # 데이터와 셀 이름 결합
    combined_data = [create_cell_content(name, value) for name, value in zip(columns, data)]
    
    # 데이터를 9x9 행렬로 재배치 (행과 열 전환)c
    grid_data = [combined_data[i::9] for i in range(9)]
    df = pd.DataFrame(grid_data)

    # HTML로 변환
    html = df.to_html(border=0, justify='center', table_id='myTable', escape=False, index=False, header=False)
    html_style = """
    <html>
    <head>
    <style>
        #myTable {
            width: 640px; 
            height: 640px;
            border-collapse: collapse;
        }
        #myTable td {
            width: 71px; 
            height: 71px;
            text-align: center; 
            vertical-align: middle;
        }
    </style>
    </head>
    <body>
    """ + html + "</body></html>"

    # HTML 파일로 저장
    with open(filename, 'w') as file:
        file.write(html_style)


def open_page(driver, url):
    driver.get(url)

#def fetch_data(driver):
    #data = []
    # CSS 선택자를 사용하여 대기 조건 설정
    #WebDriverWait(driver, 30).until(
    #    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-lg-12.gridplayers.noselect.ng-star-inserted"))
    #)

    # CSS 선택자를 사용하여 데이터 추출 selenium 3.x
    #elements = driver.find_elements_by_css_selector(".col-lg-12.gridplayers.noselect.ng-star-inserted")
    #data = [element.text.strip() for element in elements]
    
    #return data

def fetch_data(driver):
    
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-lg-12.gridplayers.noselect.ng-star-inserted"))
    )
    
    data = []
    elements = driver.find_elements(By.CSS_SELECTOR, ".col-lg-12.gridplayers.noselect.ng-star-inserted")
    data = [element.text.strip() for element in elements]
    
    return data 

def main(url):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(base_dir, 'ChromeDriver', 'chromedriver')

    #driver = webdriver.Chrome(executable_path=chromedriver_path)
    driver = webdriver.Chrome()
    open_page(driver, url)
    grid_data = fetch_data(driver)
    
    driver.quit()
    return grid_data

# 실행

url = "https://atlas-world.net/cluster/1"
grid_data = main(url)
# HTML 파일로 저장
save_to_html(grid_data, 'grid_table.html')
