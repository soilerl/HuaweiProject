import requests
from bs4 import BeautifulSoup
from source.utils.StringKeyUtils import StringKeyUtils

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
            StringKeyUtils.STR_HEADER_USER_AGENT: StringKeyUtils.STR_HEADER_USER_AGENT_SET
        }
    #获取HTML内容，返回字符串
    def getHTML(self, url) ->str:
        try:
            r = requests.get(url, headers=self.header, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            print("爬取失败, Exception: ", e)
    #在html网页中提取ProjectID
    def analyzeProjectID(self, soup=BeautifulSoup) -> str:
        strTemp = []
        for span in soup.find_all('span', attrs=StringKeyUtils.DIC_ANALYZE_PROJECT_ID_ATTR):
            strTemp.append(span.string)
        if len(strTemp) == 1:
            #allStr格式为 Project ID: 3836952
            allStr = strTemp[0]
            projectID = allStr.split(":")[1].strip()
            return projectID

    #对外暴露的接口，获取projectID
    def getProjectID(self) -> str:
        htmlText = self.getHTML(self.url)
        soup = BeautifulSoup(htmlText, 'lxml')
        projectID = self.analyzeProjectID(soup)
        return projectID

    #对外暴露的接口，获取项目mergeRequest页数
    def getMergeRequestPages(self) -> int:
        getPagesUrl = self.url
        if getPagesUrl[-1] != "/":
            getPagesUrl = getPagesUrl + "/"
        getPagesUrl += "-/merge_requests?scope=all&state=all"
        htmlText = self.getHTML(getPagesUrl)
        pages = self.analyzePages(htmlText)
        return pages

    #从html页面中提取page数
    def analyzePages(self, htmlText='') -> int:
        soup = BeautifulSoup(htmlText, 'lxml')
        pageIndexList = []
        for li in soup.find_all("li", attrs={'class': 'js-pagination-page'}):
            pageIndexList.append(int(li.findChild().text))
        pageIndexList.sort(reverse=True)
        return pageIndexList[0]



# if __name__ == '__main__':
#     helper = GetInformationOfParameterHelper("https://gitlab.com/tezos/tezos")
#     # print(helper.getProjectID())
#     pages = helper.getMergeRequestPages()
