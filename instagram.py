from insagram_UserInfo import username,password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Instagram():
    def __init__(self,username,password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs',{'intl.accept_languages':'en,en_US'})    
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('chromedriver.exe',chrome_options=self.browserProfile)
    def signIn(self):
        self.browser.get("https://www.instagram.com")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input").send_keys(self.username)
        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input").send_keys(self.password)
        self.browser.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button/div").click()
        time.sleep(5)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button").click()
        time.sleep(2.5)
        self.browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        # self.browser.maximize_window()
    def getFollowers(self):
        self.browser.get(f"https://www.instagram.com/{self.username}")
        time.sleep(2)
        self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        time.sleep(2)
        dialog = self.browser.find_element_by_css_selector("div[role=dialog] ul")
        followerCount  = len(dialog.find_elements_by_css_selector("li"))
        print(f"first count: {followerCount}")
        action = webdriver.ActionChains(self.browser)
        while True:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            newCount = len(dialog.find_elements_by_css_selector("li"))
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            if followerCount != newCount:
                followerCount = newCount
                print(f"second count: {newCount}")
                time.sleep(1)
                pass
            else:
                break

        followers = dialog.find_elements_by_css_selector("li")
        follower_List = []
        for user in followers:
            link = user.find_element_by_css_selector("a").get_attribute("href")
            follower_List.append(link)
        with open("followers.txt",'w',encoding='UTF-8') as file:
            for item in follower_List:
                file.write(item+"\n")
    def followUser(self,username):
        self.browser.get("https://www.instagram.com/"+ username)
        time.sleep(2)
        followButton = self.browser.find_element_by_tag_name("button")
        if followButton.text != "Following":
            followButton.click()
            time.sleep(1.5)
        else:
            print("You are already following this account!")
    def unfollowUser(self,username):
        self.browser.get("https://www.instagram.com/"+ username)
        time.sleep(2)
        self.browser.find_element_by_css_selector(".glyphsSpriteFriend_Follow.u-__7").click()
        time.sleep(1.5)
        self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()

instagram = Instagram(username,password)
instagram.signIn()
instagram.getFollowers()
instagram.followUser("username") #enter username of the page to follow
instagram.unfollowUser("username") #enter username of the page to unfollow

