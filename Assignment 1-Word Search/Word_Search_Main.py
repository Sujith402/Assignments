import pygame 
from random_words import RandomWords
import random 
import sys

#generating random words
def gen_words():
    rw=RandomWords()
    words=[]
    while len(words)<10:
        word=rw.random_word()
        if 3<len(word)<9:
            words.append(word)
    return words

#create a list containing the box positions
def available_positions(num_letters,letter_size):
    available_pos=[]
    for i in range(num_letters):
        for j  in  range(num_letters):
            available_pos.append((i*letter_size,j*letter_size))
    return available_pos

def find_word_position(words,available_pos,letter_size,num_letters):
    pos_words={}
    global filled_positions
    filled_positions=[]
    for word in words:
        set_pos=True
        l=len(word)*letter_size
        l1=len(word)
        while set_pos:
            initial_pos=random.choice(available_pos)
            x,y=initial_pos
            available_max_pos=[]
            if x+l<=(num_letters)*letter_size:
                available_max_pos.append((x+l-letter_size,y))
                if y+l<=(num_letters)*letter_size:
                    available_max_pos.extend([(x+l-letter_size,y+l-letter_size),(x,y+l-letter_size)])
                if y-l+letter_size>=0:
                    available_max_pos.append((x,y-l+letter_size))
            if x-l+letter_size>=0:
                available_max_pos.append((x-l+letter_size,y))
                if y+l<=(num_letters)*letter_size:
                    available_max_pos.extend([(x-l+letter_size,y+l-letter_size),(x,y+l-letter_size)])
                if y-l+letter_size>=0:
                    available_max_pos.append((x,y-l+letter_size))
            ok_max_pos=[]
            for max_pos in available_max_pos:
                if is_doable(word,initial_pos,max_pos,letter_size,filled_positions):
                    ok_max_pos.append(max_pos)
            if ok_max_pos:
                max_pos=random.choice(ok_max_pos)
                x1=max_pos[0]
                y1=max_pos[1]
                if x1>x:
                    if y1>y:
                        pos_word=[(x+letter_size*i,y+letter_size*i) for i in range(l1)]
                    elif y1==y:
                        pos_word=[(x+letter_size*i,y) for i in range(l1)]
                    else:
                        pos_word=[(x+letter_size*i,y-letter_size*i) for i in range(l1)]
                elif x1==x:
                    if y1>y:
                        pos_word=[(x,y+letter_size*i) for i in range(l1)]
                    elif y1<y:
                        pos_word=[(x,y-letter_size*i) for i in range(l1)]
                else:
                    if y1>y:
                        pos_word=[(x-letter_size*i,y+letter_size*i) for i in range(l1)]
                    elif y1==y:
                        pos_word=[(x-letter_size*i,y) for i in range(l1)]
                    else:
                        pos_word=[(x-letter_size*i,y-letter_size*i) for i in range(l1)]
                pos_words[word]=pos_word
                for i in range(l1):
                    filled_positions.append(pos_word[i])
                    pos_to_letter[pos_word[i]]=word[i].upper()
                set_pos=False
    return pos_words

def is_doable(word,initial_pos,max_pos,letter_size,filled_positions):
    x1=max_pos[0]
    y1=max_pos[1]
    x=initial_pos[0]
    y=initial_pos[1]
    l1=len(word)
    if x1>x:
        if y1>y:
            pos_word=[(x+letter_size*i,y+letter_size*i) for i in range(l1)]
        elif y1==y:
            pos_word=[(x+letter_size*i,y) for i in range(l1)]
        else:
            pos_word=[(x+letter_size*i,y-letter_size*i) for i in range(l1)]
    elif x1==x:
        if y1>y:
            pos_word=[(x,y+letter_size*i) for i in range(l1)]
        elif y1<y:
            pos_word=[(x,y-letter_size*i) for i in range(l1)]
    else:
        if y1>y:
            pos_word=[(x-letter_size*i,y+letter_size*i) for i in range(l1)]
        elif y1==y:
            pos_word=[(x-letter_size*i,y) for i in range(l1)]
        else:
            pos_word=[(x-letter_size*i,y-letter_size*i) for i in range(l1)]
    for elem in pos_word:
        if elem in filled_positions:
            return False
    return True
            
def fill_unoccupied_positions(available_pos,filled_positions):
    letters='QWERTYUIOPLKJHGFDSAZXCVBNM'
    for elem in available_pos:
        if elem not in filled_positions:
            r=random.choice(letters)
            text=MYFONT_GRID.render(r,True,BLACK)
            pos_to_letter[elem]=r
            screen.blit(text,elem)

def fill_words(pos_words):
    for word in pos_words:
        for i in range(len(word)):
            label=MYFONT_GRID.render(word[i].upper(),True,BLACK)
            screen.blit(label,pos_words[word][i])

def check_first_letter(pos_words,pos_rect):
    for word in pos_words:
        if pos_rect == pos_words[word][0]:
            return word

#gives need to check for the next letter only
#1-Yes,on right path    2-take random inputs.Stop checking  0-erase and restart
def check_next_letter(pos_rect,pos_words,word,i):
    if pos_rect == pos_words[word][i]:
        return 1
    else:
        return 2

def wordcompleted(word,i):
    if i==len(word):
        return True
    else:
        return False       

def find_rect(current_position,available_pos):
    for elem in available_pos:
        if pygame.Rect(elem,(LETTER_SIZE,LETTER_SIZE)).collidepoint(current_position):
            return elem

def blit_grid_letters(pos_letters):
    for i  in pos_letters:
        label=MYFONT_GRID.render(pos_letters[i],True,BLACK)
        screen.blit(label,i)

def calculate_and_display_score(time,SCORE_FONT):
    score=int(10000-(time*10))
    label=SCORE_FONT.render('Score: '+str(score),True,WHITE)
    pygame.draw.rect(screen,BLACK,((600,540),(200,160)))
    screen.blit(label,(620,540))
    return score

def initialisation():
    pygame.init()

    global LETTER_SIZE,NUM_LETTERS,MYFONT_GRID,MYFONT_WORDS,MYFONT_OUT,WIDTH,HEIGHT,GRID_WIDTH,GRID_HEIGHT,TIME_FONT,SCORE_FONT
    LETTER_SIZE=40
    NUM_LETTERS=15
    MYFONT_GRID=pygame.font.SysFont('comicsansms',LETTER_SIZE-10)
    MYFONT_WORDS=pygame.font.SysFont('comicsansms',LETTER_SIZE-12)
    MYFONT_OUT=pygame.font.SysFont(None,LETTER_SIZE-10)
    TIME_FONT=pygame.font.SysFont('comicsanms',28)
    SCORE_FONT=pygame.font.SysFont('monospace',30)
    WIDTH=850
    HEIGHT=600
    GRID_WIDTH=600
    GRID_HEIGHT=600

    global BLACK,WHITE,RED,pos_to_letter,ORANGE,score
    BLACK=(0,0,0)
    WHITE=(255,255,255)
    RED=(148,0,0,255)
    ORANGE=(255,99,71)
    GREEN=(0,148,47)
    pos_to_letter={}
    score=0

    global words,available_pos,pos_words
    words=gen_words()
    available_pos=available_positions(NUM_LETTERS,LETTER_SIZE)
    pos_words=find_word_position(words,available_pos,LETTER_SIZE,NUM_LETTERS)

    global screen
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    screen.fill(BLACK)
    pygame.draw.rect(screen,WHITE,(0,0,GRID_WIDTH,GRID_HEIGHT))
    fill_words(pos_words)
    fill_unoccupied_positions(available_pos,filled_positions)
    pygame.display.update()

    global pos_words_to_find
    pos_words_to_find={}

    #sort the positions according to row  and  column
    pos_list1=sorted(pos_to_letter)
    global pos_letters
    pos_letters={}
    for elem in pos_list1:
        pos_letters[elem]=pos_to_letter[elem]

    pygame.draw.rect(screen,GREEN,(GRID_WIDTH+60,100,130,400))
    
    global words_to_find
    words_to_find=list(pos_words)
    for t in range(10):
        pos_to_blit=(GRID_WIDTH+65,100+40*t)
        word_to_blit=MYFONT_WORDS.render(words_to_find[t],True,BLACK)
        screen.blit(word_to_blit,pos_to_blit)
        pos_words_to_find[words_to_find[t]]=pos_to_blit
    pygame.display.update()

def display_time(previous_game_time):
    time=pygame.time.get_ticks()//1000-previous_game_time
    timestamp=TIME_FONT.render('Elapsed time: '+str(time),True,BLACK)
    pygame.draw.rect(screen,ORANGE,((645,20),(170,30)))
    screen.blit(timestamp,(645,20))
    pygame.display.update()
    return time


def main():
    pygame.init()
    previous_game_time=pygame.time.get_ticks()//1000
    initialisation()
    print(pos_words)
    Game_Over=False
    count=0
    i=0
    completed_words=[]
    while not Game_Over:
        pygame.time.Clock().tick(10)
        time=display_time(previous_game_time)
        score=calculate_and_display_score(time,SCORE_FONT)
        for event in pygame.event.get():
            #print(event)
            if event.type==pygame.QUIT:
                Game_Over=True
            if event.type==pygame.MOUSEBUTTONDOWN:
                #print(pygame.mouse.get_pressed())
                if  pygame.mouse.get_pressed()[2]:
                    pygame.draw.rect(screen,WHITE,(0,0,GRID_WIDTH,GRID_HEIGHT))
                    for elem in completed_words:
                        for position in elem[1]:
                            pygame.draw.rect(screen,RED,(position,(LETTER_SIZE,LETTER_SIZE)))
                    blit_grid_letters(pos_letters)
                    i=0
                    count=0
                if pygame.mouse.get_pressed()[0]:
                    pos_mouse=pygame.mouse.get_pos()
                    pos_rect=find_rect(pos_mouse,available_pos)
                    pygame.draw.rect(screen,RED,(pos_rect,(LETTER_SIZE,LETTER_SIZE)))
                    blit_grid_letters(pos_letters)
                    count+=1
                    if count==1:
                        word=check_first_letter(pos_words,pos_rect)
                    if word:
                        result=check_next_letter(pos_rect,pos_words,word,i)
                        if result==1:
                            i=i+1
                            if wordcompleted(word,i):
                                count=0
                                i=0
                                completed_words.append((word,pos_words[word]))
                                pygame.draw.line(screen,BLACK,(pos_words_to_find[word][0]-25,pos_words_to_find[word][1]+23),(pos_words_to_find[word][0]+145,pos_words_to_find[word][1]+23),5)
                                del pos_words[word]
                        elif result==2:
                            word=None
                pygame.display.update()        
            l=len(completed_words)
            
            #close condition
            while l==10:
                Game_Over = True
                NEW_WIDTH=500
                NEW_HEIGHT=300
                out_screen=pygame.display.set_mode((NEW_WIDTH,NEW_HEIGHT))
                out_screen.fill(ORANGE)
                
                #blit required text onto 2nd  screen
                text=MYFONT_OUT.render("Yay!You found the words",True,BLACK)
                out_screen.blit(text,(130,50))
                label=SCORE_FONT.render('Your score: '+str(score),True,BLACK)
                screen.blit(label,(106,90))
                text=MYFONT_OUT.render("Do you wish to play another game?",True,BLACK)
                out_screen.blit(text,(78,150))
                text=MYFONT_OUT.render("Yes",True,BLACK)
                yes_pos=(108,200)
                out_screen.blit(text,yes_pos)
                no_pos=(362,200)
                text=MYFONT_OUT.render("NO",True,BLACK)
                out_screen.blit(text,no_pos)


                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        sys.exit()
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos=pygame.mouse.get_pos()
                        if pygame.Rect(yes_pos,(34,21)).collidepoint(mouse_pos):                    
                            main()
                        if pygame.Rect(no_pos,(26,21)).collidepoint(mouse_pos):
                            l=0
                    pygame.display.update()




main()


            

                