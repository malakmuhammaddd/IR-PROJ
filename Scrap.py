import requests
from bs4 import BeautifulSoup as bss4
import csv
import urllib
import urllib.request
import os

img_folder = "imgs"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

page_number = 1
Ranking = 1
url = requests.get(f"https://www.jumia.com.eg/televisions/?page={page_number}")
soup = bss4(url.text , 'lxml')
pages_T = ["str"]

with open('products.csv' , 'w',encoding='utf-8',  newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name' , 'Price' , 'Customer ratings' , 'Category' , 'Sales rank' ,'Product brand' , 'img_path'])

while len(pages_T) > 0:
    url = requests.get(f"https://www.jumia.com.eg/televisions/?page={page_number}")
    soup = bss4(url.text , 'lxml')
    products = soup.find_all('article' , {'class' : 'prd _fb col c-prd'})
    List_Brands = []
    categorise = soup.find_all('article' , {'class' : '-phs -bt'})
    for category in categorise:
        if category.find('h2').text == "Brand":
            brands = category.find_all('a' , {'class' : 'fk-cb -me-start -fsh0'})
            for brand in brands:
                List_Brands.append(brand.text)
            break
    with open('products.csv' , 'a',encoding='utf-8',  newline='') as file:
        writer = csv.writer(file)
        product_Category = soup.find('h1' , {'class' : '-fs20 -m -elli -phs'}).text   
        for product in products:
            Product_Name = product.find('h3' , {'class' : 'name'}).text
            Product_Price = product.find('div' , {'class' : 'prc'}).text
            Product_Rating = product.contents[1].find('div' , {'class' : 'stars _s'})
            Product_Sales_rank = Ranking
            Product_Brand = "Unknown"
            img_url = product.find('img' , {'class' : 'img'})['data-src']
            file_loc = os.path.join(os.getcwd(), img_folder, Product_Name.replace('"','').replace('/' , '') + '.jpg')
            if not os.path.isfile(file_loc):
                urllib.request.urlretrieve(img_url, file_loc)
            Brandd = Product_Name.split()[0]
            if Brandd in List_Brands:
                Product_Brand = Brandd
            Ranking+=1
            if Product_Rating is None:
                writer.writerow([Product_Name , Product_Price , "N/A" , product_Category , Product_Sales_rank , Product_Brand , os.path.join(img_folder , os.path.basename(file_loc))])
            else:
                    writer.writerow([Product_Name , Product_Price , Product_Rating.contents[0].split()[0] , product_Category , Product_Sales_rank , Product_Brand ,os.path.join(img_folder , os.path.basename(file_loc))])     
    print(f"done {page_number}") 
    pages_T = soup.find_all('a' , {'aria-label' : 'Next Page'})
    page_number+=1
    print(len(pages_T)) 
    

     
    


