import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import os
pageCount = 1;
titles = list()
authors = list()
years = list()
siteNumber = 1;
siteOneMax = 300;
siteTwoMax = 260;


def Write(pagenum):    
    if(len(titles) == len(authors)) and (len(authors) == len(years)):   
  

        print("writing")
        book_stuff = pd.DataFrame(
            {
                'Title': titles,
                'Authors': authors,
                'Years': years
            })
        #print(book_stuff)
        book_stuff.to_csv('ReWebCrawl'+str(pagenum)+'.csv')
        print("complete")
    else:
        print(len(titles))
        print(len(authors))
        print(len(years))

    titles.clear();
    authors.clear();
    years.clear();
    #os.system('cls');
    return;



if(siteNumber == 1):
    print("Running First Website:");
    while pageCount < siteOneMax:
        #print("1: Running Page "+str(pageCount))
        page = requests.get('https://www.goodreads.com/search?page='+str(pageCount)+'&q=Children&qid=YC104Fn5WK&tab=books')
        soup = BeautifulSoup(page.content, 'html.parser')

        container = soup.find("table", class_="tableList")
        test = 4
        index = 0
        rows = list()
       
        for row in container.findAll("tr"):
           
            rows.append(row)
            author = row.find(class_ ="AuthorName")
            titles.append(row.find("span", itemprop="name").get_text())
            authors.append(row.find(class_="authorName").get_text())
            year = row.find(class_="greyText smallText uitext").get_text()
            #print(titles[index])
            yearIntConfirm = re.findall('[1-3][0-9]{3}', year)
            if yearIntConfirm:
                x = int(yearIntConfirm[0]);
                if(x > 0) and( x < 2021):
                    years.append(x)
                else:
                    years.append(-1);
            else:
                years.append(-1);
            index += 1
        print("Site One: " + str(pageCount/siteOneMax * 100) + '%');
        #print("1: round "+str(pageCount)+" complete")
        pageCount +=1
    Write(12)
    pageCount = 1
    #siteNumber = 2

print("Running Second Website:");
if(siteNumber == 2):
    while(pageCount < siteTwoMax):
        page = requests.get('https://openlibrary.org/search?q=Children&mode=everything&page='+str(pageCount))
        soup = BeautifulSoup(page.content, 'html.parser')
        container = soup.find(id ="siteSearch")
        if container != None:
            
            items = container.find_all(class_='searchResultItem')
            
            for item in items:
                titles.append(str( item.find(class_="booktitle").get_text()).strip())
                author = str(item.find(class_="bookauthor").get_text()).strip();
                if "by" in author:
                    author = author[author.find("by",0, 5) + 2 : len(author)];
                    authors.append(author);
                else:
                    authors.append(author);
                
                year = item.find(class_="resultPublisher").get_text()
                
                year = year.partition("edition")[2]
                yearIntConfirm = re.findall('[1-3][0-9]{3}', year)
                
                if yearIntConfirm:
                    #print(yearIntConfirm[0])
                    x = int(yearIntConfirm[0])
                    if(x > 0) and( x < 2021):
                        years.append(x)
                    else:
                        years.append(-1);
                else:
                    years.append(-1)
        else:
            print("Nothing collected from page: " + str(pageCount));
        print("Site Two: " + str(pageCount/siteTwoMax * 100) + '%');
        pageCount+=1
    Write(siteNumber)

    

