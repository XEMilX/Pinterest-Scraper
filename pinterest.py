from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
def tag(): #this function give you possibility to write your search
    t_text = input("WHAT YOU WANT TO SEARCH FOR : ")
    t_ext = t_text.replace(" ", '%20')
    return t_ext

t_ext = tag()  
print(t_ext)





url = f"https://pl.pinterest.com/search/pins/?q={t_ext}&rs=typed" #url of pinterest  typed search


options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_experimental_option("detach", True)
options.binary_location = "F:\webdrive\chrome-win64\chrome-win64\\chrome.exe" #here chrome.exe location
PATH = r'F:\webdrive\chromedriver.exe' #here your chromedriver.exe location

service = Service(PATH)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()


def image_already_exists(folder_path, file_name): #check if image exist
    file_path = os.path.join(folder_path, file_name)
    return os.path.exists(file_path)

#folder_path = r"F:\pobrane nowe\pythek\webscraping\fun\gierka\zdj"
folder_path = f"G:\{t_ext}" #here directory where it would be saved (folder)
if not os.path.exists(folder_path): #if folder dont exist just create it
    os.makedirs(folder_path)

driver.get(url) 



def log():
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/button/div/div'))
    )
    element.click()
    time.sleep(3)
    em = driver.find_element(By.XPATH,'//*[@id="email"]')
    em.send_keys("")#your email here
    pas= driver.find_element(By.XPATH,'//*[@id="password"]')
    pas.send_keys("")#your password here
    element1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__PWS_ROOT__"]/div/div[1]/div[3]/div/div/div/div/div/div[4]/form/div[7]/button/div'))
    )
    element1.click()
    time.sleep(7)

print(log())

def image_find():
    images = WebDriverWait(driver, 18).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img[src]')))
    
    image_links=[]
    for image in images:
        
        image_links.append(image.get_attribute('src'))
    for link in image_links:
        file_name = link.split('/')[-1]  # Pobierz nazwę pliku z linku
        if image_already_exists(folder_path, file_name):
            print(f"Picture {file_name} exist. Skipped...")
            
            continue
        
        filename = os.path.join(folder_path, file_name)
        with open(filename, 'wb') as f:
            response = requests.get(link)
            f.write(response.content)
    return "Searched"
def scroll():
    for i in range(1,4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
    time.sleep(5)
    
    return "" 
#if something does not work play wth time.sleep function :D 
#if you have better idea to develop this script feel free to conatct me
for i in range(1,12): 
    print(image_find())
    print (scroll())
    print(image_find())
    print (scroll())
    print(image_find())
    print(scroll())

print("end")
