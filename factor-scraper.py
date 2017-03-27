import time
from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup
 
browser = webdriver.Firefox() 
browser.get('https://www.factor.ca/Pages/Public/Recipients.aspx')  
time.sleep(5)
# set date to show full range then click search button
browser.find_element_by_id('ctl00_ctl00_body_body_ApprovedStartDateDatePicker_dateInput').clear()
browser.find_element_by_id('ctl00_ctl00_body_body_ApprovedStartDateDatePicker_dateInput').send_keys('1/1/2011')
browser.find_element_by_xpath('//*[@id="body_body_SearchButton"]').click()
time.sleep(5)                
   
while True:
# note: this loop will continue forever if not manually interrupted
	html_source = browser.page_source
	soup = BeautifulSoup(html_source,'html.parser')
    # defines a lst of all trs with class rgRow or rgAltRow
	rows = soup.find_all("tr", { "class":[ "rgRow", "rgAltRow" ]})   
    	try:
            # loop to make a dict for each rows
    		for row in rows:
    			cells = row.find_all('td')
        		data = {
            		'program' : cells[0].get_text(),
            		'recipient_name' : cells[1].get_text(),
            		'artist' : cells[2].get_text(),
            		'collective_initiative' : cells[3].get_text(),
            		'date_approved' : cells[4].get_text(),
            		'total_offer' : cells[5].get_text(),
            		'recipient_province' : cells[6].get_text(),
            		'artist_province' : cells[7].get_text()
        		}
    			print data
    		# click new page, wait for it to load and then restart loop
    		browser.find_element_by_css_selector('input[class=\"rgPageNext\"]').click()
    		time.sleep(5) 
    	except: # [insert code here] if can't click next button make false
        	break
browser.quit()