import urllib
import urllib.parse
import urllib.request
import struct
import re

def getHtml(url):
        site= url
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        req = urllib.request.Request(site, headers=hdr)
        page = urllib.request.urlopen(req)
        content = page.read()
        unicode = content.decode("utf-8")
        #print (unicode)
        return (unicode)

def getDictionary(html):
        #获取当前成语信息
        print ("获取当前成语信息")
        regDicInfo = '<strong>(.*?)</strong>'
        dicName = re.compile(regDicInfo, re.M).findall(html);
        print (dicName)
        #获取拼音
        print ("获取当前成语拼音")
        regDicInfo = '<b>\[(.*?)\]</b>'
        dicPinyin = re.compile(regDicInfo, re.M).findall(html);
        print (dicPinyin)
        #获取成语接龙列表
        regDicInfo = 'idiom">(.*?)</a>'
        jielongList = re.compile(regDicInfo, re.M).findall(html);
        #print (jielongList)
        return (dicName, dicPinyin, jielongList)
      
def writeFile(id, name, pinyin):
    file = open("chengyu.txt",'a')
    text = "ID:" + str(id) + ", name :" + name + ", pinyin:" + pinyin + "\n"
    file.write(text)
    file.close()
    
def getDic(url, level, dictList, size):
        max_level = 20
        if (level > max_level):
                return;
        level = level + 1
        
        html = getHtml(url)
        (name, pinyin, jielongList) = getDictionary(html)
        if len(name) == 0:
                print(url)
                return
        dictList[name[0]] = pinyin[0]
        size = size + 1
        print(size)
        #写进文件
        writeFile(size, name[0], pinyin[0])
        
        if (level > max_level):
                return;
        
        for dic in jielongList:
                if dic in dictList:
                        print("已经存在")
                        continue  
                print(dic)
                #拼接url
                dic = urllib.request.quote(dic.encode('utf-8', 'replace'))
                newUrl = 'http://hanyu.baidu.com/zici/s?wd='+ dic +'&cf=jielong&ptype=idiom'
                newlevel = level
                getDic(newUrl, newlevel, dictList, size)
                size = size + 1

          
#开始
initUrl = 'http://hanyu.baidu.com/zici/s?wd=%E9%80%8F%E9%AA%A8%E9%85%B8%E5%BF%83&cf=jielong&ptype=idiom'                
level = 0
size = 0
dictList = {}
getDic(initUrl, level, dictList, size)
