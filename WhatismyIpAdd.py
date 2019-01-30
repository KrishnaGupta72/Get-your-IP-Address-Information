import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# ____________________Input Section : ____________________________

tot_ip_address = int(input("Please enter total number of Ip Addresses, do you want to get information: "))
ip_address = []
for i in range(0, tot_ip_address):
    j = i + 1
    ip_address.append(input('Please enter "%d" Ip Address for example("23.81.209.109"): ' % j))

# ____________________Input Section : ____________________________

driver = webdriver.Chrome("E:/PyCharm Projects/chromedriver.exe")  # Your chromedriver file path
driver.get('https://www.ip2location.com/demo')  # Hitting url

count_4_header = 0
for ip in ip_address:
    text_box = driver.find_element_by_xpath('//input[@class="form-control input-lg"]')  # Getting Input box element
    text_box.clear()  # Clear the input box before insert
    time.sleep(3)
    text_box.send_keys(ip)  # Passing IP Address value to the input box
    time.sleep(1)
    text_box.send_keys(Keys.RETURN) # Returning Ip Information by sending the Ip Address
    #No need to hit submit button above line will do this job
    ## clk_button = driver.find_element_by_xpath('//button[@class="btn btn-primary btn-lg"]')
    ## clk_button.click()

    OlsonTimeZone_NotFound = 0
    Per_link = driver.find_elements_by_xpath('//td[@class ="col-sm-7"]')#Getting Permanentlink element and so on....
    #For some Ip Addresses "OlsonTimeZone" element is not there. So handling this by using try block.
    try:
        OlsonTimeZone_val = Per_link[19].text
    except Exception as e:
        # print("Exception found: ", format(e))
        OlsonTimeZone_NotFound = 1

    for i in range(0, 1):# Loop for accessing every element as it available on website.
        count_4_header = count_4_header + 1
        with open("IP_Information.csv", "a", newline='') as file:
            # Defines column names into a csv file.
            field_names = ['Permalink', 'IP Address', 'Country', 'Region', 'City', 'Coordinates of City', 'ISP',
                           'Local Time', 'Domain', 'Net Speed', 'IDD & Area Code', 'ZIP Code', 'Weather Station',
                           'Mobile Carrier', 'Mobile Country Code - MCC', 'Mobile Network Code - MNC', 'Elevation',
                           'Usage Type', 'Anonymous Proxy', 'Olson Time Zone']
            writer = csv.DictWriter(file, fieldnames=field_names)
            # Condition for writing header only once.
            if count_4_header == 1:
                writer.writeheader()
            # Writing all information in a row.
            writer.writerow(
                {
                    'Permalink': Per_link[i].text,
                    'IP Address': Per_link[i + 1].text,
                    'Country': Per_link[i + 2].text,
                    'Region': Per_link[i + 3].text,
                    'City': Per_link[i + 4].text,
                    'Coordinates of City': Per_link[i + 5].text,
                    'ISP': Per_link[i + 6].text,
                    'Local Time': Per_link[i + 7].text,
                    'Domain': Per_link[i + 8].text,
                    'Net Speed': Per_link[i + 9].text,
                    'IDD & Area Code': Per_link[i + 10].text,
                    'ZIP Code': Per_link[i + 11].text,
                    'Weather Station': Per_link[i + 12].text,
                    'Mobile Carrier': Per_link[i + 13].text,
                    'Mobile Country Code - MCC': Per_link[i + 14].text,
                    'Mobile Network Code - MNC': Per_link[i + 15].text,
                    'Elevation': Per_link[i + 16].text,
                    'Usage Type': Per_link[i + 17].text,
                    'Anonymous Proxy': Per_link[i + 18].text,
                    'Olson Time Zone': Per_link[i + 19].text if OlsonTimeZone_NotFound == 0 else ''

                }
            )






