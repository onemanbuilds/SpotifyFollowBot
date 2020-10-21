from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from concurrent.futures import ThreadPoolExecutor
from colorama import init,Fore
import os

class Main:
    def clear(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        os.system("title {0}".format(title_name))

    def __init__(self):
        self.clear()
        self.SetTitle('One Man Builds Spotify FollowBot Selenium')
        init(convert=True)
        title = Fore.YELLOW+"""
                                    
                            ____ ___  ____ ___ _ ____ _   _    ____ ____ _    _    ____ _ _ _ 
                            [__  |__] |  |  |  | |___  \_/     |___ |  | |    |    |  | | | | 
                            ___] |    |__|  |  | |      |      |    |__| |___ |___ |__| |_|_| 
                                                                                            
                                    
        """
        print(title)
        self.follow_option = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] [1]Follow [0]Unfollow: '))
        self.browser_amount = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many browser would you like to run at the same time: '))
        self.headless = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to use headless mode [1]yes [0]no: '))
        self.waiting_time = float(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many seconds would you like to wait between follows: '))
        self.url = str(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Enter the profile url: '))
        print('')

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def Login(self,username,password,driver:webdriver):
        logged_in = False
        driver.get('https://accounts.spotify.com/en/login/')
        username_elem = driver.find_element_by_id('login-username')
        username_elem.send_keys(username)
        password_elem = driver.find_element_by_id('login-password')
        password_elem.send_keys(password)
        login_button_elem = driver.find_element_by_id('login-button')
        login_button_elem.click()
        sleep(1)

        if driver.current_url == 'https://accounts.spotify.com/en/status':
            print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] LOGGED IN WITH | {0}:{1}'.format(username,password))
            logged_in = True
        else:
            print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] FAILED TO LOGIN WITH | {0}:{1}'.format(username,password))
            logged_in = False

        return logged_in

    def ClickFollowButton(self,driver,combos):
        try:
            button_values = driver.execute_script("return document.getElementsByClassName('ff6a86a966a265b5a51cf8e30c6c52f4-scss');")
            if button_values[0].text.lower() == 'follow':
                driver.execute_script("document.getElementsByClassName('ff6a86a966a265b5a51cf8e30c6c52f4-scss')[0].click();")
                print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] FOLLOWED WITH | {0}'.format(combos))
                with open('followed.txt','a',encoding='utf8') as f:
                    f.write('FOLLOWED WITH | {0}\n'.format(combos))
            elif button_values[0].text.lower() == 'following':
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] ALREADY FOLLOWING WITH | {0}'.format(combos))
                with open('already_following.txt','a',encoding='utf8') as f:
                    f.write('ALREADY FOLLOWING WITH | {0}\n'.format(combos))
            else:
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] SOMETHING WENT WRONG')
        except:
            self.ClickFollowButton(driver,combos)

    def ClickFollowingButton(self,driver,combos):
        try:
            button_values = driver.execute_script("return document.getElementsByClassName('ff6a86a966a265b5a51cf8e30c6c52f4-scss');")
            if button_values[0].text.lower() == 'following':
                driver.execute_script("document.getElementsByClassName('ff6a86a966a265b5a51cf8e30c6c52f4-scss')[0].click();")
                print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] UNFOLLOWED WITH | {0}'.format(combos))
                with open('unfollowed.txt','a',encoding='utf8') as f:
                    f.write('UNFOLLOWED WITH | {0}\n'.format(combos))
            elif button_values[0].text.lower() == 'follow':
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] NOT FOLLOWING WITH | {0}'.format(combos))
                with open('not_following.txt','a',encoding='utf8') as f:
                    f.write('NOT FOLLOWING WITH | {0}\n'.format(combos))
            else:
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] SOMETHING WENT WRONG')
        except:
            self.ClickFollowingButton(driver,combos)

    def Follow(self,combos):
        try:
            username = combos.split(':')[0].replace("['","")
            password = combos.split(':')[-1].replace("]'","")
            options = Options()

            if self.headless == 1:
                options.add_argument('--headless')
            
            options.add_argument('no-sandbox')
            options.add_argument('--log-level=3')
            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            driver = webdriver.Chrome(options=options)

            if self.Login(username,password,driver) == True:
                driver.get(self.url)
                sleep(self.waiting_time)
                if self.follow_option == 1:
                    self.ClickFollowButton(driver,combos)
                else:
                    self.ClickFollowingButton(driver,combos)
                sleep(self.waiting_time)
        except:
            self.Follow(combos)
        finally:
            driver.quit()

    def Start(self):
        combos = self.ReadFile('combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.browser_amount) as ex:
            for combo in combos:
                ex.submit(self.Follow,combo)
        
if __name__ == '__main__':
    main = Main()
    main.Start()