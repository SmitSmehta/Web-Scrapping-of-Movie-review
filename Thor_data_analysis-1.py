#Author:-Smit Mehta


from time import time
from time import sleep
from random import randint
import urllib2
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from requests import get
from IPython.core.display import clear_output
from warnings import warn
import re
import numbers
import csv
import string

from collections import Counter
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt



pages = [str(i) for i in range(1,16)]


url = 'https://www.rottentomatoes.com/m/thor_ragnarok_2017/reviews/'
res = get(url)

#Creating Soup to check number of pages
soup = bs(res.text,'html.parser')
PAGE = soup.find('span',class_='pageInfo')
print'Number of pages are :---  ',PAGE.text




# Redeclaring the lists to store data in
reviews = []
ratings = []
floats=[]
Rates = []




# Preparing the monitoring of the loop
start_time = time()
requests = 0


    
# For every page in the interval 1-4
for page in pages:
        
        # Make a get request
        response = get('https://www.rottentomatoes.com/m/thor_ragnarok_2017/reviews/?' + page + 
        '&sort=' )
        # Parse the content of the request with BeautifulSoup
        page_html = bs(response.text, 'html.parser')
        
        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'review_desc')
        
        # For every movie of these 50
        for container in mv_containers:
            
           #Reviews of the movie
            review = container.find('div',class_='the_review')
            reviews.append(review.text)
           
            #Rating of the movie for Data Frame
            rating =  container.find('div',class_ = 'small subtle')
            ratings.append(rating.text)
            
                  
            trial = container.find('div',class_ = 'small subtle')
            #Ratings of the MOVIE
            floats.append((trial.text))
            
            #gettign list of numbers
            for story_heading in container.find_all(class_ = 'small subtle'):
                story_title = story_heading.text.replace('/5', ' ').strip()
                story_title = story_title.replace('/10',' ').strip()
                new_story_title = story_title.encode('utf-8')
                story_title_list = story_title.split()
                #story_title_list = new_story_title.split()
                #print '\n',story_title_list
                #print '\n',new_story_title
                for word in story_title_list:
                    try:
                        float(word)  # True if string is a number contains a dot
                        
                        Rates.append(word)        
                    except ValueError:  # String is not a number
                        pass
                           
                #Dataframe of reviews and ratings                             
                df = pd.DataFrame({'Review': reviews,'Rating': ratings})       

print ''
print 'ALL Rating :- ',df['Rating'] 
print''
Rates = '  '.join(Rates)
print '\nRatings: ', Rates,' '
#test_df.dropna()                
#print test_df

#Top 20 reviews
print '\nTop 20 reviews are : \n',df['Review'].head(20)

#Bottom 20 reviews
print '\nBottom 20 reviews are : \n',df['Review'].tail(20)



#Bonus


stopwords = []
Review = []
Top_20 = []
Bottom_20 = []
stopwords_file = open("C:\Smit\Stevens College\First Sem\Em 624  Python\Assignment\Assignment 8\stopwords_en.txt","rU") 

for word in stopwords_file:
    stopwords.append( word.strip('\n') )

#Top 20 review in list    
for story_heading in df['Review'].head(20):
    story_title = story_heading.replace('\n', ' ').strip()
    new_story_title = story_title.encode('utf-8')
    story_title_list = new_story_title.split()
    #print '\n',new_story_title
    for word in story_title_list:
        if word.isalpha():
            Top_20.append(word.lower())
    

#Bottom 20 review in list    
for story_heading in df['Review'].tail(20):
    story_title = story_heading.replace('\n', ' ').strip()
    new_story_title = story_title.encode('utf-8')
    story_title_list = new_story_title.split()
    #print '\n',new_story_title
    for word in story_title_list:
        if word.isalpha():
            Bottom_20.append(word.lower())


Top_20 = [word for word in Top_20 if word not in stopwords]
Top_20 = ' '.join(Top_20)
#print Top_20

Bottom_20 = [word for word in Bottom_20 if word not in stopwords]
Bottom_20 = ' '.join(Bottom_20)


# Defining the wordcloud parameters
Top = WordCloud(background_color="white", max_words=2000,
               stopwords=stopwords)
Bottom = WordCloud(background_color="white", max_words=2000,
               stopwords=stopwords)


Top.generate(Top_20)
Bottom.generate(Bottom_20)

# Show the cloud
plt.figure()
plt.title('Top 20 reviews')
plt.imshow(Top)
plt.axis('off')


plt.figure()
plt.title('Bottom 20 reviews')
plt.imshow(Bottom)


plt.axis('off')
plt.show()



            