from selenium import webdriver
from selenium.webdriver.common import keys
import csv
import time
import argparse
from tkinter.filedialog import askopenfilename

# make a pd df and use that instead of data[], 

import pandas as pd

book_df =  pd.DataFrame(columns = ['book_title',
        'book_author',
        'book_narrator',
        'book_genre',
        'book_year',
        'book_length',
        'book_publisher',
        'image_link',
        'amazon_link',
        'amazon_price',
        'goodreads',
        'rating',
        'book_review'])



driver = ''


newFile = input('Select a file y/n: ')
rukyle = input("are you kyle? y/n: ")
if(rukyle=="n"):
	username = input("Enter your GoodReads username/email: ")
	password = input("Enter your GoodReads password: ")
else:


    username = "kylespigvids@gmail.com"
    password = "grMesaboogie52"



def login_to_goodreads(username, password):
    driver.find_element_by_css_selector('#userSignInFormEmail').send_keys(username)
    driver.find_element_by_css_selector('#user_password').send_keys(password)
    #driver.find_element_by_css_selector('#user_password').send_keys('\n')
    driver.find_element_by_xpath('//*[@id="sign_in"]/div[3]/input[1]').click()


def csv_to_list(input_file):
    
    if(newFile=="y"):
        csv_file = askopenfilename()
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = list(csv_reader)
        return data


    else:
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
        'goodreads',
        'rating',
        'book_review'
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
        #
        url = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]/a')
        link = url.get_attribute('href')
        return link
    except:
        return ""

def scrape_url(link):
    driver.get(link)
    time.sleep(3)

    
    try: 
        book_title = driver.find_element_by_xpath('//*[@id="bookTitle"]').text


    except:
        book_title = ""


    try:
        author_name = '\n'.join([x.text.strip() for x in driver.find_elements_by_xpath('//*[@class="authorName"]/span[@itemprop="name"]')])
    except: 
        author_name = ""


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
        published_by = details[1].strip().split('(')[0]
    except:
        publish_year = ""
        published_by = ""



    try:
        book_price = driver.find_element_by_css_selector('.glideButton.buttonBar').text.split('$')[-1] 
    except:
        book_price = ''


    try:
        book_rating = driver.find_element_by_css_selector('#bookMeta > span:nth-child(2)').text 
    except:
        book_rating = ''


    
        
    # review_dict = {}
    
    # reviews = driver.find_elements_by_xpath('//div[@class="friendReviews elementListBrown"]')
    # print(len(reviews))

    # driver.execute_script("window.scrollTo(0, 1500)") 


    # for idx, review in enumerate(reviews, 1):
        
    #     try:
    #         review.find_element_by_xpath('.//div[@class="reviewText stacked"]/span/a').click()
    #         text = review.find_element_by_xpath('.//div[@class="reviewText stacked"]/span/span[2]').text
            
    
        
    #     except Exception as e:
    #         print(type(e), e)
    #         print(f'No button for review {idx}!')
            
    #         try:
    #             text = review.find_element_by_xpath('.//div[@class="reviewText stacked"]/span/span[1]').text   

    #         except Exception as e:
    #             print(type(e), e)
    #             text = "short review"     



            
    #     review_dict[idx] = text

    # book_review = review_dict









    return book_title, author_name, book_length, book_image_link, publish_year, published_by, amazon_link, book_genre, book_price, book_rating, book_review

      

   

def main(input_file, output_file):
    options = webdriver.ChromeOptions() 
    #options.add_argument("start-maximized") 
    # options.add_argument("headless") 
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option('useAutomationExtension', False)
    global driver
    #driver = webdriver.Chrome('./chromedriver', options=options) #Comment this line and use the second option if you need to provide executable webdriver path

    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

    driver.get('https://www.goodreads.com')
    login_to_goodreads(username, password)
    print("[*] Successfully loggedin")
    create_csv_file(output_file)
    # titles = read_from_txt_file(input_file)  
    rows = csv_to_list(input_file)[1:]

    try:
        for row in rows:

           # data = row[,1:12]

            dataDict = {}

            data = ['','','','','','','','','','','','','','']
            data[0] = row[0]
            print(row[0])
            link = search_for_title(data[0])
            if link != "":
                book_title, author_name, book_length, book_image_link, publish_year, published_by, amazon_link, book_genre, book_price, book_rating, book_review = scrape_url(link) 

                dataDict = {'book_title':book_title, 
                'author_name':author_name, 
                'book_length':book_length, 
                'book_image_link':book_image_link, 
                'publish_year':publish_year, 
                'published_by':published_by, 
                'amazon_link':amazon_link, 
                'book_genre':book_genre, 
                'book_price':book_price,
                'link':link,
                'book_rating':book_rating,
                'book_review':book_review}
              
                data[1] = book_title
                data[2] = author_name
                data[5] = publish_year[-4:]
                data[6] = book_length
                data[7] = published_by
                data[8] = book_image_link
                data[9] = amazon_link
                data[4] = book_genre
                data[10] = book_price
                data[11] = link
                data[12] = book_rating
                data[13] = book_review


            write_into_csv_file(output_file, data)

           # book_df = book_df.append(dataDict)

           # print(book_df)





    except Exception as E:
        print(E)

    finally:
        driver.close()
        driver.quit()
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='add, modify and delete upstream nodes')
    ap = argparse.ArgumentParser(prog='GoodreadsScraper.py',
                                    usage='%(prog)s [options] --input ./booktitle.csv --output output.csv',
                                    description='Start scrapping of the input .txt file and store in output .csv file')
    ap.add_argument( '-i','--input',type=str,action='store', required=True, help='input txt file path(default:current path)')
    ap.add_argument( '-o','--output' ,type=str, action='store',required=True,help='output csv fiel path(defualt: current path)')
    args = ap.parse_args()
    input_file = args.input
    output_file = args.output
    print('reading book title..')
    main(input_file, output_file)