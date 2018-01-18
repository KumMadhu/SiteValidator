'''
Created on Jan 18, 2018

@author: madhu
'''
import unittest
from appium import webdriver
import logging
import sys

logger = logging.getLogger('siteValidator')
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))

USERNAME = "kmadhu3042008@gmail.com"
PASSWORD = "Asimil91"
STRAITTIMES_URL = "http://www.straitstimes.com/"
class SiteValidationMobile(unittest.TestCase):
    "Class to run tests to Validate the Site"
    
    def setUp(self):
        "Setup for the test"
        methodName = "setUp"
        logger.info("Entering Method: %s" %methodName)
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1.1'
        desired_caps['deviceName'] = 'Nexus_4_API_22_-_TestSiteValidator'
        desired_caps['browserName'] = 'Browser'
        desired_caps['nativeWebTap'] = True
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        logger.info("Exiting Method: %s" %methodName)
    
    def tearDown(self):
        "Tear down the test"
        methodName = "tearDown"
        logger.info("Entering Method: %s" %methodName)
        
        self.driver.quit()
        logger.info("Exiting Method: %s" %methodName)
    
    def _login(self, username=USERNAME, password= PASSWORD):
        '''
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
        
        logger.info("Exiting Method: %s" %methodName)
    
    def _verifyLoggedInUser(self,expectedUser = USERNAME):
        '''
        expectedUser: Refers to UserId expected to be shown on home page(as logged in user)
        '''
        methodName = "_verifyLoggedInUser"
        logger.info("Entering Method: %s" %methodName)
        
        #Fetch the username showing on the home page
        user = self.driver.find_element_by_xpath("//a[@name='login-user-name']").text  
        if user == "":
            self.driver.find_element_by_xpath("//a[text()='%s']" %USERNAME)
        else:
            #Compare the user
            self.assertEqual(user, expectedUser, "User not logged in successfully")

        logger.info("Exiting Method: %s" %methodName)
        
    def _verifyMainArticle(self):
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
            #Fetch the type of element based on contents of first file
            if (content.find(".jpg")!= -1):
                elementType = "image"
            elif (content.find("jpeg") != -1):
                elementType = "image"
            elif (content.find("Loaded")!= -1):
                elementType = "video"
            elif (content.find("Progress") != -1):
                elementType = "video"
            else:
                #Fetch the title of the main article(usually first line after image name
                actualTitle = content
                break
        
        #Validate the element type is image or video
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
        
    def test_get(self):
        "Test the Single Player mode launches correctly"
        methodName = "test_get"
        logger.info("Entering Method: %s" %methodName)

        #Goto the Site URL
        self.driver.get(STRAITTIMES_URL)
        
        #Refresh driver to remove any unwanted Advertisement pop-ups
        self.driver.refresh()
        
        #Wait for sometime for page to be loaded
        #time.sleep(2)
        self.assertEqual('The Straits Times - Breaking news, Singapore news, Asia and world news & multimedia',self.driver.title)
        
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
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(SiteValidationMobile)
    unittest.TextTestRunner().run(suite)