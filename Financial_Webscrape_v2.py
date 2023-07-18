from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service

class Webscrape_stocks():
    def __init__(self):
        global write_file_path
        write_file_path = f"FinancialWebscrape/webpages_prices.csv"
        
    def create_csv_file(self):
        """sets a data storage file"""
        with open(write_file_path, 'w') as f:
            f.write(f"no,name,price\n")
    
    def write_data(self, no, name, price):
        """writes new data"""
        with open(write_file_path, 'a') as f:
            f.write(f"{no},{name},{price}\n")

    def webscrape(self):
        """Read webpage data info into a dictionary"""
        webpages = {}    
        file_path = f"FinancialWebscrape/webpages.csv"
        file_reader = open(file_path,'r')
        next(file_reader)   #Skips first line
        for row, line in enumerate(file_reader):
            webpages[row] = line.strip().split(',')
        file_reader.close() #everything is stored in a dictionary

        s = Service('FinancialWebscrape')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options, service=s)

        accepted = False
        def accept_cookies():
            nonlocal accepted
            if not accepted:
                accept_btn = WebDriverWait(driver, 3).until(ec.element_to_be_clickable((By.CLASS_NAME, "btn")))
                accept_btn.click()
                accepted = True

        """scrape webpages"""
        for key in webpages.keys():
            driver.get(webpages[key][1]) # read webpage
            if webpages[key][2] == 'ft':     
                price = WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.CLASS_NAME, "mod-ui-data-list__value"))).text
                print('Finished: ',webpages[key][1])
            elif webpages[key][2] == 'yahoo':
                if not accepted:
                    accept_cookies()
                price_str = WebDriverWait(driver, 3).until(ec.element_to_be_clickable((By.ID, "quote-summary")))
                price = price_str.text.split('\n')[0].split(' ')[2]
                print('Finished: ',webpages[key][1]) 
            else:
                print(f'Unable to webscrape {webpages[key][1]}!')
            self.write_data(key,webpages[key][0],float(price))
        print('Success!')

if __name__ == '__main__':
    webscrape_app = Webscrape_stocks()
    webscrape_app.create_csv_file()
    webscrape_app.webscrape()