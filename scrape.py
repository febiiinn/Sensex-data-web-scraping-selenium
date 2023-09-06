#Note: Try to run it in REPL like ipython. I had used ipython while extracting
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep

# BROWSER PROCESSES

# You can choose not to keep it headless and visualize the whole process.
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

driver.get("https://finance.yahoo.com/quote/%5EBSESN/history?p=%5EBSESN")

driver.implicitly_wait(7)# This will apply to all the find elements
wait = WebDriverWait(driver=driver, timeout=5)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-test=dropdown]')))
time_period = driver.find_element(By.XPATH, "//*[@class='C($linkColor) Fz(14px)']")
earliest_year = "1997" #Set the earliest year of whatever time period you choose. 

# Setting and Applying Time Period 
# The page sometimes doesn't apply the changes in one try. So we have to make sure the correct time preiod is selected and applied
while earliest_year not in time_period.text:
  time_period.click()
  max_period = driver.find_element(By.XPATH, "//button[@data-value='MAX']").click()
  # five_yr = driver.find_element(By.XPATH, "//button[@data-value='5_Y']").click() # Data for 5 years. will take less time to be extracted..useful while testing
  apply_btn = driver.find_element(By.XPATH, "//button[@class=' Bgc($linkColor) Bdrs(3px) Px(20px) Miw(100px) Whs(nw) Fz(s) Fw(500) C(white) Bgc($linkActiveColor):h Bd(0) D(ib) Cur(p) Td(n)  Py(9px) Fl(end)']").click()

# Scrolling the Page till the End
while True:
  rows = driver.find_elements(By.XPATH, "//tr[@class= 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)']")
  last_row = driver.find_elements(By.XPATH, "//tr[@class= 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)']")[-1]
  driver.execute_script("arguments[0].scrollIntoView();", last_row)
  # Sleep works the best here. Tried waiting stratergies checking for the last element to be displayed but as all the rows are same it can lead to unwanted complications.
  sleep(2)
  new_page_rows = driver.find_elements(By.XPATH, "//tr[@class= 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)']")
  if len(new_page_rows) > len(rows):
   continue
  else:
   break
  
# Checking the total number of rows in the page 
final_rows = driver.find_elements(By.XPATH, "//tr[@class= 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)']")
print("Total number of days: ",len(final_rows))

# SCRAPING 
from bs4 import BeautifulSoup
import html5lib
import csv

# Defining Functions

def get_day(data):
   try:
      return data[0].text.split()[0]
   except Exception as e:
      print("Day extraction ERROR:",e)
      return ""
   
def get_month(data):
   try:
      return data[0].text.split()[1].strip(",")
   except Exception as e:
      print("Month extraction ERROR:",e)
      return ""
   
def get_year(data):
   try:
      return data[0].text.split()[2]
   except Exception as e:
      print("Year extraction ERROR:",e)
      return ""
   
def get_open(data):
   try:
      return data[1].text
   except Exception as e:
      print("Open extraction ERROR:",e)
      return ""
   
def get_high(data):
   try:
      return data[2].text
   except Exception as e:
      print("High extraction ERROR:",e)
      return ""
   
def get_low(data):
   try:
      return data[3].text
   except Exception as e:
      print("Low extraction ERROR:",e)
      return ""
   
def get_close(data):
   try:
      return data[4].text
   except Exception as e:
      print("Close extraction ERROR:",e)
      return ""
   
def get_adj(data):
   try:
      return data[5].text
   except Exception as e:
      print("Adjusted close extraction ERROR:",e)
      return ""
   
def get_vlm(data):
   try:
      return data[6].text
   except Exception as e:
      print("Volume extraction ERROR:",e)
      return ""
   
page = driver.page_source # The Whole Loaded Page Content
soup = BeautifulSoup(page, "html5lib")
all_rows = soup.find_all("tr", {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})
print("Total rows for scraping: ",len(all_rows))
sensex = {"Day":[], "Month":[], "Year":[], "Open":[], "High":[], "Low":[],"Close":[],"Adj Close":[],"Volume":[]}

for row in all_rows:
   row_elems = row.select("td>span")
   if len(row_elems) < 8:
        sensex["Day"].append(get_day(row_elems))
        sensex["Month"].append(get_month(row_elems))
        sensex["Year"].append(get_year(row_elems))
        sensex["Open"].append(get_open(row_elems))
        sensex["High"].append(get_high(row_elems))
        sensex["Low"].append(get_low(row_elems))
        sensex["Close"].append(get_close(row_elems))
        sensex["Adj Close"].append(get_adj(row_elems))
        sensex["Volume"].append(get_vlm(row_elems))
   else:
      continue
print("\n Extracted all data!")
    
# Saving to a Csv file
with open("data.csv","a",encoding="utf-8",newline="") as file:
   csv_writer = csv.writer(file)
   key_list = list(sensex.keys())
   limit = len(sensex["Day"])
   for i in range(limit):
      csv_writer.writerow(sensex[x][i] for x in key_list)
print("\nFile Saved!")

driver.quit()
print("Browser Closed")
 
# Its Highly Recommended to use it in a REPL Environment like ipython..as it lets you fidget around the code and also to not open the browser every time.