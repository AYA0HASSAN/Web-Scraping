######################################## Header ##################################################
#   Author : Aya Mohamed Hassan                                                                  #
#   Date : 1/2/2022                                                                              #
#   Version : v1                                                                                 #
#   Program :  Web Scraping to Get all details about a Book in various                            #
#              webpages and save it in CSV file                                                  #                                                                                  #    
##################################################################################################

from selenium import webdriver
import csv
import re
import pandas as pd
import numpy as np
import  time
#######################################################################################################################################
driver = webdriver.Chrome(r"H:\ITI\Data Preparation\WebS\chromedriver.exe")
driver.get("http://books.toscrape.com/catalogue/category/books_1/index.html")

#######################################################################################################################################
#To ensure integrety of Data so that methon convert string stars to interger

def StarConersion(value):
    if value == "One":
        return 1
    elif value == "Two":
        return 2
    elif value == "Three":
        return 3
    elif value == "Four":
        return 4
    elif value == "Five":
        return 5
###################################
# titles = []
# price = []
# stock = []
# stars = []
# upc = []
# tax = []
# category = []
# description = []
allDetails = []
########################################################################################################################################
for c in range(1,51):
    try:
        driver.get("http://books.toscrape.com/catalogue/category/books_1/page-{}.html".format(c))
        print("http://books.toscrape.com/catalogue/category/books_1/page-{}.html".format(c))
        allBooks = driver.find_elements_by_class_name("product_pod")
        links = []
        #get all links for all books
        for i in range(0,len(allBooks)):
            item = allBooks[i]
            a = item.find_element_by_tag_name("h3").find_element_by_tag_name("a").get_property("href")
            links.append(a)
        #get the Data of each link to access each book 
        for link in links:
            driver.get(url=link)
            titles = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/h1")
            
            price = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[1]")
            
            stock = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[2]")
            stock = int(re.findall("\d+",stock.text)[0])
            
            stars = driver.find_element_by_xpath("//*[@id='content_inner']/article/div[1]/div[2]/p[3]").get_attribute("class")
            stars = StarConersion(stars.split()[1])
            
            try :
                description = driver.find_element_by_xpath("//*[@id='content_inner']/article/p")
                description.text
            except :
                description = None
            upc = driver.find_element_by_xpath("//*[@id='content_inner']/article/table/tbody/tr[1]/td")
            
            tax = driver.find_element_by_xpath("//*[@id='content_inner']/article/table/tbody/tr[5]/td")
            
            category = driver.find_element_by_xpath("//*[@id='default']/div/div/ul/li[3]/a")
            
            detail= {
				"1Title":titles.text,
				"2Category":category.text,
				"3Stock": stock,
				"4Stars": stars,
				"5Price":price.text,
				"6Tax":tax.text,
				"7UPC":upc.text,
				"8Description": description}
            allDetails.append(detail)
    except:
        driver.close()

########################################################################################################################################
#Writing the Data in CSV file
# with open("H:\ITI\Data Preparation\Assignments\FullBooksData.csv","w",newline="",encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["BookTitle","Category","Stock","Stars","Price","Taxs","UPC","Description"])
#     for i in range(0,len(titles)):
#         writer.writerow([titles[i],category[i],stock[i],stars[i],price[i],tax[i],upc[i],description[i]])
        
df = pd.DataFrame(allDetails)
df.to_csv("all_pages.csv")

time.sleep(3)
driver.close()