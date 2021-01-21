from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,WebDriverException
from selenium.webdriver.common.by import By
from threading import Thread,Lock
from random import choice
from colorama import init,Fore,Style
from os import name,system
from sys import stdout
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import json

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title:str):
        if name == 'posix':
            stdout.write(f"\x1b]2;{title}\x07")
        elif name in ('ce', 'nt', 'dos'):
            system(f'title {title}')
        else:
            stdout.write(f"\x1b]2;{title}\x07")

    def TitleUpdate(self):
        while True:
            self.SetTitle(f'[One Man Builds Follow Bot Selenium] ^| FOLLOWED / UNFOLLOWED: {self.success} ^| ALREADY FOLLOWED / UNFOLLOWED: {self.already} ^| RETRIES: {self.retries}')
            sleep(0.1)

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('[Data]/useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('[Data]/proxies.txt','r')
        if self.proxy_type == 1:
            return f'http://{choice(proxies_file)}'
        elif self.proxy_type == 2:
            return f'socks4://{choice(proxies_file)}'
        elif self.proxy_type == 3:
            return f'socks5://{choice(proxies_file)}'

    def ReadJson(self,filename,method):
        with open(filename,method) as f:
            return json.load(f)

    def ReadFile(self,filename,method):
        with open(filename,method,encoding='utf8') as f:
            content = [line.strip('\n') for line in f]
            return content

    def close_driver(self,method_name,driver):
        self.PrintText(Fore.WHITE,Fore.YELLOW,method_name,'CLOSING WEBDRIVER')
        driver.quit()
            
    def __init__(self):
        self.SetTitle('[One Man Builds Spotify Follow Bot Selenium]')
        self.clear()
        init(convert=True)
        self.lock = Lock()

        self.success = 0
        self.already = 0
        self.retries = 0
        
        self.title = Style.BRIGHT+Fore.GREEN+"""
                                  ╔══════════════════════════════════════════════════╗
                                    ╔═╗╔═╗╔═╗╔╦╗╦╔═╗╦ ╦  ╔═╗╔═╗╦  ╦  ╔═╗╦ ╦╔╗ ╔═╗╔╦╗
                                    ╚═╗╠═╝║ ║ ║ ║╠╣ ╚╦╝  ╠╣ ║ ║║  ║  ║ ║║║║╠╩╗║ ║ ║ 
                                    ╚═╝╩  ╚═╝ ╩ ╩╚   ╩   ╚  ╚═╝╩═╝╩═╝╚═╝╚╩╝╚═╝╚═╝ ╩ 
                                  ╚══════════════════════════════════════════════════╝         
                                          
                                                                                     
        """
        print(self.title)

        config = self.ReadJson('[Data]/configs.json','r')

        self.use_proxy = config['use_proxy']
        self.proxy_type = config['proxy_type']
        self.method = config['method']
        self.headless = config['headless']
        self.website_load_max_wait = config['website_load_max_wait']
        self.login_check_max_wait = config['login_check_max_wait']
        self.button_click_max_wait = config['button_click_max_wait']
        self.wait_after_follow_unfollow_click = config['wait_after_follow_unfollow_click']
        self.wait_before_start = config['wait_before_start']
        self.browser_amount = config['browser_amount']
        self.url = config['url']

        print('')

    def Login(self,email,password,driver):
        try:
            driver.get('https://accounts.spotify.com/en/login/')

            try:
                WebDriverWait(driver,self.website_load_max_wait).until(EC.visibility_of_element_located((By.ID,'login-username'))).send_keys(email)
                try:
                    WebDriverWait(driver,self.website_load_max_wait).until(EC.visibility_of_element_located((By.ID,'login-password'))).send_keys(password)
                    try:
                        WebDriverWait(driver,self.website_load_max_wait).until(EC.element_to_be_clickable((By.ID,'login-button'))).click()
                        try:
                            url_to_be_present = EC.url_contains('https://accounts.spotify.com/en/status')
                            WebDriverWait(driver, self.login_check_max_wait).until(url_to_be_present)
                            self.PrintText(Fore.WHITE,Fore.GREEN,'LOGGED IN WITH',f'{email}:{password}')
                            return True
                        except TimeoutException:
                            self.PrintText(Fore.WHITE,Fore.RED,'FAILED TO LOGIN WITH',f'{email}:{password}')
                            return False
                    except TimeoutException:
                        self.retries += 1
                        self.close_driver('CAN NOT PRESS LOGIN BUTTON',driver)
                        self.Login(email,password,driver)
                except TimeoutException:
                    self.retries += 1
                    self.close_driver('CAN NOT ENTER PASSWORD',driver)
                    self.Login(email,password,driver)
            except TimeoutException:
                self.retries += 1
                self.close_driver('CAN NOT ENTER USERNAME',driver)
                self.Login(email,password,driver)
        except WebDriverException:
            self.retries += 1
            self.close_driver('LOGIN',driver)
            self.Login(email,password,driver)
        finally:
            self.PrintText(Fore.WHITE,Fore.YELLOW,'LOGIN','PROCESS FINISHED')

    def Follow(self,email,password):
        try:
            options = Options()

            if self.headless == 1:
                options.add_argument('--headless')

            useragent = self.GetRandomUserAgent()

            options.add_argument(f'--user-agent={useragent}')
            options.add_argument('no-sandbox')
            options.add_argument('--log-level=3')
            options.add_argument('--lang=en')

            if self.use_proxy == 1:
                options.add_argument('--proxy-server=http://{0}'.format(self.GetRandomProxy()))

            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("window-size=1280,800")
            options.add_argument('--disable-blink-features=AutomationControlled')

            driver = webdriver.Chrome(options=options)

            if self.Login(email,password,driver) == True:
                driver.get(self.url)
                try:
                    WebDriverWait(driver,self.button_click_max_wait).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#onetrust-accept-btn-handler'))).click()
                    self.PrintText(Fore.WHITE,Fore.GREEN,'COOKIES','ACCEPTED')
                    if self.method == 1:
                        try:
                            follow_button_element = WebDriverWait(driver,self.button_click_max_wait).until(EC.element_to_be_clickable((By.CLASS_NAME,"ff6a86a966a265b5a51cf8e30c6c52f4-scss")))
                            if follow_button_element.text == 'FOLLOW':
                                follow_button_element.click()
                                if self.wait_after_follow_unfollow_click > 0:
                                    sleep(self.wait_after_follow_unfollow_click)
                                self.success += 1
                                self.PrintText(Fore.WHITE,Fore.GREEN,'FOLLOWED',f'{email}:{password}')
                            else:
                                self.already += 1
                                self.PrintText(Fore.WHITE,Fore.RED,'FOLLOWING',f'{email}:{password}')
                        except TimeoutException:
                            self.retries += 1
                            self.close_driver('CANNOT CLICK FOLLOW BUTTON',driver)
                            self.Follow(email,password)
                    else:
                        try:
                            unfollow_button_element = WebDriverWait(driver,self.button_click_max_wait).until(EC.element_to_be_clickable((By.CLASS_NAME,'ff6a86a966a265b5a51cf8e30c6c52f4-scss')))
                            if unfollow_button_element.text == 'FOLLOWING':
                                unfollow_button_element.click()
                                if self.wait_after_follow_unfollow_click > 0:
                                    sleep(self.wait_after_follow_unfollow_click)
                                self.success += 1
                                self.PrintText(Fore.WHITE,Fore.GREEN,'UNFOLLOWED',f'{email}:{password}')
                            else:
                                self.already += 1
                                self.PrintText(Fore.WHITE,Fore.RED,'NOT FOLLOWING',f'{email}:{password}')
                        except TimeoutException:
                            self.retries += 1
                            self.close_driver('CANNOT CLICK UNFOLLOW BUTTON',driver)
                            self.Follow(email,password)
                except TimeoutException:
                    self.retries += 1
                    self.close_driver('CANNOT ACCEPT COOKIES',driver)
                    self.Follow(email,password)
        except WebDriverException:
            self.retries += 1
            self.close_driver('FOLLOW / UNFOLLOW',driver)
            self.Follow(email,password)
        finally:
            self.close_driver('FOLLOW / UNFOLLOW PROCESS FINISHED',driver)

    def Start(self):
        Thread(target=self.TitleUpdate).start()
        combos = self.ReadFile('[Data]/combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.browser_amount) as ex:
            for combo in combos:
                email = combo.split(':')[0]
                password = combo.split(':')[-1]
                ex.submit(self.Follow,email,password)
                if self.wait_before_start > 0:
                    sleep(self.wait_before_start)
if __name__ == "__main__":
    main = Main()
    main.Start()