#encoding=utf8

import requests
import json
from bs4 import BeautifulSoup
import webbrowser
from wox import Wox,WoxAPI

USERTOKEN = 'Daisy:441938E072997B0A3108'
class Pinboard(Wox):

    def request(self,url):
        #If user set the proxy, you should handle it.
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
            "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
            "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
            return requests.get(url,proxies = proxies)
        else:
            return requests.get(url)

    def query(self,key):
        if not USERTOKEN:
            result = {
                "Title": "Please fill in your token in pinboard plugin settings", 
                "SubTitle": "You can find the token under pinboard settings tab",
                "IcoPath":"icon.png"
            }
            return [result]

        url = 'https://api.pinboard.in/v1/posts/get'
        params = {'auth_token':USERTOKEN, 'url':key, 'meta':'yes'}
        r = requests.get(url, params)
        data = json.loads(r.content.decode('utf-8').replace("'", '"'))
        posts = data['posts']

        bs = BeautifulSoup(r.text)
        results = []
        
        for post in posts:
            title = post['description']
            subtitle = post['time']
            url = post['href']

            result = {
                'Title': title,
                'subTitle': subtitle,
                'IconPath': 'icon.png', 
                'JsonRPCAction':{
                    'method':'openUrl',
                    'parameters':[url],
                    'dontHideAfterAction':True
                }
            }

            results.append(result)

        return results

    def openUrl(self,url):
        webbrowser.open(url)
        #todo:doesn't work when move this line up
        WoxAPI.change_query(url)

if __name__ == "__main__":
    Pinboard()