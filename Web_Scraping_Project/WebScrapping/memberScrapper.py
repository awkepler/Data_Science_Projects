#Import all required libraries and classes
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import pandas as pd
from WebScrapping import wsLogging
import csv

class clsMemberScrapper:
    __url = ''
    __companyId = ''
    __userId = ''
    __password = ''
    __wsLogging = None
    __chormeBrowser = None
    
    def __init__(self, url, userId, password, wsLogging):
        self.__url = url
        self.__userId = userId
        self.__password = password
        self.__wsLogging = wsLogging
        self.__chormeBrowser = webdriver.Chrome('/Users/amitwalia/Documents/GitHub/DataScience_Projects/Web_Scraping_Project/chromedriver') 

    def getBrowserInstance(self):

        try:
            self.__chormeBrowser.get(self.__url)
            ##time.sleep(3)
            userId = self.__chormeBrowser.find_element_by_name('session_key')
            password = self.__chormeBrowser.find_element_by_name('session_password')
            userId.send_keys(self.__userId + Keys.RETURN)
            password.send_keys(self.__password + Keys.RETURN)
        except Exception as e:
            print(e)
            self.__wsLogging.logException(str(e))

    # Function to identify driver
    def driving(self, x):
        if x.lower().find('data') != -1 or x.lower().find('scien') != -1 or x.lower().find('Data') != -1 or x.lower().find('Scien') != -1 or x.lower().find('machine') != -1:
            return(1)
        else:
            return(0)

    def scrapMemberProfileToCSV(self):
        try:            
            df = pd.read_csv("output_search1.csv")
            
            #df['driver'] = list(map(driving, df['title']))

            #Remove value 0
            #df = df[df.driver != 0]

            #create empty data frame
            Expdf = pd.DataFrame(columns = ['profile', 'expTitle', 'expCompany', 'expDates'])
            Edudf = pd.DataFrame(columns = ['profile', 'eduNname', 'eduDegree', 'eduDates'])
            Skilldf = pd.DataFrame(columns = ['profile', 'skill'])

            #Create big loop
            for profileLink in df.loc[:,'profile']:
                if profileLink == 'https://www.linkedin.com#':     #if it equal link then skip
                    continue 
                time.sleep(2)

                self.__chormeBrowser.get(profileLink)
                time.sleep(2)
                self.__chormeBrowser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(.75)
                self.__chormeBrowser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(.75)
                self.__chormeBrowser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(.75)
                self.__chormeBrowser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(.75)
                self.__chormeBrowser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

                profilePage = BeautifulSoup(self.__chormeBrowser.page_source, 'lxml')

                print(profilePage)
    
                # Experience Section  
                titles = profilePage.find_all('div', class_ = "pv-entity__position-group-pager")
                print(titles)
                companies = profilePage.find_all('span', class_ = "pv-entity__secondary-title")
                dates = profilePage.find_all('h4', class_ = "pv-entity__date-range")

                #Put scraped data into exp_df
                arraylen1 = len(profilePage.find_all('div', class_ = "pv-entity__position-group-pager"))

                profile = profileLink
                exp_titles = list(map(lambda x: x.h3.text.strip(), titles))[0:arraylen1]
                exp_companies = list(map(lambda x: x.text.strip(), companies))[0:arraylen1]
                exp_dates = list(map(lambda x: x.text.strip().split('\n')[-1], dates))[0:arraylen1]
    
                #Education Section 
                institution = profilePage.find_all('div', class_ = "pv-entity__degree-info")
                degree = profilePage.find_all('p', class_ = "pv-entity__degree-name")
                dates = profilePage.find_all('p', class_ = "pv-entity__dates")
 
                #Put scraped data into edu_df
                arraylen2 = len(profilePage.find_all('div', class_ = "pv-entity__degree-info"))

                profile = profileLink
                edu_name = list(map(lambda x: x.text.strip().split('\n')[-1], institution))[0:arraylen2]
                edu_degree = list(map(lambda x: x.text.strip().split('\n')[-1], degree))[0:arraylen2]
                edu_dates = list(map(lambda x: x.text.strip().split('\n')[-1], dates))[0:arraylen2]

                if len(edu_dates) < arraylen2:
                    edu_dates = 'NA'
                
                #Skill Section 
                skill = profilePage.find_all('span', class_ = "pv-skill-category-entity__name-text")
    
                #Put scraped data into a ski_df
                arraylen3 = len(profilePage.find_all('span', class_ = "pv-skill-category-entity__name-text"))
        
                profile = profileLink
                skill = list(map(lambda x: x.text.strip(), skill))[0:arraylen3]
                try:
                    temp1 = pd.DataFrame({'profile':profile, 'expTitle':exp_titles, 'expCompany':exp_companies, 'expDates':exp_dates})
                    temp2 = pd.DataFrame({'profile':profile, 'eduNname':edu_name, 'eduDegree':edu_degree, 'eduDates':edu_dates}) 
                    temp3 = pd.DataFrame({'profile':profile, 'skill':skill})
                    Exp_df = Exp_df.append(temp1)
                    Edu_df = Edu_df.append(temp2)
                    Ski_df = Ski_df.append(temp3)
                    print(profileLink, 'completed')
                except:
                    print(profileLink, 'skipped')
                    continue

            # Reset dataframe index
            Expdf.reset_index()
            Edudf.reset_index()
            Skilldf.reset_index()
        
            # Export results
            Expdf.to_csv("output_experience.csv", index = False,sep='\t', encoding='utf-8')
            Edudf.to_csv("output_education.csv", index = False,sep='\t', encoding='utf-8')
            Skilldf.to_csv("output_skills.csv", index = False,sep='\t', encoding='utf-8')

            # Close Selenium
            self.__chormeBrowser.quit()
        except Exception as e:
            print(e)
            self.__wsLogging.logException(str(e))