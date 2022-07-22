import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_topic_page(url):
    
    response  = requests.get(url)
    
    if response.status_code != 200:
        print('Status code : ', response.status_code)
        raise Exception('Failed to reach webpage ' + topic_repos_url)
        
    doc = BeautifulSoup(response.text, 'html.parser')
    
    return doc


def get_movie_details(movie_doc, i):
    
    # getting different movie details
    movie_first_line = movie_doc[i].find("h3", class_="lister-item-header")
    movie_title = movie_first_line.find("a").text
    movie_release_date = movie_first_line.find_all("span")[-1].text[1:-1]
    movie_run_time = movie_doc[i].find("span", class_="runtime").text[:-4]
    movie_genre = movie_doc[i].find("span", class_="genre").text.strip().replace("\n","").split(",")
    movie_rating = movie_doc[i].find("strong").text
    movie_cast = movie_doc[i].find('p', class_="").text.replace("n","").split("|")
    movie_cast = [cast.strip().replace('\n','').split(':') for cast in movie_cast]
    movie_director = movie_cast[0][1]
    
    # returning movie details as a list
    #return [movie_title, movie_rating, movie_run_time, movie_genre, movie_release_date, movie_director]
    return {
        'Movie Name' : movie_title,
        'Rating' : movie_rating,
        'Duration' : movie_run_time,
        'Year Of Release' : movie_release_date,
        'Director' : movie_director,
        'Genre' : movie_genre
    }

def get_top_movies(doc):
    top_movies = doc.find_all("div", class_="lister-item mode-advanced")
    
    all_movies = []
    
    for i in range (50):
        movie_details = get_movie_details(top_movies, i)
        all_movies.append(movie_details)
    return all_movies      


def write_csv(items, category, order):
    with open(f"{category}_movie_list_{order}.csv",'w') as f:
        if len(items) == 0:
            return
        
        headers = list(items[0].keys())
        f.write(','.join(headers) + '\n')
        
        for item in items:
            values = []
            for header in headers:
                values.append(str(item.get(header, '')))
            f.write(','.join(values) + '\n')

def scrape_imdb(category, order):

    website_url = 'https://www.imdb.com/search/title/?groups={}_100&sort=user_rating,{}'.format(category, order)
    
    doc = get_topic_page(website_url)
    website_title = doc.title.text.replace("\n","").replace('100', '50')
    print(website_title)
    top_movies = get_top_movies(doc)
    write_csv(top_movies, category, order)

if __name__ == '__main__':
    
    print('Select what kind of category \n 1. Top rates \n 2. Bottom Rated')
    select_category = int(input('Enter the category : '))
    print('Select the order of list \n 1. Asending Order \n 2. Desending Order')
    select_order = int(input('Enter the number : '))
    
    if select_category ==  1 and select_order == 1:
        scrape_imdb('top', 'asc')
    elif select_category ==  2 and select_order == 1:
        scrape_imdb('bottom', 'asc')
    elif select_category ==  1 and select_order == 2:
        scrape_imdb('top', 'desc')
    elif select_category ==  2 and select_order == 2:
        scrape_imdb('bottom', 'desc')
    else:
        print("You didn't select proper value")
        
    print('\nYour file is created')
