from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from threading import Thread,Lock
from random import choice
from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from concurrent.futures import ThreadPoolExecutor
from time import sleep

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def TitleUpdate(self):
        while True:
            self.SetTitle('One Man Builds Follow Bot Selenium ^| FOLLOWED / UNFOLLOWED: {0} ^| ALREADY FOLLOWED / UNFOLLOWED: {1} ^| RETRIES: {2}'.format(self.success,self.already,self.retries))
            sleep(0.1)

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        return choice(proxies_file)

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def Login(self,username,password,driver):
        try:
            logged_in = False

            driver.get('https://accounts.spotify.com/en/login/')
            login_username_present = EC.presence_of_element_located((By.ID, 'login-username'))
            WebDriverWait(driver, self.website_load_max_wait).until(login_username_present)

            username_elem = driver.find_element_by_id('login-username').send_keys(username)
            password_elem = driver.find_element_by_id('login-password').send_keys(password)
            login_button_elem = driver.find_element_by_id('login-button').click()

            try:
                url_to_be_present = EC.url_to_be('https://accounts.spotify.com/en/status')
                WebDriverWait(driver, self.login_check_max_wait).until(url_to_be_present)
                self.PrintText(Fore.CYAN,Fore.RED,'LOGIN',f'LOGGED IN WITH | {username}:{password}')
                logged_in = True
            except TimeoutException:
                self.PrintText(Fore.RED,Fore.CYAN,'LOGIN',f'FAILED TO LOGIN WITH | {username}:{password}')
                logged_in = False
        
            return logged_in
        except:
            driver.quit()
            self.Login(username,password,driver)
        #finally:
        #    driver.quit()

    def Follow(self,username,password):
        try:
            options = Options()

            #if self.headless == 1:
            #    options.add_argument('--headless')

            #options.add_argument(f'--user-agent={self.GetRandomUserAgent()}')
            options.add_argument('no-sandbox')
            options.add_argument('--log-level=3')
            options.add_argument('--lang=en')

            if self.use_proxy == 1:
                options.add_argument('--proxy-server=http://{0}'.format(self.GetRandomProxy()))

            #Removes navigator.webdriver flag
            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            
            # For older ChromeDriver under version 79.0.3945.16
            options.add_experimental_option('useAutomationExtension', False)

            options.add_argument("window-size=1280,800")

            #For ChromeDriver version 79.0.3945.16 or over
            options.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(options=options)

            if self.Login(username,password,driver) == True:
                driver.get(self.url)
                try:
                    follow_button_clickable = EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div/div[3]/div/button[1]'))
                    WebDriverWait(driver, self.max_wait).until(follow_button_clickable)
                    follow_button_element = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div/div[3]/div/button[1]')
                    if follow_button_element.text == 'FOLLOW':
                        follow_button_element.click()
                        if self.wait_after_follow_unfollow_click > 0:
                            sleep(self.wait_after_follow_unfollow_click)
                        self.PrintText(Fore.CYAN,Fore.RED,'FOLLOWED',f'{username}:{password}')
                        self.success += 1
                    else:
                        self.PrintText(Fore.CYAN,Fore.RED,'FOLLOWING',f'{username}:{password}')
                        self.already += 1
                except TimeoutException:
                    self.PrintText(Fore.RED,Fore.CYAN,'ERROR','FOLLOW BUTTON NOT CLICKABLE')
        except:
            driver.quit()
            self.retries += 1
            self.Follow(username,password)
        finally:
            driver.quit()

    def UnFollow(self,username,password):
        
        try:
            options = Options()

            #if self.headless == 1:
            #    options.add_argument('--headless')

            options.add_argument(f'--user-agent={self.GetRandomUserAgent()}')
            options.add_argument('no-sandbox')
            options.add_argument('--log-level=3')
            options.add_argument('--lang=en')

            if self.use_proxy == 1:
                options.add_argument('--proxy-server=http://{0}'.format(self.GetRandomProxy()))

            #Removes navigator.webdriver flag
            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            
            # For older ChromeDriver under version 79.0.3945.16
            options.add_experimental_option('useAutomationExtension', False)

            options.add_argument("window-size=1280,800")

            #For ChromeDriver version 79.0.3945.16 or over
            options.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(options=options)

            if self.Login(username,password,driver) == True:
                driver.get(self.url)
                try:
                    follow_button_clickable = EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div/div[3]/div/button[1]'))
                    WebDriverWait(driver, self.max_wait).until(follow_button_clickable)
                    follow_button_element = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div/div[3]/div/button[1]')
                    if follow_button_element.text == 'FOLLOWING':
                        follow_button_element.click()
                        if self.wait_after_follow_unfollow_click > 0:
                            sleep(self.wait_after_follow_unfollow_click)
                        self.PrintText(Fore.CYAN,Fore.RED,'UNFOLLOWED',f'{username}:{password}')
                        self.success += 1
                    else:
                        self.PrintText(Fore.CYAN,Fore.RED,'NOT FOLLOWING',f'{username}:{password}')
                        self.already += 1
                except TimeoutException:
                    self.PrintText(Fore.RED,Fore.CYAN,'ERROR','UNFOLLOW BUTTON NOT CLICKABLE')
        except:
            driver.quit()
            self.retries += 1
            self.UnFollow(username,password)
        finally:
            driver.quit()
            

    def __init__(self):
        init(convert=True)
        self.lock = Lock()

        self.success = 0
        self.already = 0
        self.retries = 0

        self.clear()
        self.SetTitle('One Man Builds Spotify Follow Bot Selenium')
        self.title = Style.BRIGHT+Fore.RED+"""
                                  ╔══════════════════════════════════════════════════╗
                                    ╔═╗╔═╗╔═╗╔╦╗╦╔═╗╦ ╦  ╔═╗╔═╗╦  ╦  ╔═╗╦ ╦╔╗ ╔═╗╔╦╗
                                    ╚═╗╠═╝║ ║ ║ ║╠╣ ╚╦╝  ╠╣ ║ ║║  ║  ║ ║║║║╠╩╗║ ║ ║ 
                                    ╚═╝╩  ╚═╝ ╩ ╩╚   ╩   ╚  ╚═╝╩═╝╩═╝╚═╝╚╩╝╚═╝╚═╝ ╩ 
                                  ╚══════════════════════════════════════════════════╝         
                                          
                                                                                     
        """
        print(self.title)
        self.method = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Follow ['+Fore.RED+'0'+Fore.CYAN+']Unfollow: '))
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        self.browser_amount = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Threads: '))
        self.max_wait = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Max Wait For Url To Load (seconds): '))
        self.website_load_max_wait = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Website Load Max Wait (seconds): '))
        self.login_check_max_wait = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Login Check Max Wait (seconds): '))
        self.wait_after_follow_unfollow_click = float(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Wait After Follow / Unfollow Button Click: '))
        self.wait_before_start = float(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Wait Before Start (seconds): '))
        self.url = str(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Profile url: '))
        print('')

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        combos = self.ReadFile('combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.browser_amount) as ex:
            if self.method == 1:
                for combo in combos:
                    username = combo.split(':')[0]
                    password = combo.split(':')[-1]
                    ex.submit(self.Follow,username,password)
                    if self.wait_before_start > 0:
                        sleep(self.wait_before_start)
            else:
                for combo in combos:
                    username = combo.split(':')[0]
                    password = combo.split(':')[-1]
                    ex.submit(self.UnFollow,username,password)
                    if self.wait_before_start > 0:
                        sleep(self.wait_before_start)

if __name__ == "__main__":
    main = Main()
    main.Start()