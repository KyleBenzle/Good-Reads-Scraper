from selenium import webdriver
from selenium.webdriver.common import keys
import csv
import time
import argparse


driver = ''




def csv_to_list(input_file):
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = list(csv_reader)
    return data



def create_csv_file(output_file):
    header =['id',
        'book_title',
        'book_author',
        'book_narrator',
        'book_genre',
        'book_year',
        'book_length',
        'book_publisher',
        'image_link',
        'amazon_link',
        'amazon_price',
        'goodreads'
        ]
    with open(output_file, 'w+') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(header)

#No longer Needed
def read_from_txt_file(input_file):
    lines = [line.rstrip('\n') for line in open(input_file, 'r')]
    return lines


def write_into_csv_file(output_file, row):
   with open(output_file, 'a') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(row)

def search_for_title(title):
    driver.get(f"https://www.goodreads.com/search?q={title}")
    time.sleep(2)
    try:
        url = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]/a')
        link = url.get_attribute('href')
        return link
    except:
        return ""

def scrape_url(link):
    driver.get(link)
    time.sleep(3)
    author_name = '\n'.join([x.text.strip() for x in driver.find_elements_by_xpath('//*[@class="authorName"]/span[@itemprop="name"]')])
    try:
        book_length = driver.find_element_by_xpath('//*[@itemprop="numberOfPages"]').text
    except:
        book_length = ""

    try:
        amazon_link = driver.find_element_by_css_selector('#buyButton').get_attribute('href')
    except:amazon_link = ""


    try:
        book_genre = driver.find_element_by_css_selector('.bookPageGenreLink').text
    except:book_genre = ""



    try:
        book_image_link = driver.find_element_by_css_selector('#coverImage').get_attribute('src')
    except:
        book_image_link = ""
    try:
        details =[x.text for x in  driver.find_elements_by_css_selector('#details .row')  if "publish" in x.text.lower()][0]
        details = details.split('by')

        publish_year = details[0].replace("Published", "").strip()
        published_by = details[1].strip()
    except:
        publish_year = ""
        published_by = ""

    return author_name, book_length, book_image_link, publish_year, published_by, amazon_link, book_genre

      

   

def main(input_file, output_file):
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized") 
    # options.add_argument("headless") 
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option('useAutomationExtension', False)
    global driver
    driver = webdriver.Chrome(options=options) #Comment this line and use the second option if you need to provide executable webdriver path
    # driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

    driver.get('https://www.goodreads.com')
    create_csv_file(output_file)
    # titles = read_from_txt_file(input_file)    
    rows = csv_to_list(input_file)[1:]

    try:
        for row in rows:
            data = row
            link = search_for_title(data[1])
            if link != "":
                #['id','book_title','book_author','book_narrator','book_genre','book_year','book_length','book_publisher','image_link','amazon_link','amazon_price','goodreads'
                author_name, book_length, book_image_link, publish_year, published_by, amazon_link, book_genre = scrape_url(link)
                data[2] = author_name
                data[5] = publish_year
                data[6] = book_length
                data[7] = published_by
                data[8] = book_image_link
                data[9] = amazon_link
                data[4] = book_genre

            write_into_csv_file(output_file, data)
    except Exception as E:
        print(E)

    finally:
        driver.close()
        driver.quit()
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='add, modify and delete upstream nodes')
    ap = argparse.ArgumentParser(prog='GoodreadsScraper.py',
                                    usage='%(prog)s [options] --input ./booktitle.txt --output output.csv',
                                    description='Start scrapping of the input .txt file and store in output .csv file')
    ap.add_argument( '-i','--input',type=str,action='store', required=True, help='input txt file path(default:current path)')
    ap.add_argument( '-o','--output' ,type=str, action='store',required=True,help='output csv fiel path(defualt: current path)')
    args = ap.parse_args()
    input_file = args.input
    output_file = args.output
    print('reading book title..')
    main(input_file, output_file)
