#!/usr/bin/env python3

import pygame
import random

# Define parameters --------------------------------------------------

# Define the colors
AQUA = (0, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)

# Window size
WEIDTH = 1055
HEIGHT = 700

# Make the deck parameters
figures = ["ace","queen","king","jack"]
simpols = ["_diamonds","_hearts","_clubs","_spades"]
deck = []

# board rectangular
stack_rec = [[91,25,71,96],[167,25,71,96],[40,50,96,71]]
aces_rec = []
aces_start = 310
for i in range(8):
    next_rec = [ aces_start + 90*i, 25, 71, 96]
    aces_rec.append(next_rec)
board_rec = []
board_start = 40
for i in range(10):
    if i >= 5:
        next_rec = [board_start + 90 * i + 90, 140, 71, 96]
    else:
        next_rec = [board_start + 90*i, 140, 71, 96]
    board_rec.append(next_rec)

key_rec = [board_start + 5*90, 140, 71, 96]

# Define Classes ---------------------------------------------------
class Card():
    def __init__(self,fig,simp):
        self.name = '{}{}'.format(simp,fig)
        dir = 'playing_cards/{}.png'.format(self.name)
        self.img = pygame.image.load(dir).convert()
        self.fig = fig
        self.simpol = simp
        if self.fig == str("_clubs") or self.fig == "_spades":
            self.color = "black"
        elif self.fig == "_hearts" or self.fig == "_diamonds":
            self.color = "red"
        else:
            self.color = "error"
        self.num = 0
        if simp == "ace":
            self.num = 1
        if simp == "queen":
            self.num = 12
        if simp == "king":
            self.num = 13
        if simp == "jack":
            self.num = 11
        if self.num == 0:
            self.num = int(simp)

    def next_card(self,next_num,next_color):
        if self.color != next_color and int(self.num) - int(next_num) == -1:
            return True
        elif next_num == 14 and self.num == 13:
            return True
        else:
            return False

    def next_card_ace(self,next_num,next_fig):
        if self.fig == next_fig and int(next_num) - int(self.num) == -1:
            return True
        elif next_num == 0 and self.num == 1:
            return True
        else:
            return False

class Moved_card():

    def __init__(self,deck):
        self.deck = deck

    def drag(self,screen):
        if len(self.deck) > 0:
            pos = pygame.mouse.get_pos()
            x = pos[0] - 35
            y = pos[1] - 15
            for item in self.deck:
                screen.blit(item.img,[x,y])
                y += 27

class Deck():

    def __init__(self,deck,left,top):
        self.deck = deck
        self.top = top
        self.left = left

    def draw(self,screen):
        if len(self.deck) > 0:
            i = 0;
            for card in self.deck:
                screen.blit(card.img,[self.left, self.top + i*27])
                i = i + 1



class Ace_deck(Deck):
    def __init__(self,deck,left,top):
        super().__init__(deck,left,top)

    def check_click(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        if x > self.left and x < self.left + 71 and y > self.top and y < self.top + 96:
            return True
        else:
            return False

    def check_unclick(self,card):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        if x > self.left and x < self.left + 71 and y > self.top and y < self.top + 96:
            if len(self.deck) > 0:
                next_num = self.deck[len(self.deck) - 1].num
                next_fig = self.deck[len(self.deck) - 1].fig
                return card.next_card_ace(next_num,next_fig)
            else:
                return card.next_card_ace(0, "_")
        else:
            return False

    def draw(self,screen):
        if len(self.deck) > 0:
            card = self.deck[len(self.deck)-1]
            screen.blit(card.img, [self.left, self.top])

class Stack_deck2(Deck):
    def __init__(self,deck,left,top):
        super().__init__(deck,left,top)

    def draw(self,screen):
        if len(self.deck) > 0:
            card = self.deck[len(self.deck)-1]
            screen.blit(card.img, [self.left, self.top])

class Stack_deck3(Deck):
    def __init__(self,deck,left,top):
        super().__init__(deck,left,top)

    def draw(self,screen):
        if len(self.deck) > 0:
            card = self.deck[0]
            # i must rotate the image
            rot_img = pygame.transform.rotate(card.img,90)
            screen.blit(rot_img, [self.left, self.top])

class DeckBoard(Deck):

    def __init__(self,deck,left,top):
        super().__init__(deck,left,top)

    def check_unclick(self,card):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        if x > self.left:
            if x < self.left + 71:
                if y > self.top + (len(self.deck) - 1) * 27:
                    if y < self.top + 96 + (len(self.deck) - 1) * 27:
                        if len(self.deck) == 0:
                            return card.next_card(14,"-")
                        else:
                            next_num = self.deck[len(self.deck)-1].num
                            next_color = self.deck[len(self.deck)-1].color
                            return card.next_card(next_num,next_color)
                        return True
        return False

    def check_click(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        if x > self.left:
            if x < self.left + 71:
                if y > self.top:
                    if y < self.top + 96 + (len(self.deck)-1)*27:
                        if len(self.deck) > 0:
                            position = self.get_card()
                            ok = True
                            for i in range(len(self.deck) - position - 1):
                                card1 = self.deck[len(self.deck) - i - 1]
                                card2 = self.deck[len(self.deck) - i - 2]
                                next_color = card2.color
                                next_num = card2.num
                                if card1.next_card(next_num,next_color) == False:
                                    ok = False
                            if ok:
                                moving_deck = self.move(position)
                                return moving_deck, ok
                            else:
                                return [], False
        return [], False

    def get_card(self):
        pos = pygame.mouse.get_pos()
        y = pos[1]
        lenth = len(self.deck)
        for i in range(lenth):
            if y < self.top + 27*(i+1):
                return i
        return lenth - 1

    def move(self,position):
        lenth = len(self.deck)
        moving_deck = []
        for i in range(lenth - position):
            moving_deck.append(self.deck[position])
            self.deck.remove(self.deck[position])
        return moving_deck

    def add_deck(self,added_deck):
        for added_card in added_deck:
            self.deck.append(added_card)

class Key_deck(Deck):
    def __init__(self, deck, left, top):
        dir = 'playing_cards/red.png'
        self.red_img = pygame.image.load(dir).convert()
        dir = 'playing_cards/green.png'
        self.green_img = pygame.image.load(dir).convert()
        super().__init__(deck, left, top)

    def draw(self, screen, key_boolean):
        if len(self.deck) > 0:
            for j in range(len(self.deck)):
                if j == len(self.deck) - 1 and key_boolean:
                    screen.blit(self.green_img, [self.left - 5, self.top - 5 + j * 27])
                else:
                    screen.blit(self.red_img, [self.left - 5, self.top - 5 + j * 27])
            i = 0;
            for card in self.deck:
                screen.blit(card.img, [self.left, self.top + i * 27])
                i = i + 1

    def check_click(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        if x > self.left:
            if x < self.left + 71:
                if y > self.top + (len(self.deck)-1)*27:
                    if y < self.top + (len(self.deck)-1)*27 + 96:
                        next_deck = []
                        next_deck.append(self.deck[len(self.deck) - 1])
                        self.deck.remove(self.deck[len(self.deck) - 1])
                        return next_deck, True
        return [], False

# just draw the board
def draw_the_board(screen):
    for rec in stack_rec:
        pygame.draw.rect(screen, BLACK, rec, 2)
    for rec in aces_rec:
        pygame.draw.rect(screen, BLACK, rec, 2)
    for rec in board_rec:
        pygame.draw.rect(screen, BLACK, rec, 2)
    pygame.draw.rect(screen, BLACK, key_rec, 2)

def click_on_deck():
    x_mouse = pygame.mouse.get_pos()[0]
    y_mouse = pygame.mouse.get_pos()[1]
    x = stack_rec[0][0]
    y = stack_rec[0][1]
    if x_mouse > x and x_mouse < x + 71 and y_mouse > y and y_mouse < y + 96:
        return True

def click_on_stack2():
    x_mouse = pygame.mouse.get_pos()[0]
    y_mouse = pygame.mouse.get_pos()[1]
    x = stack_rec[1][0]
    y = stack_rec[1][1]
    if x_mouse > x and x_mouse < x + 71 and y_mouse > y and y_mouse < y + 96:
        return True

def click_on_stack3():
    x_mouse = pygame.mouse.get_pos()[0]
    y_mouse = pygame.mouse.get_pos()[1]
    x = stack_rec[2][0]
    y = stack_rec[2][1]
    if len(deck) > 0:
        if x_mouse > x and x_mouse < x + 45 and y_mouse > y and y_mouse < y + 71:
            return True
        else:
            return False
    elif len(deck) == 0:
        if x_mouse > x and x_mouse < x + 96 and y_mouse > y and y_mouse < y + 71:
            return True
        else:
            return False

class Button():
    def __init__(self,color,x,y,width,height,text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,screen):
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render(self.text,1,(0,0,0))
        screen.blit(text, (self.x, self.y))

    def check_click(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        if x > self.x and y > self.y and y < self.y + self.height:
            return True
        else:
            return False

def main():

#----  Define the pygame window ----  #
    pygame.init()
    screen = pygame.display.set_mode([WEIDTH, HEIGHT])
    pygame.display.set_caption("Solitaire")
    done = False
    clock = pygame.time.Clock()
    screen.fill((GREEN))
# -----------------------------------#

    # back card img
    back_img = pygame.image.load('playing_cards/back.png').convert()

    # Build the button
    reset = Button(TEAL,900,650,100,100,"RESET")

    # Build the deck!
    for _ in range(2):
        for simp in simpols:
            for fig in figures:
                deck.append(Card(simp,fig))
            for i in range(9):
                deck.append(Card(simp,str(i+2)))
    first_deck = []
    first_deck = deck



# make the decks

    moved_cards = Moved_card([])
    board_deck = []
    aces_deck = []
    key_deck = Key_deck([],key_rec[0],key_rec[1])
    stack_deck2 = Stack_deck2([],stack_rec[1][0],stack_rec[1][1])
    stack_deck3 = Stack_deck3([],stack_rec[2][0],stack_rec[2][1])

    for rec in board_rec:
        deck_test = []
        for _ in range(6):
            random_card = random.choice(deck)
            deck_test.append(random_card)
            deck.remove(random_card)
        board_deck.append(DeckBoard(deck_test, rec[0], rec[1]))

    for _ in range(6):
        random_card = random.choice(deck)
        key_deck.deck.append(random_card)
        deck.remove(random_card)


    for rec in aces_rec:
        new_deck = Ace_deck([],rec[0],rec[1])
        aces_deck.append(new_deck)

    click_on_stack2_boolean = False
    click_on_board_boolean= False
    click_on_aces_boolean = False
    click_on_stack3_boolean = False
    click_on_key_boolean = False
    reset_boolean = False

    while not done:
        # mouse click actions
        for event in pygame.event.get():

            # check to load the stack 3 card
            if len(stack_deck3.deck) == 0 and len(deck) > 0 and len(moved_cards.deck) == 0:
                random_card = random.choice(deck)
                stack_deck3.deck.append(random_card)
                deck.remove(random_card)

            # check for the key...
            key_boolean = False
            last_key_card = key_deck.deck[len(key_deck.deck) - 1]
            if last_key_card.num == 1:
                key_boolean = True
            for ace_deck in aces_deck:
                if len(ace_deck.deck) > 0:
                    ace_card = ace_deck.deck[len(ace_deck.deck) - 1]
                    next_num = ace_card.num
                    next_fig = ace_card.fig
                    if last_key_card.next_card_ace(next_num,next_fig):
                        key_boolean = True

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if reset.check_click():
                    reset_boolean = True
                    print("click")

                for j in range(len(board_deck)):
                    if len(moved_cards.deck) == 0:
                        moved_cards.deck, check = board_deck[j].check_click()
                        if check:
                            click_on_board_boolean = True
                            last_j = j
                check = False

                if key_boolean:
                    if len(moved_cards.deck) == 0:
                        moved_cards.deck, check = key_deck.check_click()
                        if check:
                            click_on_key_boolean = True
                    check = False

                if click_on_deck() and len(deck) > 0:
                    random_card = random.choice(deck)
                    stack_deck2.deck.append(random_card)
                    deck.remove(random_card)

                if click_on_stack2() and len(stack_deck2.deck) > 0:
                    click_on_stack2_boolean = True
                    moved_cards.deck.append(stack_deck2.deck[len(stack_deck2.deck) - 1])
                    stack_deck2.deck.remove(stack_deck2.deck[len(stack_deck2.deck) - 1])

                if click_on_stack3() and len(stack_deck3.deck) > 0:
                    click_on_stack3_boolean = True
                    moved_cards.deck.append(stack_deck3.deck[0])
                    stack_deck3.deck.remove(stack_deck3.deck[0])

                for i in range(len(aces_deck)):
                    if len(aces_deck[i].deck) > 0 and aces_deck[i].check_click():
                        moved_cards.deck.append(aces_deck[i].deck[len(aces_deck[i].deck)-1])
                        aces_deck[i].deck.remove(aces_deck[i].deck[len(aces_deck[i].deck) - 1])
                        click_on_aces_boolean = True
                        last_i = i

            if event.type == pygame.MOUSEBUTTONUP:
                if len(moved_cards.deck) > 0:

                    if not click_on_key_boolean:
                        for j in range(len(board_deck)):
                            if len(moved_cards.deck) > 0:
                                last_card = moved_cards.deck[0]
                                if board_deck[j].check_unclick(last_card):
                                    board_deck[j].add_deck(moved_cards.deck)
                                    moved_cards.deck = []

                    for i in range(len(aces_deck)):
                        if len(moved_cards.deck) == 1:
                            last_card = moved_cards.deck[0]
                            if aces_deck[i].check_unclick(last_card) :
                                aces_deck[i].deck.append(moved_cards.deck[0])
                                moved_cards.deck = []

                    if click_on_aces_boolean and len(moved_cards.deck) == 1:
                        aces_deck[last_i].deck.append(moved_cards.deck[0])
                        moved_cards.deck = []

                    if click_on_stack2_boolean and len(moved_cards.deck) == 1:
                        stack_deck2.deck.append(moved_cards.deck[0])
                        moved_cards.deck = []

                    if click_on_stack3_boolean and len(moved_cards.deck) == 1:
                        stack_deck3.deck.append(moved_cards.deck[0])
                        moved_cards.deck = []

                    if click_on_board_boolean and len(moved_cards.deck) > 0:
                        board_deck[last_j].add_deck(moved_cards.deck)
                        moved_cards.deck = []

                    if click_on_key_boolean and len(moved_cards.deck) == 1:
                        key_deck.deck.append(moved_cards.deck[0])
                        moved_cards.deck = []

                click_on_stack2_boolean = False
                click_on_board_boolean = False
                click_on_aces_boolean = False
                click_on_stack3_boolean = False
                click_on_key_boolean = False

        # clear the screen
        screen.fill((GREEN))

        if reset_boolean:
            break

        # Redrawing
        draw_the_board(screen)
        stack_deck2.draw(screen)
        stack_deck3.draw(screen)
        reset.draw(screen)

        if len(deck) > 0:
            x = stack_rec[0][0]
            y = stack_rec[0][1]
            screen.blit(back_img,[x,y])

        for brd_deck in board_deck:
            brd_deck.draw(screen)

        for ace_deck in aces_deck:
            ace_deck.draw(screen)

        key_deck.draw(screen,key_boolean)

        moved_cards.drag(screen)

        pygame.display.flip()
        clock.tick(20)

    pygame.quit()

    return reset_boolean

if __name__ == '__main__':
    run = True
    while run:
        run = main()


# Effe in the key
# Restart
# you wan at the end
