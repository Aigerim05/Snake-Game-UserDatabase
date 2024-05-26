import pygame
from game_object import GameObject 
from worm import Worm
from food import Food
from wall import Wall

from Pausing import pause

#--------------------Functions to insert and update data---------------------------------------
import psycopg2
from config import load_config

def insert_username(username, level):

    sql = """INSERT INTO snake_user(user_name, level)
             VALUES(%s,%s)"""
    
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:

                cur.execute(sql, (username, level))

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  

def insert_score(username, score):

    sql = """INSERT INTO snake_score(user_name, score)
             VALUES(%s,%s)"""
    
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:

                cur.execute(sql, (username, score))

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 

def update_level(username, level):

    sql = """ UPDATE snake_user
                SET level = %s
                WHERE user_name = %s"""
    

    config = load_config()
    
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
            
                cur.execute(sql, (level, username))

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  

def update_score(username, score):

    sql = """ UPDATE snake_score
                SET score = %s
                WHERE user_name = %s"""
    

    config = load_config()
    
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
            
                cur.execute(sql, (score, username))

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)    

#-----------------------------------------------------------

def create_background(screen, width, height):
        colors = [(255, 255, 255), (212, 212, 212)]
        tile_width = 20
        y = 0
        while y < height:
                x = 0
                while x < width:
                        row = y // tile_width
                        col = x // tile_width
                        pygame.draw.rect(screen, colors[(row + col) % 2],pygame.Rect(x, y, tile_width, tile_width))
                        x += tile_width
                y += tile_width

done = False

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

worm = Worm((0,0,255), 20)
food = Food((100,20),(0,255,0), 20)
wall = Wall(20)
super_food = Food((120,20), (0,0,0), 20)

FPS = 5
score = 0
five_seconds = 5000

font_small = pygame.font.SysFont("Verdana", 17)
disappear_time = pygame.time.get_ticks() + five_seconds

#-------------Updating list of usernames in usernames.txt----------------------------------------------

username = input("Username: ")

with open('usernames.txt','r+') as file:
    username_list = file.read()
    if username not in username_list:
        file.write(username + '\n')
        insert_username(username,str(wall.level))
        insert_score(username,str(score))

#-----------------------------------------------------------


                             
while not done:
        filtered_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    update_level(username, str(wall.level))
                    update_score(username, str(score))
                    done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                        update_score(username, str(score))
                        pause(screen, score)
                else:
                        filtered_events.append(event)

        worm.process_input(filtered_events)
        worm.move()
       
        # return to initial condition if snake leaves screen or touches walls
        if worm.detect_screen() or worm.detect_wall(wall.points):
              worm = Worm((0,255,255),20)
              FPS = 5
              update_level(username, str(wall.level))
              update_level(username, str(score))
              score = 0
              wall.level = 0
              
        
                   

        # super_food is disappearing item
        if pygame.time.get_ticks() >= disappear_time:
                super_food = Food(food.get_random_coordinates(worm.points+wall.points+food.points), (0,0,0), 20)
                disappear_time = pygame.time.get_ticks() + five_seconds

        # check if snake can eat and eating
        pos_food = food.can_eat(worm.points[0])
        pos_super_food = super_food.can_eat(worm.points[0])

        if(pos_food != None):
           
            worm.increase(pos_food)
            score += 1
            food = Food(food.get_random_coordinates(worm.points+wall.points),(0,255,0), 20)

            # change level if score % 3
            if len(worm.points) % 3 == 0:
                wall.next_level()
                FPS += 2

        if(pos_super_food != None):
            worm.increase(pos_super_food)
            score += 2
            # change level if score % 3
            if len(worm.points) % 3 == 0:
                wall.next_level()
                FPS += 2

        create_background(screen, 400, 300)
        
        # rendering text for score and level score
        score_text = font_small.render("score:" + str(score), True, "black")
        screen.blit(score_text, (320,0))
        level_text = font_small.render("level:" + str(wall.level), True, "black")
        screen.blit(level_text, (320,20))

        food.draw(screen)
        super_food.draw(screen)
        wall.draw(screen)
        worm.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)