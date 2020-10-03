from bs4 import BeautifulSoup
import re
# with open('data.html', 'r', encoding='utf-8') as f:
#     bs = BeautifulSoup(f.read(), 'html5lib')
#     div_lst = bs.find_all('div', attrs={'style': 'width: 730px;'
#                                                 'float:left;'
#                                                 'display:inline;'
#                                                 'margin-top:20px;'
#                                                 'margin-left:20px;'
#                                                 'border-bottom:dotted 1px #878787;'
#                                                 'padding-bottom:20px;'})
#
#     for div in div_lst:
#         a_lst = div.find_all('a')
#         for a in a_lst:
#             print(a.text.strip(), a['href'])


with open('data.html', 'r', encoding='utf-8') as f:
    bs = BeautifulSoup(f.read(),'html5lib')
    div_lst = bs.find_all('div', attrs={'style': re.compile('width:730px.*')})

    for div in div_lst:
        a_lst = div.find_all('a')
        for a in a_lst:
            if a.text != "":
                print(a.text.strip(), a['href'])
