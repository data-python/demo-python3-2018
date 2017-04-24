import spynner
import glob

browser = spynner.Browser()
browser.show()

having_file_list = glob.glob('./htmls/*.html')
having_names_list = []
for f in having_file_list:
    having_names_list.append(f.split('./htmls/')[1].split('.html')[0])


all_hrefs_f = open('all_hrefs.txt','r')
base_url = 'http://www.phei.com.cn'

for line in all_hrefs_f.readlines():

    book_name = line.split('\t')[0].replace('/','_')
    book_part_url = line.split('\t')[1].rstrip()
    book_id = book_part_url.split('bookid=')[1]

    if book_name not in having_names_list:
        url = base_url + book_part_url
        browser.load(url, load_timeout=120, tries=3)
        html_f = open('./htmls/' + book_name + '_' = book_id + '.html', 'w')
        html_f.write(browser.html)
        html_f.close()
        print('saving:', book_name)
    else:
        print('existing!', book_name)

all_hrefs_f.close()
browser.close()            
