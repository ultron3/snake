import pygame
import time
import random
import mysql.connector

# Inizializzazione di Pygame
pygame.init()

# Definizione dei colori
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Dimensioni della finestra di gioco
dis_width = 1000
dis_height = 600

# Creazione della finestra di gioco
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 20
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Connessione al database MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="golfclub",
    database="snake_game"
)

mycursor = mydb.cursor()

def save_score(nickname, score):
    sql = "INSERT INTO giocatore (nickname, score) VALUES (%s, %s)"
    val = (nickname, score)
    mycursor.execute(sql, val)
    mydb.commit()

def update_score(nickname, score):
    sql = "UPDATE giocatore SET score = %s WHERE nickname = %s"
    val = (score, nickname)
    mycursor.execute(sql, val)
    mydb.commit()

def get_score(nickname):
    sql = "SELECT score FROM giocatore WHERE nickname = %s"
    val = (nickname,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        return result[0]
    return None

def get_leaderboard():
    sql = "SELECT nickname, score FROM giocatore ORDER BY score DESC LIMIT 10"
    mycursor.execute(sql)
    return mycursor.fetchall()

def your_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, pos):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, pos)

def game_instructions():
    instructions = True
    while instructions:
        dis.fill(blue)
        message("Istruzioni", black, [dis_width / 3, dis_height / 4])
        message("Usa le frecce per muovere il serpente", black, [dis_width / 8, dis_height / 2.5])
        message("Premi B per tornare al menu", red, [dis_width / 5, dis_height / 2])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    instructions = False

def display_leaderboard():
    leaderboard = get_leaderboard()
    leaderboard_display = True
    while leaderboard_display:
        dis.fill(blue)
        message("Classifica", green, [dis_width / 3, dis_height / 10])
        for index, (nickname, score) in enumerate(leaderboard):
            message(f"{index + 1}. {nickname}: {score}", black, [dis_width / 6, dis_height / 5 + index * 30])
        message("Premi B per tornare al menu", red, [dis_width / 3, dis_height - 50])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    leaderboard_display = False

def gameLoop(nickname):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Hai perso. Premi C per riniziare o Q per tornare al menu", red, [dis_width / 6, dis_height / 3])
            your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = False
                        game_menu()  # Tornare al menu principale
                    if event.key == pygame.K_c:
                        if get_score(nickname) is None:
                            save_score(nickname, Length_of_snake - 1)
                        else:
                            update_score(nickname, Length_of_snake - 1)
                        gameLoop(nickname)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    if get_score(nickname) is None:
        save_score(nickname, Length_of_snake - 1)
    else:
        update_score(nickname, Length_of_snake - 1)
    pygame.quit()
    quit()


def enter_nickname():
    nickname = ""
    entering = True
    while entering:
        dis.fill(blue)
        message("Inserisci il tuo nickname: " + nickname, black, [dis_width / 6, dis_height / 3])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                else:
                    nickname += event.unicode

    return nickname

def game_menu():
    menu = True
    while menu:
        dis.fill(blue)
        message("Snake Game", green, [dis_width / 3, dis_height / 4])
        message("Premi A per Avvio", black, [dis_width / 3, dis_height / 2.5])
        message("Premi I per Istruzioni", black, [dis_width / 3, dis_height / 2])
        message("Premi L per classifica", black, [dis_width / 3, dis_height / 1.5])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    nickname = enter_nickname()
                    menu = False
                    gameLoop(nickname)
                if event.key == pygame.K_i:
                    game_instructions()
                if event.key == pygame.K_l:
                    display_leaderboard()

game_menu()
