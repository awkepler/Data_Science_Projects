# Import logging methods and membersScrapper class 
from WebScrapping import wsLogging
from WebScrapping.membersScrapper import clsMembersScrapper
from WebScrapping.memberScrapper import clsMemberScrapper


# Set variable
__companyId = 309694 #input("Enter Company ID: ")
__userId = "waliamit@ymail.com" #input("Enter username: ")
__password = "Hello@123" #input("Enter password: ")
__url = 'https://www.linkedin.com'
__membersCountLimit = 3 # Change as per your preference
__wsLogging = wsLogging 

# Define log settings
__wsLogging.logSettings()

try:
    #__wsLogging.logInfo("Scrap process has started.")
    #__wsLogging.logInfo("Create instance for MembersScrapper class.")
    #members_scrap = clsMembersScrapper(__url, __companyId, __userId, __password, __membersCountLimit, __wsLogging)
    #__wsLogging.logInfo("Get browser instance using getBrowserInstance() method.")
    #members_scrap.getBrowserInstance()
    #__wsLogging.logInfo("Read data and convert to CSV file using scrapToCSV() method.")
    #members_scrap.scrapToCSV()
    #__wsLogging.logInfo("Scrap process has ended.")

    __wsLogging.logInfo("Profile Scrap process has started.")
    __wsLogging.logInfo("Create instance for MemberScrapper class.")
    member_scrap = clsMemberScrapper(__url, __userId, __password, __wsLogging)
    __wsLogging.logInfo("Get browser instance using getBrowserInstance() method.")
    member_scrap.getBrowserInstance()
    __wsLogging.logInfo("Read data and convert to CSV file using scrapToCSV() method.")
    member_scrap.scrapMemberProfileToCSV()
    __wsLogging.logInfo("Scrap process has ended.")
except Exception as e:
    print(e)
    wsLogging.logException(str(e))
