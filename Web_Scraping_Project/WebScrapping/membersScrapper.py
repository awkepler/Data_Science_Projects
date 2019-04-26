#Import all required libraries and classes
import pandas as pd  
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from WebScrapping import wsLogging

class clsMembersScrapper:

    __url = ''
    __companyId = ''
    __userId = ''
    __password = ''
    __membersCountLimit = 0
    __wsLogging = None
    __chormeBrowser = None
    
    def __init__(self, url, companyId, userId, password, membersCountLimit, wsLogging):
        self.__url = url
        self.__companyId = companyId
        self.__userId = userId
        self.__password = password
        self.__membersCountLimit = membersCountLimit
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
            #time.sleep(3)
            searchUrl = "https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22" + str(self.__companyId) + "%22%5D"
            self.__chormeBrowser.get(searchUrl)
            #time.sleep(3)
            self.__chormeBrowser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print(e)
            self.__wsLogging.logException(str(e))
    
    def scrapToCSV(self):

        # Create empty dataframe
        df = pd.DataFrame(columns = ['name', 'title', 'location', 'profile'])
        current_url = 'url_placeholder'

        try:
            while True:
                if current_url.find('page=100') != -1:
                    break

                previous_url = current_url
                current_url = self.__chormeBrowser.current_url
                if current_url == previous_url:
                    break

                resultPage = BeautifulSoup(self.__chormeBrowser.page_source, 'lxml')
                resultNames = resultPage.find_all('span', class_ = 'actor-name')
                resultTitles = resultPage.find_all('p', class_ = 'subline-level-1')
                resultLocations = resultPage.find_all('p', class_ = 'subline-level-2')
                resultProfiles = resultPage.find_all('a', class_ = 'search-result__result-link')

                names = list(map(lambda x: x.text, resultNames))
                titles = list(map(lambda x: x.text.replace('\n', ''), resultTitles))
                locations = list(map(lambda x: x.text.replace('\n', ''), resultLocations))
                profiles = list(map(lambda x: self.__url + x['href'], resultProfiles))[::2]
                temp = pd.DataFrame({'name':names, 'title':titles, 'location':locations, 'profile':profiles})

                temp = temp[temp['name'] != 'LinkedIn Member']
                df = df.append(temp)

                if df.shape[0] >= self.__membersCountLimit:
                    break

                nextt = self.__chormeBrowser.find_element_by_class_name('next')
                nextt.click()
                time.sleep(5)

            df.reset_index()
            df.to_csv("output_search1.csv", index = False)
            self.__chormeBrowser.quit()
        
        except Exception as e:
            print(e)
            self.__wsLogging.logException(str(e))