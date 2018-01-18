'''
Created on Jan 16, 2018

@author: madhu
'''
import unittest
from selenium import webdriver
import time
import logging
import sys

logger = logging.getLogger('siteValidator')
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))
USERNAME = "kmadhu3042008@gmail.com"
PASSWORD = "Asimil91"
CHROMEDRIVER_LOCATION = "../tools/chromedriver"
STRAITTIMES_URL = "http://www.straitstimes.com/"

class SiteValidatorWeb(unittest.TestCase):
    "Class to run tests to Validate the Site"
    
    def setUp(self):
        #Initialize the Selenium driver
        self.driver = webdriver.Chrome(CHROMEDRIVER_LOCATION)
        
    def _login(self, username=USERNAME, password= PASSWORD):
        '''
        Method to login to the site
        username: userid to login
        password: password corresponding to the userid
        '''
        methodName = "_login"
        logger.info("Entering Method: %s" %methodName)
        element = self.driver.find_element_by_xpath("//li[@class='nav-login']//a[text()='Login']")
        self.driver.execute_script("arguments[0].click();", element)
        
        self.driver.find_element_by_name("j_username").send_keys(USERNAME)
        self.driver.find_element_by_name("j_password").send_keys(PASSWORD)
        self.driver.find_element_by_xpath("//button[@type='submit']").submit()
        time.sleep(2)
        
        logger.info("Exiting Method: %s" %methodName)
        
    def _verifyLoggedInUser(self,expectedUser = USERNAME):
        '''
        Method to verify that the logged-in user is same as expected
        expectedUser: Refers to UserId expected to be shown on home page(as logged in user)
        '''
        methodName = "_verifyLoggedInUser"
        logger.info("Entering Method: %s" %methodName)
        #Fetch the username showing on the home page
        user = self.driver.find_element_by_name("login-user-name").text
        
        #Compare the user 
        self.assertEqual(user, expectedUser, "User not logged in successfully")
        logger.info("Exiting Method: %s" %methodName)
        
    def _verifyMainArticle(self):
        '''
        Method to validate the main article to be an image
        Returns-
        mainArticle: The element in the webpage showing main article
        actualTitle: The title of the article
        elementType: The type of the article(i.e image or video or unknown)
        '''
        methodName = "_verifyMainArticle"
        logger.info("Entering Method: %s" %methodName)
        
        #Validate whether on the Home Page
        self.driver.find_element_by_id("main-content")
        
        #Fetch the list of main featured story
        elements = self.driver.find_elements_by_xpath("//div[contains(@class,'main-featured-story')]")
        
        #Fetch the main article
        mainArticle = elements[0]
        
        #Fetch the main article Text Contents
        mainArticleText = str(elements[0].text)
        
        #Split the contents of the main article and fetch the lines
        mainArticleLines = mainArticleText.split("\n")
        actualTitle = ""
        elementType = ""
        for content in mainArticleLines:
            if (content.find(".jpg")!= -1):
                elementType = "image"
            elif (content.find("jpeg") != -1):
                elementType = "image"
            elif (content.find("Loaded")!= -1):
                elementType = "video"
            else:
                actualTitle = content
                break
        self.assertTrue(elementType in ["image","video"],"The article is neither image nor video")
        logger.info("Exiting Method: %s" %methodName)
        return mainArticle,actualTitle,elementType
    
    def _verifyNavigatedArticle(self,expectedTitle,expectedArticleType="image"):
        methodName = "_verifyNavigatedArticle"
        logger.info("Entering Method: %s" %methodName)
        
        #Get the title of article navigated to
        currentTitle = self.driver.find_element_by_xpath("//h1[@itemprop='headline']").text
        
        #Compare the expected and current article title
        self.assertEqual(expectedTitle, currentTitle, "The page got navigated to a different page")
        
        #Get the Current Article Type(on the navigated page)
        currentArticleType = self.driver.find_element_by_xpath("//div[@class='media-group fadecount0']").get_attribute("itemprop")
        
        #Compare the expected and current article type
        self.assertEqual(currentArticleType,expectedArticleType, "Element Type loaded is different from expected")
    
        logger.info("Exiting Method: %s" %methodName)
        
    def test_site(self):
        methodName = "test_site"
        logger.info("Entering Method: %s" %methodName)
        
        #Goto the Site URL
        self.driver.get(STRAITTIMES_URL)
        
        #Refresh driver to remove any unwanted Advertisement pop-ups
        self.driver.refresh()
        
        #Wait for sometime for page to be loaded
        time.sleep(2)
        
        #Login to the site
        self._login()
        
        #Verify the Logged In User
        self._verifyLoggedInUser()
        
        #Verify the main article[Image in this case]
        mainArticle, expectedTitle,expectedArticleType = self._verifyMainArticle()
        
        #Load the main article
        mainArticle.click()
        
        #Verify the navigated article
        self._verifyNavigatedArticle(expectedTitle,expectedArticleType)
        logger.info("Exiting Method: %s" %methodName)
        
if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SiteValidatorWeb)
    unittest.TextTestRunner().run(suite)