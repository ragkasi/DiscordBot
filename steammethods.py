import discord
from discord.ext import commands
from random import *
import discord
from discord.ext import commands,tasks
import os
from flask import *
import requests
import bs4
from bs4 import BeautifulSoup
import random
from random import randrange

app = Flask(__name__) 

if __name__=='__main__':
   app.run()

def get_game_containers(soup):
    #goes over the page and makes a "soup" or each class that has the name 
    #.search_result_row

    #Each one of these holds a "game" inside.
    
    return soup.select(".search_result_row")

def get_name(soup):
    #get from the soup the item that has <span, with a class = "title"!
    title = soup.find("span", class_="title")
    #Return the title as a string.
    return title.text.strip()

def get_date(soup):
    return soup.select(".col.search_released.responsive_secondrow")[0].text

def get_price(soup):
    try:
        price = soup.select(".discount_original_price")[0].text.strip()
    except IndexError:
        price = "free"
    try:
        discount = soup.select(".discount_final_price")[0].text.strip()
    except IndexError:
        discount = price
    if price != "free" and price != discount:
        price = f"{price}/{discount}"
    return price # return price

def get_review(soup):
    top = soup.select(".col.search_reviewscore.responsive_secondrow")
    rev = top[0].select(".search_review_summary")
    if len(top) > 0 and len(rev) > 0:
        return rev[0].attrs['data-tooltip-html']
    else:
        return ""
    
def get_games(game_containers):
    list_of_games=[]
    #For each game in the soup of games
    for game in game_containers:

        #Get the string of each part through the methods above...
        name = get_name(game)
        date = get_date(game)
        price = get_price(game)
        reviews = get_review(game)

        #Append to the array a series of elements for each game!
        list_of_games.append((name,date,price,reviews))
    return list_of_games #An array with each entry the basic info of the game.


def teamgen_command(message):
    names_list = message.content.split()
    num_of_teams = int(names_list[1])
    names_list = names_list[2:]
    teams = {x+1:[] for x in range(num_of_teams)} 
    cool_num = len(names_list)//num_of_teams
    for i in range(num_of_teams-1):
        for x in range(cool_num):            
            teams[i+1].append(names_list.pop(randrange(len(names_list))))
    teams[num_of_teams] = names_list
    finalstring = ""
    for i in range(num_of_teams):
        finalstring += f"Team {i+1}:"
        for x in teams[i+1]:
            finalstring += " " + x
        finalstring+= "\n"
    return finalstring

def sale_command(message):
    x = message.content.split()
    url = "https://store.steampowered.com/search/?sort_by=Reviews_DESC&term={x[1]}&specials=1&supportedlang=english&ndl=1"
    session_id = {'cookie': 'sessionid=21276008a014b2b56c02855f'}
    page = requests.get(url, headers=session_id)
    soup = bs4.BeautifulSoup(page.text,"lxml")
    game_containers = get_game_containers(soup)
    games = get_games(game_containers)
    return_message = ""

    random_index = []
    for i in range(10):
        random_num = random.randrange(0, len(games))
        while random_num in random_index:
            random_num = random.randrange(0, len(games))
        random_index.append(random_num)
    return_list = []
    for i in range(10):
        this_game = games[random_index[i]]
        return_list.append(this_game)
    
    for i,message in enumerate(return_list):
        message_3 = "".join(message[3])
        return_message += "{}\n    Release Date: {}\n    Sale: {}\n    Rating: {}\n\n".format(message[0],message[1],message[2],message_3)



    return return_message.replace("<br>","\n      ")


def ratings_command(message):
    genre = message.content.split()[1] #Get the genre from the input.

    #go to the url with the right genre on the sale setting...
    url = f"https://store.steampowered.com/search/?sort_by=Reviews_DESC&term={genre}&force_infinite=1&supportedlang=english&ndl=1"

    #now use beautifulSoup to get the page as a "soup" 
    #Cookie says what page. A particular page = session id.
    session_id = {'cookie': 'sessionid=21276008a014b2b56c02855f'}

    #requests.get is a method for the url - take the page from the given url, second part is extra returns a request.
    page = requests.get(url, headers=session_id)

    #putting in page.text which is the html of the given page. "lxml" should always be there
    soup = bs4.BeautifulSoup(page.text,"lxml")

    #Feeds in the whole page to get_game_containers...
    game_containers = get_game_containers(soup)

    #Feed in the soup of "games" to get_games.
    games = get_games(game_containers)
    #now we have an array containing the name, rating, and price for each game!
    
    #use f-string to format the output
    output = f"Here are top ten games for {genre}: \n"
    for i, game in enumerate(games[0:9]):
        name = game[0]
        date = game[1]
        price = game[2]
        rating = game[3]
        
        output += f"{i+1}. {name} \n date: {date}\n pricing：{price}\n rating：{rating}% \n\n"

    return output.replace("<br>","\n      ")
#Returns an array with each game and its name, price, and rating

def random_command(message):
    x = message.content.split()

    url = f"https://store.steampowered.com/search/?&term={x[1]}&supportedlang=english&ndl=1"
    #Cookie says what page. A particular page = session id.
    session_id = {'cookie': 'sessionid=21276008a014b2b56c02855f'}

    #requests.get is a method for the url - take the page from the given url, second part is extra returns a request.
    page = requests.get(url, headers=session_id)

    #putting in page.text which is the html of the given page. "lxml" should always be there
    soup = bs4.BeautifulSoup(page.text,"html.parser")

    if(x[0] == "!random"):
        games = get_games(get_game_containers(soup))
        gameNames = []
        i = 0
        while(i < len(games)):
            gameNames.append([games[i][0], games[i][2]])
            i+=1

    duplicates = []
    return_list = []
    if(len(gameNames) > 9):
        for i in range(10):
            num = (int) (random.random()*len(gameNames))
            duplicates.append(num)
            if(num in duplicates):
                return_list.append(gameNames[num])
        s = ""
    for i in range(len(return_list)):
        s += f"Game: {return_list[i][0]} \n Price: {return_list[i][1]} \n\n"

    return s.replace("<br>","\n      ")
