# ==============================================================================
"""CRAWL : play a variant of the 'Card Crawl' games"""
# ==============================================================================
__author__  = "Alexandra Millot"
__version__ = "3.0"
__date__    = "2022-12-29"
# ==============================================================================
from ezTK import *
from random import shuffle, randrange as rr
# ------------------------------------------------------------------------------
class Crawl_Game(object):
  """kernel class for the 'Card Crawl' game"""
  def __init__(self):
    """build initial grid and deck"""
    # build grid as a symbolic representation for the game board
    # grid is defined col by col, from left to right, using 4 items per col :
    # text for upper card, states for upper/lower cards, text for lower card
    self.health = 10
    self.money = 0
    self.grid = [['', 0, 10, str(self.money) + ' ♦'], ['', 0, 1, ''], ['', 0, 11, str(self.health) + ' ❤'],
                 ['', 0, 21, ''], ['', 0, 20, '']] # set initial grid
    # build deck by adding twice each 'potion/sword/shield/monster' card and
    # adding 4 times each 'coin' card, then shuffle whole deck (= 48 cards)
    self.deck = [(10*row + col, 3*row + rr(1,4)) for col in (3,3,4,5,6,7,8,9)
      for row in range(3) for n in range(2)];
    shuffle(self.deck)
    #dict = { "coin" : [3,13,23], "potion" : [4, 14, 24], "sword" : [5, 15, 25], "shield" : [6, 16, 26], "monster" : [7, 17, 27, 8, 18, 28, 9, 19, 29] }
    self.coin = [(3,1), (3, 2), (3, 3), (13, 4), (13, 5), (13, 6), (23, 7), (23, 8), (23, 9)]
    self.potion = [(4,1), (4, 2), (4, 3), (4,4), (14, 4), (14,5), (14, 6), (24, 7), (24, 8), (24, 9)]
    self.sword = [(5, 1), (5, 2), (5, 3), (5,4), (15, 4), (15,5), (15, 6), (25, 7), (25, 8), (25, 9)]
    self.shield = [(6,1), (6, 2), (6, 3), (6,4), (16, 4), (16, 5), (16, 6), (26, 7), (26, 8), (26, 9)]
    monstre = [7, 17, 27, 8, 18, 28, 9, 19, 29]
    self.monster = []
    i = 1
    while i < 10 :
      for item in monstre:
        self.monster.append((item, i))
      i = i + 1
    self.vide = [1, 20, 21]
    self.defense = self.sword + self.shield
    self.nonmonster = self.potion + self.coin + self.sword + self.shield 

  def add_money(self, text):
    """Rajouter les points de pièce au compter money"""
    self.money = self.money + text

  def add_health(self, text):
    """Rajouter les points de vie au compter health"""
    self.health = self.health + text
    
  def attack(self, text, defense):
    """Contient les changements implicant une attaque"""
    
    if defense == 0 :                     # Si il n'y a pas de bouclier ou d'armure 
      if self.health > text :
        self.health = self.health - text
      else :
        self.health = 0
        print('*** VOUS AVEZ PERDU ***')
    else :                                # Si il y a un bouclier ou une armure
      if defense > text :                 # Si la défense est plus forte que l'attaque 
        defense = defense - text          # Perte de point pour la défense
      else :                              # Si l'attaque est plus forte que la défense
        text = text - defense             # Le monstre s'affaiblie  
        defense = 0                       # La défense est détruite = 0
        
      
# ------------------------------------------------------------------------------
class Crawl_Win(Win):
  """interface class for the 'Card Crawl' game"""
  click = None
  game = None
  
  def __init__(self):
    """build initial window setup"""
    global game
    Win.__init__(self, title='CRAWL', op=2, bg='#000', click=self.on_click)
    font1, font2 = 'Arial 18 bold', 'Arial 30 bold'
    images = ImageGrid('crawl.png', rows=3, cols=10) # load grid of cards
    game = Crawl_Game() # create instance for kernel class
    grid, deck = game.grid, game.deck # get attributes from kernel class
    # --------------------------------------------------------------------------
    ### Choix du personnage (Voir E5C_win.py pour une page de configuration) ###
    game.grid[2][2] = int(input("Select your Player (between 2, 12 or 22) : "))
    # --------------------------------------------------------------------------
    board = Frame(self, font=font1, fg='#FFF', fold=4, flow='SE')
    for loop in range(20): # loop over board cells
      row, col = loop % 4, loop // 4 # get coordinates for current board cell
      cell = grid[col][row] # get text or state for current cell from grid
      if row in (0,3): Label(board, text=cell) # set text for current card
      else: Label(board, image=images, state=cell) # set image for current card
    # --------------------------------------------------------------------------
    board[0][1].config(text=len(deck), compound='center', font=font2)
    self.game, self.board = game, board; self.loop()
  # ----------------------------------------------------------------------------
  def on_click(self, widget, code, mods, ):
    """generic callback for all mouse click events"""
    global click
    board, deck = self.board, self.game.deck # set local aliases

    if widget.master != self.board or widget.index != (0,1):

      ### LES 4 CARTES DE LA PIOCHE ###
      if widget.index == (1,1) or widget.index == (2,1) or widget.index == (3,1) or widget.index == (4,1) :
        state, text = board[widget.index[0]][1].state, board[widget.index[0]][0]['text']
        click = [state, text, widget.index]
        print(click)

      ### RECYCLAGE ### 
      elif widget.index == (0,2) :
        if click == [] :
          return
        for item in game.monster :          # Si la carte est un monstre il ne se passe rien 
          if tuple(click[:2]) == item :
            return

          
        ###  Version originale du jeu ###
          
##        print('vous recyclez une carte')    # Si la carte n'est pas un monstre elle retourne dans la pioche 
##        deck.append(tuple(click[:2]))
##        shuffle(deck)
##        board[0][1]['text'] = len(deck)
##        position = click[2]
##        if position == (4,2) :
##          board[position[0]][position[1]].state = 20
##          board[position[0]][position[1]+1]['text'] = ''
##          del click[:]
##          if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 :
##              print('Vous avez gagnez')
##        else :
##          board[position[0]][position[1]].state = 0
##          board[position[0]][position[1]-1]['text'] = ''
##          del click[:]
##          if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 :
##              print('Vous avez gagnez')
##        return

          
        ### Version demander pour le projet ###
        
        sanscarte = 0
        for i in range(1,5) :
          print(board[i][1].state)
          if board[i][1].state == 0 :
            sanscarte = sanscarte + 1
          else :
            pass
        print('Nombre de case vide :')
        print(sanscarte)
        print('click 1 :')
        print(click[1])
        print(click)
        #print(click[1] in range(4,7) and ((sanscarte in range(0,2)) or (click[3] == (4,2) and sanscarte in range(0,3))))
        #print(click[1] in range(1,4)) and ((sanscarte in range(0,3)) or (click[3] == (4,2) and sanscarte in range(0,4)))
        if (click[1] in range(1,4) and sanscarte in range(0,3)) or (click[1] in range(1,4) and click[2] == (4,2) and sanscarte in range(0,4)) :  # Si la carte est de force 1, 2 ou 3 elle l'échange 1 carte au hasard de la zone de jeu avec les cartes restantes
          cards = [deck.pop() for n in range(1)]
          print('carte recyclé <=> 1 carte échangée')
          print(cards)
          cards = tuple(cards)
          print(cards)
          card = cards[0]
          print(card)
          deck.append(card)
          shuffle(deck)
          i = 0
          value = 0
          while i == 0 :
            value = rr(1,5)
            print(value)
            if board[value][1].state == 0 or (value == click[2][0] and  not click[2] ==(4,2))  :
              print('le hasard fait mal les choses')
            else :
              i = i + 1
          print(value)
          state, text = cards[0][0], cards[0][1]
          board[value][0]['text'] = text # change card text on board
          board[value][1].state = state # change card image on board
          board[0][1]['text'] = len(deck) # update counter of remaining cards      
          print('vous recyclez une carte')
          position = click[2]
          if position == (4,2) :
              board[position[0]][position[1]].state = 20
              board[position[0]][position[1]+1]['text'] = ''
          else :
              board[position[0]][position[1]].state = 0
              board[position[0]][position[1]-1]['text'] = ''
          del click[:]
        elif (click[1] in range(4,7) and sanscarte in range(0,2)) or (click[1] in range(4,7) and click[2] == (4,2) and sanscarte in range(0,3)) :   # Si la carte est de force 4, 5 ou 6 elle l'échange 2 cartes au hasard de la zone de jeu avec les cartes restantes
          cards = [deck.pop() for n in range(2)]
          print(cards)
          deck.extend(cards)
          print(deck)
          shuffle(deck)
          print('carte recyclé <=> 2 carte échangée')
          i = 0
          value = []
          while i != 2 :
            random = rr(1,5)
            print('Carte au hasard :')
            print(random)
            print(click[2][0])
            if (board[random][1].state != 0 and random != click[2][0]) or (board[random][1].state != 0 and click[2] == (4,2)) :
              p = 0
              print('cool')
              print(value)
              for item in value :
                if random == item :
                  print(random)
                  print('le hasard fait mal les choses (2)')
                  p = p + 1
              print('Valeur de p, si elle est = 0 on valide le chiffre')
              print(p)
              if p == 0 :
                i = i + 1
                value.append(random)
                
          print('position des cartes à échanger :')
          print(value)
          state, text = [cards[0][0], cards[1][0]],[cards[0][1], cards[1][1]]
          board[value[0]][0]['text'] = text[0] # change card text on board
          board[value[1]][0]['text'] = text[1] # change card text on board
          board[value[0]][1].state = state[0] # change card text on board
          board[value[1]][1].state = state[1] # change card text on board
          board[0][1]['text'] = len(deck) # update counter of remaining cards     
          print('vous recyclez une carte')
          position = click[2]
          if position == (4,2) :
            board[position[0]][position[1]].state = 20
            board[position[0]][position[1]+1]['text'] = ''
          else :
            board[position[0]][position[1]].state = 0
            board[position[0]][position[1]-1]['text'] = ''
          del click[:]
        elif (click[1] in range(7,10) and sanscarte == 0) or (click[1] in range(7,10) and click[2] == (4,2) and sanscarte in range(0,2)) :    # Si la carte est de force 7, 8 ou 9 elle l'échange 3 cartes au hasard de la zone de jeu avec les cartes restantes
          cards = [deck.pop() for n in range(3)]
          print('carte recyclé <=> 3 carte échangée')
          print(cards)
          deck.extend(cards)
          print(deck)
          shuffle(deck)
          i = 0
          value = []
          while i != 3 :
            random = rr(1,5)
            print('Carte au hasard :')
            print(random)
            if (board[random][1].state != 0 and random != click[2][0]) or (board[random][1].state != 0 and click[2] == (4,2)) :
              p = 0
              for item in value :
                if random == item :
                  print(random)
                  print('le hasard fait mal les choses (2)')
                  p = p + 1
              print('Valeur de p, si elle est = 0 on valide le chiffre')
              print(p)
              if p == 0 :
                i = i + 1
                value.append(random)
          print('position des cartes à échanger :')
          print(value)
          state, text = [cards[0][0], cards[1][0], cards[2][0]],[cards[0][1], cards[1][1], cards[2][1]]
          board[value[0]][0]['text'] = text[0] # change card text on board
          board[value[1]][0]['text'] = text[1] # change card text on board
          board[value[2]][0]['text'] = text[2] # change card text on board
          board[value[0]][1].state = state[0] # change card text on board
          board[value[1]][1].state = state[1] # change card text on board
          board[value[2]][1].state = state[2] # change card text on board
          board[0][1]['text'] = len(deck) # update counter of remaining cards     

          position = click[2]
          if position == (4,2) :
            board[position[0]][position[1]].state = 20
            board[position[0]][position[1]+1]['text'] = ''
          else :
            board[position[0]][position[1]].state = 0
            board[position[0]][position[1]-1]['text'] = ''
          del click[:]
        else :
          print('le recyclage est impossible')
            
      ### SAC ###    
      elif widget.index == (4,2) :
        state, text = board[4][2].state, board[4][3]['text']
        print('sélection du sac')
        for item in game.vide :
          if state == item:             # Si la main est vide
            print('le sac est vide')
          
            for item in game.nonmonster :          # Si mon premier click comprenait tout sauf un monstre
              if tuple(click[:2]) == item :
                print('vous avez pré-sélectionné une carte différente du monstre')
                board[4][2].state = click[0]
                board[4][3]['text'] = click[1]
                position = click[2]
                board[position[0]][position[1]].state = 0
                board[position[0]][position[1]-1]['text'] = ''
        if state != 20 :
          click = [state, text, widget.index]

      ### MAINS ###     
      elif widget.index == (3,2) or widget.index == (1,2) :
        state, text = board[widget.index[0]][2].state, board[widget.index[0]][3]['text']
        print('sélection de la main')
        print(state)
        
        if (widget.index == (3,2) and state != 21) or (widget.index == (1,2) and state != 1):          # Si la main est occupée
            print('la main est occupée')
            for item in game.monster :          # Si mon premier click comprenait un monstre
                if tuple(click[:2]) == item :
                  print(type(text), text)
                  game.attack(click[1],text)
                  degat = text - click[1]
                  position = click[2]
                  if degat > 0 :                # dégat positif le bouclier reste en étant impacté OK
                    print("dégat positif le bouclier reste en étant impacté")
                    board[widget.index[0]][3]['text'] = degat
                    board[position[0]][position[1]].state = 0
                    board[position[0]][position[1]-1]['text'] = ''
                  else :                        # dégat négatif ou nul le bouclier disparaît et le niveau de vie peut être impacté
                    print("dégat est négatif ou nul le bouclier disparaît et le niveau de vie peut être impacté")
                    if widget.index == (3,2) : 
                      board[widget.index[0]][2].state = 21
                    else :
                      board[widget.index[0]][2].state = 1
                    board[widget.index[0]][3]['text'] = ''
                    board[position[0]][position[1]-1]['text'] = click[1] - text
                    if click[1] - text == 0 :
                      board[position[0]][position[1]].state = 0
                      board[position[0]][position[1]-1]['text'] = ''
                  del click[:]
                  if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 and game.health != 0 :
                      print('*** VOUS AVEZ GAGNEZ***')
                else : pass      
        else : pass
        
        for item in game.vide :
          if state == item:             # Si la main est vide
            print('la main est vide')

            for item in game.defense :          # Si mon premier click comprenait une épée ou un bouclier
              if tuple(click[:2]) == item :
                print('vous avez pré-sélectionné une épée')
                board[widget.index[0]][2].state = click[0]
                board[widget.index[0]][3]['text'] = click[1]
                position = click[2]
                if position == (4,2) :
                  board[position[0]][position[1]].state = 20
                  board[position[0]][position[1]+1]['text'] = ''
                  del click[:]
                  if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 and game.health != 0 :
                      print('*** VOUS AVEZ GAGNEZ***')
                else :
                  board[position[0]][position[1]].state = 0
                  board[position[0]][position[1]-1]['text'] = ''
                  del click[:]
                  if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 and game.health != 0 :
                      print('*** VOUS AVEZ GAGNEZ***')

            for item in game.coin :          # Si mon premier click comprenait une pièce
              if tuple(click[:2]) == item :
                print('vous avez pré-sélectionné une pièce')
                game.add_money(click[1])
                board[0][3]['text'] = str(game.money) + ' ♦'
                position = click[2]
                if position == (4,2) :
                  board[position[0]][position[1]].state = 20
                  board[position[0]][position[1]+1]['text'] = ''
                  del click[:] 
                else :
                  board[position[0]][position[1]].state = 0
                  board[position[0]][position[1]-1]['text'] = ''
                  del click[:]
                if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 and game.health != 0 :
                  print('*** VOUS AVEZ GAGNEZ***')

            for item in game.potion :          # Si mon premier click comprenait une potion
              if tuple(click[:2]) == item :
                if game.health + item[1] <= 10 :
                  print('vous avez pré-sélectionné une potion')
                  game.add_health(click[1])
                  print(game.health)
                  board[2][3]['text'] = str(game.health) + ' ❤'
                  position = click[2]
                  if position == (4,2) :
                    board[position[0]][position[1]].state = 20
                    board[position[0]][position[1]+1]['text'] = ''
                    del click[:]
                  else :
                    board[position[0]][position[1]].state = 0
                    board[position[0]][position[1]-1]['text'] = ''
                    del click[:]
                if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 and game.health != 0 :
                  print('*** VOUS AVEZ GAGNEZ***')
                else :
                  print("Vous ne pouvez pas dépasser 10 points de vie")

            for item in game.monster :          # Si mon premier click comprenait un monstre
              if tuple(click[:2]) == item :
                print('vous avez pré-sélectionné un monster')
                game.attack(click[1], 0)
                board[2][3]['text'] = str(game.health) + ' ❤'
                position = click[2]
                board[position[0]][position[1]].state = 0
                board[position[0]][position[1]-1]['text'] = ''
                del click[:]
                if len(deck) == 0 and board[1][1].state == 0 and board[2][1].state == 0 and board[3][1].state == 0 and board[4][1].state == 0 and game.health != 0 :
                  print('*** VOUS AVEZ GAGNEZ***')
      return    

    ### PIOCHE ###  
    if len(deck) == 0: # no more card in deck     Si la pioche est vide
        print('la pioche est vide')
        return
    #  self.game = Crawl_Game(); deck = self.game.deck # build a new deck
    i = [(board[1][1].state), (board[2][1].state), (board[3][1].state) , (board[4][1].state)]
    print(i)
    carte = 0
    for item in i :
      if item == 0 :
        carte = carte + 1
    print(carte) # Nombre de carte vide
    print(len(deck))
    
    if carte == 4 and len(deck) >=4 :
      cards = [deck.pop() for n in range(4)] # draw 4 cards from deck
      print('distribution de 4 nouvelles cartes')
      print(cards)
      for n in range(4): # loop over drawn cards
        state, text = cards[n][0], cards[n][1] # get parameters for current card
        board[n+1][0]['text'] = text # change card text on board
        board[n+1][1].state = state # change card image on board
      board[0][1]['text'] = len(deck) # update counter of remaining cards
      
    elif carte == 3 and len(deck) >= 3 :
      print(deck)
      cards = [deck.pop() for n in range(3)] # draw 3 cards from deck
      print('distribution de 3 nouvelles cartes')
      print(cards)
      for n in range(1,5) :
        print(n)
        if board[n][1].state == 0 :
          print('emplacement vide')
          card = cards.pop()        # On prend 1 carte des 3 piochés pour la placer
          print(cards)              # sur l'emplacement vide trouvé
          print(card)
          state, text = card[0], card[1]
          board[n][0]['text'] = text # change card text on board
          board[n][1].state = state # change card image on board
        else : pass
          
      board[0][1]['text'] = len(deck) # update counter of remaining cards

    elif (len(deck) < 3 and carte == 3) or (len(deck) < 4 and carte == 4) :
      cards = [deck.pop() for n in range(len(deck))]
      print('distribution des cartes restantes')
      board[0][1]['text'] = len(deck) # update counter of remaining cards
      for n in range(1,5) :
        print(n)
        if board[n][1].state == 0 :
          print('emplacement vide')
          card = cards.pop()        # On prend 1 carte des cartes restant dans la pioche pour la placer
          print(cards)              # sur l'emplacement vide trouvé
          print(card)
          state, text = card[0], card[1]
          board[n][0]['text'] = text # change card text on board
          board[n][1].state = state # change card image on board
          if cards == [] :
            return
        else : pass

# ==============================================================================
if __name__ == "__main__":
  Crawl_Win()
# ==============================================================================
