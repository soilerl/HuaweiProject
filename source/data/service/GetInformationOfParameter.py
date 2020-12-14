import requests
from bs4 import BeautifulSoup

"""爬虫爬取一些参数"""


class GetInformationOfParameterHelper:
    url = None
    project_id = None
    header = {}

    def __init__(self, url):
        self.url = url
        self.initHeader()

    #初始化头
    def initHeader(self):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
    #获取HTML内容，返回字符串
    def getHTML(self) ->str:
        try:
            r = requests.get(self.url, headers=self.header, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            print("爬取失败")
    #在html网页中提取ProjectID
    def analyzeProjectID(self, soup=BeautifulSoup) -> str:
        strTemp = []
        for span in soup.find_all('span', attrs={'data-qa-selector':'project_id_content'}):
            strTemp.append(span.string)
        if len(strTemp) == 1:
            #allStr格式为 Project ID: 3836952
            allStr = strTemp[0]
            projectID = allStr.split(":")[1].strip()
            return projectID

    #对外暴露的接口，获取projectID
    def getProjectID(self) -> str:
        htmlText = helper.getHTML()
        soup = BeautifulSoup(htmlText, 'lxml')
        projectID = self.analyzeProjectID(soup)
        return projectID

if __name__ == '__main__':
    helper = GetInformationOfParameterHelper("https://gitlab.com/tezos/tezos")
    print(helpe r.getProjectID())

