import requests

# 抓取网页text返回
def get_content(url):
    resp = requests.get(url)
    return resp.text

if __name__ == '__main__':

    url = "http://www.baidu.com"
    content = get_content(url)
    # print(content[0:50])
    print(content)  # 输出网页
    print(len(content))  # 2381

    f1 = open("page1.html","w",encoding="utf-8")
    f1.write(content)
    f1.close()

    f2 = open("page1.html", "r", encoding="utf-8")
    content_read = f2.read()
    print(content_read[0:50])

    # 第2种文件读取方式
    with open("page2.html", "w", encoding="utf-8") as f3:
        f3.write(content)
    with open("page2.html", "r", encoding="utf-8") as f4:
        content_read2 = f4.read()
        print(content_read2[0:100])




