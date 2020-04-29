from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import urllib.parse
import csv

class AmazonReviews:

    def __init__(self):
        self.first_three = []
        self.headers = {"User-Agent" : "Mozilla/5.0"}
    
    def set_sleep_time(self):
        sleep_time = randint(1,10)
        sleep(sleep_time)
    
    def open_url(self,url):
        values = {}
        data = urllib.parse.urlencode(values).encode("utf-8")
        req = urllib.request.Request(url, data, self.headers)
        response = urlopen(req)
        html = response.read()
        return html
    
    def save_data(self,row):
        with open("data/amazon_reviews.csv","a+") as f:
            reviewwriter = csv.writer(f,delimiter='$')
            reviewwriter.writerow(row)
 

    def fetch_url(self,url):
            html = self.open_url(url)
            bsObj = BeautifulSoup(html,features="html.parser")
            self.first_three.append(bsObj.find("div",{"class":"column col2 "}).find("td",{"class":"value"}).getText()) #//div[@class='column col2 ']/descendant-or-self::node()/td[@class='value']
            self.first_three.append(bsObj.find("span",{"id":"productTitle"}).getText().strip())
            self.first_three.append(self.first_three[1].split(" ")[0])
            all_reviews_link = bsObj.find("a",{"data-hook":"see-all-reviews-link-foot"})["href"]
            self.set_sleep_time()
            self.fetch_reviews(all_reviews_link)
    
    def fetch_reviews(self,all_reviews_link):
        try:
            url = "https://www.amazon.in" + all_reviews_link
            html = self.open_url(url)
            bsObj = BeautifulSoup(html)
            reviews = bsObj.findAll("div",{"class":"a-section celwidget"})
            reviews = reviews[1::]
            next_page_link = ""
            for review in reviews:
                row = []  
                row.extend(self.first_three)
                row.append(review.find("a",{"class":"a-profile"})["href"])
                row.append(review.find("i",{"data-hook":"review-star-rating"}).find("span").getText())
                row.append(review.find("a",{"data-hook":"review-title"}).find("span").getText())
                row.append(review.find("span",{"data-hook":"review-date"}).getText())
                try:
                  row.append(review.find("span",{"data-hook":"avp-badge"}).getText())
                except:
                    row.append("Unverified")
                row.append(review.find("span",{"data-hook":"review-body"}).find("span").getText())
                try:
                  row.append(review.find("span",{"data-hook":"helpful-vote-statement"}).getText())
                except:
                  row.append(0)
                self.save_data(row)
            self.set_sleep_time()
            next_page_link = bsObj.find("li",{"class":"a-last"}).find("a")["href"]
            if next_page_link is not None:
                self.fetch_reviews(next_page_link)
        except AttributeError as e:
            print(e)
        except TypeError as e:
            print(e)
    
review = AmazonReviews()
review.fetch_url("https://www.amazon.in/gp/product/B07B1BRMKC/ref=s9_acss_bw_cg_catrevmp_5b1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=MWMJE97HX772YNM2MGVF&pf_rd_t=101&pf_rd_p=e0fd0416-84d5-4d58-a389-5bc389f1f8a2&pf_rd_i=1375427031")