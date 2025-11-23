"""
File: webcrawler.py
Name: 
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def main():
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)

        driver = webdriver.Chrome()

        driver.get('https://www.ssa.gov/oact/babynames/decades/names' + year + '.html')
        try:
            element_present = EC.presence_of_element_located((By.ID, 'specific-element-id'))
            WebDriverWait(driver, 5).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        # Get the entire HTML content of the page
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        # ----- Write your code below this line ----- #
        table = soup.find('table', {'class':'t-stripe'})
        tobdy = table.find('tbody')

        boy, girl = 0, 0
        tags = tobdy.find_all('tr')

        for tag in tags:
            targets = tag.find_all('td')
            if len(targets) >= 5:  # valid lines
                boy_num = targets[2].text
                girl_num = targets[4].text

                boy_num = int(boy_num.strip().replace(',',''))
                girl_num = int(girl_num.strip().replace(',',''))

                boy += boy_num
                girl += girl_num

        print('Total boys:', boy)
        print('Total girls:', girl)




        driver.quit()


if __name__ == '__main__':
    main()
