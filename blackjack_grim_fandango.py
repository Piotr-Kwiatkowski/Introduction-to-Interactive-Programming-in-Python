#link: http://www.codeskulptor.org/#user39_hhiV1xKZik_21.py

""" Blackjack -- Grim Fandango Edition

    Piotr Kwiatkowski, April 2015 """

""" TODO:
    - komunikat o wycofaniu sie (DEAL za wczesnie) lub zablokowanie opcji
    - przyciski na ekranie zamiast buttonow
    - przyjmowanie zakladow 
    - przycisk na ekranie/button exit
    - poprawic tablice wynikow
    - losowanie kart co sekunde(?)
    - ladniejsze ulozenie kart
    - "place your bets" co 3. gre?
"""

try:
    import simplegui
    import random
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    import SimpleGUICS2Pygame.random as random

# load sounds
win = simplegui.load_sound("https://www.dropbox.com/s/bd6p507a9hy6wdb/invitation-crowdcheer.wav?dl=1")
win.set_volume(0.1)

whitenoise = simplegui.load_sound("https://www.dropbox.com/s/q0h3atoluixwy0y/whitenoise.mp3?dl=1")
whitenoise.set_volume(0.3)

lounge = simplegui.load_sound("https://www.dropbox.com/s/fg2rzxov16t3x9u/lounge.mp3?dl=1")
lounge.set_volume(0.3)

lost = simplegui.load_sound("https://www.dropbox.com/s/vgj06gf2y0zswmf/playerloses.wav?dl=1")
lost.set_volume(0.1)

bets_long = simplegui.load_sound("https://www.dropbox.com/s/ww8infjuee60kz8/placeyourbets-long.wav?dl=1")
bets_long.set_volume(0.2)

seventeen = simplegui.load_sound("https://www.dropbox.com/s/t03lmix5qmoz6ra/17.wav?dl=1")
seventeen.set_volume(0.2)

eighteen = simplegui.load_sound("https://www.dropbox.com/s/l1uks7hd6n2k1oq/18.wav?dl=1")
eighteen.set_volume(0.2)

nineteen = simplegui.load_sound("https://www.dropbox.com/s/dzxmpf3hk71zhk6/19.wav?dl=1")
nineteen.set_volume(0.2)

twenty = simplegui.load_sound("https://www.dropbox.com/s/9n7agieuqv5oabo/20.wav?dl=1")
twenty.set_volume(0.2)

twentyone = simplegui.load_sound("https://www.dropbox.com/s/qrw88wzwh461my6/21.wav?dl=1")
twentyone.set_volume(0.2)

goodnews = simplegui.load_sound("https://www.dropbox.com/s/fbsq8whoaxyx3tg/por%20favor%2C%20tell%20me%20some%20good%20news%2C%20why%20don%27t%20cha.wav?dl=1")
goodnews.set_volume(0.2)

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

bg_img = simplegui.load_image("https://www.dropbox.com/s/mce0na8pwvaynwm/goddamn.jpg?dl=1")
bg_img_center = (300, 300)
bg_img_size = (600, 600)

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
lounge_time = 0
whitenoise_time = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []

    def __str__(self):
        final_str = "= "
        for card in self.card_list:
            final_str += card.get_suit() + card.get_rank() + " "
        return final_str

    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        final_value = 0
        aces_present = False
        for card in self.card_list:
            final_value += VALUES[card.get_rank()] 
            if card.get_rank() == 'A':
                aces_present = True
                
        if aces_present and final_value + 10 <= 21:
            final_value += 10
        return final_value
   
    def draw(self, canvas, pos):
        for card in self.card_list:
            card.draw(canvas, [pos[0], pos[1]])
            pos[0] += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards_list = []
        for rank in RANKS:
            for suit in SUITS:
                self.cards_list.append(Card(suit, rank))
        random.shuffle(self.cards_list)

    def shuffle(self):
        random.shuffle(self.cards_list)

    def deal_card(self):
        return self.cards_list.pop()
    
    def __str__(self):
        deck = "Deck contains: "
        for card in self.cards_list:
            deck += str(card) + " "
        return deck

#define event handlers for buttons
def deal():
    global deck, outcome, in_play, player_hand, dealer_hand, score
    if outcome == "" and in_play == True:
        score -= 1
    outcome = ""
    if not score:
        bets_long.play()
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    in_play = True

def hit():
    global in_play, player_hand, dealer_hand, deck, outcome, score
    if in_play == True and outcome == "":
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21 :
            in_play = False
            outcome = "You have busted"
            lost.play()
            goodnews.play()
            score -= 1
    elif outcome == "":
        if dealer_hand.get_value() <= 21:
            dealer_hand.add_card(deck.deal_card())
    
def stand():
    global outcome, dealer_hand, in_play, score
    if outcome == "You have busted":
        pass
#        print outcome + " (already busted)"
    elif outcome == "":
        while dealer_hand.get_value() < 17:
            in_play = False
            hit()
        if dealer_hand.get_value() < player_hand.get_value() or dealer_hand.get_value() > 21:
            outcome = "You won!"
            # TU BEDZIE PETLA
            if player_hand.get_value() == 21:
                twentyone.play()
            elif player_hand.get_value() == 20:
                twenty.play()
            elif player_hand.get_value() == 19:   
                nineteen.play()
            elif player_hand.get_value() == 18:
                eighteen.play()
            elif player_hand.get_value() == 17:
                seventeen.play()
                
            win.play()
            score += 1
            in_play = False
        else:
            outcome = "You lost"
            lost.play()
            score -= 1
            in_play = False

# draw handler    
def draw(canvas):
    canvas.draw_image(bg_img, bg_img_center, bg_img_size, bg_img_center, bg_img_size)
#    canvas.draw_text('BLACKJACK', [30, 60], 50, 'White', 'monospace')
    canvas.draw_text('    Grim Fandango Edition', [30, 73], 15, 'White', 'monospace')
    canvas.draw_text('Dealer:', [30, 200], 24, 'White', 'monospace')
    canvas.draw_text('Player:', [30, 410], 24, 'White', 'monospace')
    canvas.draw_text('Your score: ' + str(score), [300, 120], 24, 'White', 'monospace')
    player_pos = [20, 420]
    dealer_pos = [20, 210]
    player_hand.draw(canvas, player_pos)
    dealer_hand.draw(canvas, dealer_pos)
    if outcome == "":
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          (56, 258), CARD_BACK_SIZE)
        canvas.draw_text('Hit or stand?', [200, 410], 24, 'White', 'monospace')
    else:
        canvas.draw_text(outcome, [30, 370], 50, 'Red', 'monospace')
        canvas.draw_text('New deal?', [200, 410], 24, 'White', 'monospace')

def lounge_timer_handler():
    global lounge_time
#    print "lounge_time =", lounge_time
    if lounge_time == 0 or lounge_time == 135:
        lounge.rewind()
        lounge.play()
        lounge_time = 1
    else:
        lounge_time += 1
        

def whitenoise_timer_handler():
    global whitenoise_time
#    print "whitenoise_time =", whitenoise_time
    if whitenoise_time == 0 or whitenoise_time == 104:
        whitenoise.rewind()
        whitenoise.play()
        whitenoise_time = 1
    else:
        whitenoise_time += 1
        
def noise():
    if whitenoise_timer.is_running():
        whitenoise_timer.stop()
        whitenoise.pause()
    else:
        whitenoise_timer.start()
        whitenoise.play()
        
def music():
    if lounge_timer.is_running():
        lounge_timer.stop()
        lounge.pause()
    else:
        lounge_timer.start()
        lounge.play()
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 100)
frame.add_button("Hit",  hit, 100)
frame.add_button("Stand", stand, 100)
frame.add_label("")
frame.add_label("")
frame.add_label("Options:")
frame.add_button("Noise ON/OFF", noise, 150)
frame.add_button("Music ON/OFF", music, 150)
frame.set_draw_handler(draw)

lounge_timer = simplegui.create_timer(1000, lounge_timer_handler)
whitenoise_timer = simplegui.create_timer(1000, whitenoise_timer_handler)

# get things rolling
deal()
lounge_timer.start()
whitenoise_timer.start()
frame.start()
