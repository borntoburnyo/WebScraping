import requests 
import bs4 
from bs4 import BeautifulSoup 
import re 
import pandas as pd 
from time import sleep, time 
from warnings import warn 
import numpy as np 

#From year 2000 to 2017
#Scraping the first four pages of each year
pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000, 2018)]

#a few containers 
start_time = time()
num_requests = 0
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

#main body 
for year_url in years_url:
    for page in pages:
        #request web contents
        response = requests.get('http://www.imdb.com/search/title?release_date=' + \
                               year_url + '&sort=num_votes,desc&page=' + page)
        
        #pause for a while, try not be banned 
        sleep(np.random.randint(10,20))
        
        #print process info 
        num_requests += 1
        elapsed_time = time() - start_time
        print("request: {} frequency: {:.3f}".format(num_requests, num_requests/elapsed_time))
        
        if response.status_code != 200:
            warn("request: {} status: {}".format(num_requests, response.status_code))
        
        #set limit for total pages scrapped 
        if num_requests > 72:
            warn("number of requests exceed threshold!")
            break 
        
        #parse web content into beautiful soup object 
        soup = BeautifulSoup(response.content, 'lxml')
        
        #find the minimum self-contained section with all the information we need 
        movie_containers = soup.find_all('div', class_='lister-item mode-advanced')
        
        #loop through each section
        for container in movie_containers:
            #we need both IMDb ratings and Metascores
            if container.find('div', class_ = 'ratings-metascore') is not None:
            
                #find movie name
                name = container.h3.a.string 
                names.append(name)
                
                #find release year
                year = container.h3.find_all('span')[1].string
                year = int(re.sub("[^0-9]", "", year))
                years.append(year)
        
                #find IMDb rating
                imdb_rating = float(container.strong.string)
                imdb_ratings.append(imdb_rating)
        
                #find Metascore
                metascore = int(container.find('div', class_='inline-block ratings-metascore').span.string)
                metascores.append(metascore)
        
                #find how many voters
                vote = container.find('span', string="Votes:").find_next().string
                vote = int(re.sub("[^0-9]", "", vote))
                votes.append(vote)   
                
#build pandas dataframe
movies = pd.DataFrame(
    {'movie': names,
    'year': years,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'vote': votes}
)

#take a peek
movies.head()             
                
           
