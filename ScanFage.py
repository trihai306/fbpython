import json
from random import randint
import random
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
from base import TIMEOUT, BasePage

class searchMbasic():

    def ScanFage(self,stringCookie,token,KeyWords,MaxScan,Stop_keyword,SleepFrom,SleepTo):
        results = []
        response = ""
        cookie_str = stringCookie       
        for keyword in KeyWords:
            response = searchMbasic.search_one(self,cookie_str,keyword)
            if len(results) > MaxScan:break
            for i in range(Stop_keyword):
                if len(results) > MaxScan:break
                sleep(randint(SleepFrom,SleepTo))
                response = searchMbasic.search_see_more(self,cookie_str,response)
                results.append(searchMbasic.Get_Name_Uid_Fage(self,cookie_str,response,token))


        return results
    
    def search_one(self,cookie_str,keyword):
        url_search = f"https://mbasic.facebook.com/search/?refid=7&search=Search&search_source=top_nav&query={keyword}"
        cookies = {}
        for cookie in cookie_str.split('; '):
            name, value = cookie.split('=', 1)
            cookies[name] = value
        response = requests.get(url_search, cookies=cookies).text
        return response
    
    def search_see_more(self,cookie_str,response):
        cookies = {}
        for cookie in cookie_str.split('; '):
            name, value = cookie.split('=', 1)
            cookies[name] = value
        see_more = re.search(r'keywords_pages\?f=(.*?)"', response)
        if see_more:
            #print(see_more.group(1))
            print("click input see more")
            url_see_more = "https://mbasic.facebook.com/graphsearch/str/abc/keywords_pages?f="+see_more.group(1)
        response = requests.get(url_see_more, cookies=cookies).content.decode('utf-8')#
        return response


    def Get_Name_Uid_Fage(self,cookie_str,response,token):
        matches = re.findall(r'<div class="ci">(.+?)<.+?id=(\d+)', response)
        results = []
        for match in matches:
            uid = match[1]
            results.append(searchMbasic.Get_Info_Fage(self,cookie_str,uid,token))
        return results
    

    def Get_Info_Fage(self,cookie_str,uid,token):
        cookies = {}
        for cookie in cookie_str.split('; '):
            name, value = cookie.split('=', 1)
            cookies[name] = value
        time.sleep(5)
        url= f"https://graph.facebook.com/v16.0/{uid}?fields=id%2Cname%2Cphone%2Clink%2Cemails%2Cartists_we_like%2Ccountry_page_likes%2Cnew_like_count%2Cfan_count&access_token={token}"
        response = requests.get(url, cookies=cookies).content.decode('utf-8')#
        res = json.loads(response)
        print(res)
        return res
    