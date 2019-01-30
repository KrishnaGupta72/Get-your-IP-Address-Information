#requests module will allow you to send HTTP/1.1 requests using Python. With it, you can add content like headers, form data, multipart files, and parameters via simple Python libraries. It also allows you to access the response data of Python in the same way
import requests
#csv module implements classes to read and write tabular data in CSV format
import csv
#lxml provides a very simple and powerful API for parsing XML and HTML documents very quickly.
from lxml import html
#itertools functions creates iterators for efficient looping,here it is used for zip()
import itertools
import time

http_proxy = "your proxy:port number"
https_proxy = "your proxy:port number"
proxies = {'http': http_proxy, 'https': https_proxy}

#User defined function for extracting a portion of string from a given string.
def get_str(resp_str,frm_str,to_str):
    start_index = resp_str.find(frm_str) + len(frm_str)
    end_index = resp_str.find(to_str, start_index)
    resp_dict = resp_str[start_index:end_index]
    return resp_dict

# ##############Hitting Printer Category page #######################
Printer_page_url = "https://www.amazon.com/s/ref=lp_16225007011_nr_n_8?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A172635&bbn=16225007011&ie=UTF8&qid=1547624107&rnid=16225007011"

Printer_page_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Host": "www.amazon.com",
    "Accept-Language": "en-US,en;q=0.9",
}

#Sending HTTP request and getting response.
Printer_page_url_resp = requests.get(Printer_page_url,proxies=proxies,headers=Printer_page_headers)
#print(len(Printer_page_url_resp))

#Writing a Printer List Page response in a file
with open("Printer_page.html", 'w', encoding='utf-8') as file:
    file.write(Printer_page_url_resp.text)

##Opening a Printer List page response in a file
with open("Printer_page.html", "r", encoding='utf-8') as f:
    text = f.read()

#Parsing parsing HTML document
tree = html.fromstring(text)
#Fetching total available products on a single page using xpath
prod_per_page_cnt = tree.xpath('//span[@id="s-result-count"]/text()')[0]
prod_per_page_cnt = get_str(prod_per_page_cnt,'1-',' of')
#print(prod_per_page_cnt)

#Fetching total number od list Pages available for Printers using xpath
Tot_list_page_cnt = get_str(prod_per_page_cnt,'of ',' result')
#print(Tot_list_page_cnt)

#If total number od list Pages are not showing than Fetching Total list pages count directly
if Tot_list_page_cnt=='' or Tot_list_page_cnt == None:
    Tot_list_page_cnt = tree.xpath('//div[@id="pagn"]/span[@class="pagnDisabled"]/text()')[0]
    # print(Tot_list_page_cnt)

#Fetching 2nd list page url from the 1st page
prod_2nd_page_url = tree.xpath('//div[@class="pagnHy"]/span/a/@href')[0]
#print(prod_2nd_page_url)

#Capturing all 24 products from first list page
count_4_header=1
total_prod_cnt=0
Fisrt_pg_prod_cut=[]
for prod_no in range(0,int(prod_per_page_cnt)):
    #Cut each product section data and stored into a list named "Fisrt_pg_prod_cut" from the 1st list page.
    Fisrt_pg_prod_cut.append(get_str(text, 'id="result_' + str(prod_no), ' id="result_' + str(prod_no+1)))
    total_prod_cnt+=1
    # with open("Prod_1-" + str(prod_no) + ".html", 'w', encoding='utf-8') as file:
    #     file.write(Fisrt_pg_prod_cut[prod_no])

    #Now parsing Product(Printer) information from the 1st product section cut
    tree = html.fromstring(Fisrt_pg_prod_cut[prod_no])

    Prod_name = tree.xpath('//a/h2[@class="a-size-base s-inline  s-access-title  a-text-normal"]/text()')
    #print(Prod_name)
    Brand_name = tree.xpath('//*[@class="s-item-container"]/div[3]//span[2]/text()')
    #print(Brand_name)

    P_price=[]
    Prod_fraction_price=[]
    Prod_whole_price = tree.xpath('//span[@class ="sx-price sx-price-large"]/span[@class ="sx-price-whole"]/text()')
    if len(Prod_whole_price)==0:
        Prod_whole_price = tree.xpath('//span[@class="a-size-base a-color-base"]/text()')
        P_price=Prod_whole_price
    else:
        Prod_fraction_price=tree.xpath('//span[@class="sx-price sx-price-large"]/sup[@class="sx-price-fractional"]/text()')
        price = '$' + Prod_whole_price[0] + '.' + Prod_fraction_price[0]
        P_price.append(price)

    List_price = tree.xpath('//span[@class="a-size-base-plus a-color-secondary a-text-strike"]/text()')
    #print(List_price)
    Star_Rat = tree.xpath('//a[@class="a-popover-trigger a-declarative"]//span[@class="a-icon-alt"]/text()')

    Prod_Star_Rat=[]
    for prod in Star_Rat:
        Prod_Star_Rat.append(get_str(prod,'',' out'))
    #print(Prod_Star_Rat)
    Prod_Review = tree.xpath('//div[@class="s-item-container"]/div[6]/a/text()')
    #print(Prod_Review)
    #Capturing remaining Prod_Review which were not captured earlier
    if len(Prod_Review)==0:
        Prod_Review = tree.xpath('//div[@class ="s-item-container"]/div[5]/a/text()')

    Prod_Url = tree.xpath('//div/a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href')
    #print(Prod_Url)

    #Writing all product(Printer) information into a csv file.
    with open("AmazonPrinterData.csv", "a", newline='') as file:
        # Defines column names into a csv file.
        field_names = ['Prod_name', 'Brand_name', 'Prod_price', 'Cross_price', 'Prod_Star_Rat', 'Prod_Review', 'Prod_Url']
        writer = csv.DictWriter(file, fieldnames=field_names)
        # Condition for writing header only once.

        if count_4_header == 1:
            writer.writeheader()
        count_4_header = count_4_header + 1
        for (Prod_name_val, Brand_name_val, P_price_val, List_price_val, Prod_Star_Rat_val, Prod_Review_val, Prod_Url_val) in itertools.zip_longest(Prod_name, Brand_name, P_price, List_price, Prod_Star_Rat, Prod_Review, Prod_Url):

            # Writing all information in a row.
            writer.writerow(
                {
                    'Prod_name': Prod_name_val,
                    'Brand_name': Brand_name_val,
                    'Prod_price': P_price_val,
                    'Cross_price': List_price_val,
                    'Prod_Star_Rat': Prod_Star_Rat_val,
                    'Prod_Review': Prod_Review_val,
                    'Prod_Url': Prod_Url_val
                }
            )

###############Hitting from 2nd list page and next...#######################

Printer_listpage_link=''

for listpg in range(2,(Tot_list_page_cnt+1)):

    if listpg==2:
        #Making 2nd list pages url dynamic
        Printer_listpage_url = "https://www.amazon.com" + prod_2nd_page_url
    else:
        # Making 3rd and next list pages urls dynamic
        Printer_listpage_url="https://www.amazon.com" + Printer_listpage_link

    #print(Printer_listpage_url)

    Printer_listpage_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        "Host": "www.amazon.com",
        #"Referer": "https://www.myntra.com/shop/men",
        #"Connection": "keep-alive",
        "Accept-Language": "en-US,en;q=0.9",
    }

    time.sleep(2)
    #Sending HTTP request and getting response.
    prod_2nd_page_url_resp = requests.get(Printer_listpage_url ,proxies=proxies,headers=Printer_listpage_headers)

    ##Write 2nd List page response in a file
    with open("Printer_listpage" + str(listpg) + ".html", 'w', encoding='utf-8') as file:
        file.write(prod_2nd_page_url_resp.text)

    ##Open 2nd page response in a file
    with open("Printer_listpage" + str(listpg) + ".html", "r", encoding='utf-8') as f:
        text = f.read()

    # Parsing parsing HTML document from 2nd List pages and next...
    tree = html.fromstring(text)

    prod_listpage_url = tree.xpath('//div[@class="pagnHy"]/span[{0}]/a/@href'.format(listpg+2))
    #print(prod_listpage_url)
    if prod_listpage_url:
        Printer_listpage_link = prod_listpage_url[0]
        #print(Printer_listpage_link)
    ##############Hitting from page 2 and next#######################

    prod_res=0
    for prod_cnt in range(total_prod_cnt,int(prod_per_page_cnt*listpg)):

        if prod_res==24:
            #total_prod_cnt += 1
            prod_res=0
            break
        Fisrt_pg_prod_cut.append(get_str(text, 'id="result_' + str(prod_cnt), ' id="result_' + str(prod_cnt+1)))
        # print(len(Fisrt_pg_prod_cut))
        with open("Prod_" + str(listpg) + "-" + str(prod_cnt) + ".html", 'w', encoding='utf-8') as file:
            file.write(Fisrt_pg_prod_cut[prod_cnt])

        total_prod_cnt+=1
        prod_res=prod_res+1
        #print(len(prod_sec_cut))
        tree = html.fromstring(Fisrt_pg_prod_cut[prod_cnt])

        Prod_name = tree.xpath('//a/h2[@class="a-size-base s-inline  s-access-title  a-text-normal"]/text()')
        #print(Prod_name)
        Brand_name = tree.xpath('//*[@class="s-item-container"]/div[3]//span[2]/text()')
        #print(Brand_name)

        P_price=[]
        Prod_fraction_price=[]
        Prod_whole_price = tree.xpath('//span[@class ="sx-price sx-price-large"]/span[@class ="sx-price-whole"]/text()')
        if len(Prod_whole_price)==0:
            Prod_whole_price = tree.xpath('//span[@class="a-size-base a-color-base"]/text()')
            P_price=Prod_whole_price
        else:
            Prod_fraction_price=tree.xpath('//span[@class="sx-price sx-price-large"]/sup[@class="sx-price-fractional"]/text()')
            price = '$' + Prod_whole_price[0] + '.' + Prod_fraction_price[0]
            P_price.append(price)

        List_price = tree.xpath('//span[@class="a-size-base-plus a-color-secondary a-text-strike"]/text()')
        #print(List_price)
        Star_Rat = tree.xpath('//a[@class="a-popover-trigger a-declarative"]//span[@class="a-icon-alt"]/text()')

        Prod_Star_Rat=[]
        for prod in Star_Rat:
            Prod_Star_Rat.append(get_str(prod,'',' out'))
        #print(Prod_Star_Rat)
        Prod_Review = tree.xpath('//div[@class="s-item-container"]/div[6]/a/text()')
        #print(Prod_Review)
        #Capturing remaining Prod_Review which were not captured earlier
        if len(Prod_Review)==0:
            Prod_Review = tree.xpath('//div[@class ="s-item-container"]/div[5]/a/text()')

        Prod_Url = tree.xpath('//div/a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@href')
        #print(Prod_Url)

        with open("AmazonPrinterData.csv", "a", newline='') as file:
            # Defines column names into a csv file.
            field_names = ['Prod_name', 'Brand_name', 'Prod_price', 'Cross_price', 'Prod_Star_Rat', 'Prod_Review', 'Prod_Url']
            writer = csv.DictWriter(file, fieldnames=field_names)
            # Condition for writing header only once.

            for (Prod_name_val, Brand_name_val, P_price_val, List_price_val, Prod_Star_Rat_val, Prod_Review_val, Prod_Url_val) in itertools.zip_longest(Prod_name, Brand_name, P_price, List_price, Prod_Star_Rat, Prod_Review, Prod_Url):

                # Writing all information in a row.
                writer.writerow(
                    {
                        'Prod_name': Prod_name_val,
                        'Brand_name': Brand_name_val,
                        'Prod_price': P_price_val,
                        'Cross_price': List_price_val,
                        'Prod_Star_Rat': Prod_Star_Rat_val,
                        'Prod_Review': Prod_Review_val,
                        'Prod_Url': Prod_Url_val
                    }
                )



