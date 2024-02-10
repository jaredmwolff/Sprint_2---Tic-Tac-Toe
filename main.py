#======================================================================================================================


# This whole first portion is where the screen/grid is created for the game of Tic Tac Toe. It's a
# long portion that I had to do A LOT of searching for...


import sys

import pygame
from pygame import mixer

pygame.init()
pygame.mixer.init()


Width, Height = 900, 900
Screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Tic Tac Toe")


# Sources:
        # X Image: https://freevector.co/vector-icons/shapes/x-symbol.html
        # O Image: https://iconscout.com/icons/circle
Board = pygame.image.load("Board.png")
X_IMG = pygame.image.load("X_Symbol.png")
O_IMG = pygame.image.load("O_Symbol.png")


# The 3x3 grid, of course
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# A 3-Dimensional List for the X/O Surface, then the X/O Rect [None, None].
graphical_grid = [[[None, None], [None, None], [None, None]],
                    [[None, None], [None, None], [None, None]],
                    [[None, None], [None, None], [None, None]]]


# Sources:
        # click_sfx: https://www.youtube.com/watch?v=hoKKbVbCCxE
        # win_sfx: https://www.youtube.com/watch?v=wqVw8sGjnkI
click_sfx = pygame.mixer.Sound("click_sfx.mp3")
win_sfx = pygame.mixer.Sound("win_sfx.mp3")

# Editing volume
click_sfx.set_volume(0.1)
win_sfx.set_volume(0.1)


to_move = 'X'
Screen.fill("white")
Screen.blit(Board, (64, 64))
game_finished = False


pygame.display.update()



#======================================================================================================================



# Trying to render the board...
def render_board(grid, X_IMG, O_IMG):
    global graphical_grid

    # i = surface/image
    # j = rect, or where to put the image/surface (which refers to the "i" directly above)

    # The i in range(3) and the j in range(3) in the statements below refers to it being a 3x3 grid
    for i in range(3):
        for j in range(3):

            if grid[i][j] =='X':
                # Create an X image and rect. This first line is the image
                graphical_grid[i][j][0] = X_IMG
                # This one is the rect. Equations are for the ROW and COLUMN
                graphical_grid[i][j][1] = X_IMG.get_rect(center=(j*300+150, i*300+150))

            elif grid[i][j] =='O':
                # Exact same thing as the "if" statement directly above, but with the O_IMG instead
                graphical_grid[i][j][0] = O_IMG
                graphical_grid[i][j][1] = O_IMG.get_rect(center=(j*300+150, i*300+150))



#======================================================================================================================



# Trying to get the mouse to work in the code. Oh boy...
def add_XO(grid, graphical_grid, to_move):
    current_pos = pygame.mouse.get_pos()

    # Black magic wizardry that centers the X and/or the O and scales it somehow
    converted_x = (current_pos[0]-65)/835*2
    converted_y = (current_pos[1])/835*2

    # Showcases who's turn it is to move
    if grid[round(converted_y)][round(converted_x)] != 'O' and grid[round(converted_y)][round(converted_x)] != 'X':
        grid[round(converted_y)][round(converted_x)] = to_move

        if to_move == 'O':
            to_move ='X'
        else:
            to_move ='O'

    # Function to, of coarse, render the board from the earlier class above
    render_board(grid, X_IMG, O_IMG)

    for i in range(3):
        for j in range(3):
            # Allows us to place either an X or and O down in a square, depending on who's turn it is
            if graphical_grid[i][j][0] is not None:
                Screen.blit(graphical_grid[i][j][0], graphical_grid[i][j][1])

    return grid, to_move



#======================================================================================================================


# Checks to see if either player has won the game

# And HOLY CRAP, this portion was massively confusing. I can't tell if the person helping me was really good at this
# or if he was overcomplicating things to the max in an attempt to sound smart. Regardless, I THINK I understood it
def check_win(grid):

    winner = None

    # Recognizes the winner for a Row
    for row in range(0, 3):
        if((grid[row][0] == grid[row][1] == grid[row][2]) and (grid [row][0] is not None)):
            winner = grid[row][0]
            for i in range(0, 3):
                Screen.blit(graphical_grid[row][i][0], graphical_grid[row][i][1])
            pygame.display.update()
            return winner

    # Recognizes the winner for a Column
    for col in range(0, 3):
        if((grid[0][col] == grid[1][col] == grid[2][col]) and (grid[0][col] is not None)):
            winner =  grid[0][col]
            for i in range(0, 3):
                Screen.blit(graphical_grid[i][col][0], graphical_grid[i][col][1])
            pygame.display.update()
            return winner

    # Recognizes the winner for one Diagonal Line
    if (grid[0][0] == grid[1][1] == grid[2][2]) and (grid[0][0] is not None):
        winner =  grid[0][0]
        Screen.blit(graphical_grid[0][0][0], graphical_grid[0][0][1])
        Screen.blit(graphical_grid[1][1][0], graphical_grid[1][1][1])
        Screen.blit(graphical_grid[2][2][0], graphical_grid[2][2][1])
        pygame.display.update()
        return winner

    # Recognizes the winner for on the other Diagonal Line
    if (grid[0][2] == grid[1][1] == grid[2][0]) and (grid[0][2] is not None):
        winner =  grid[0][2]
        Screen.blit(graphical_grid[0][2][0], graphical_grid[0][2][1])
        Screen.blit(graphical_grid[1][1][0], graphical_grid[1][1][1])
        Screen.blit(graphical_grid[2][0][0], graphical_grid[2][0][1])
        pygame.display.update()
        return winner

    # Recognizes if there is NO winner
    if winner is None:
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 'X' and grid[i][j] != 'O':
                    return None
        return "DRAW"


#======================================================================================================================



#Ending the game/code
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # There is a bit of a delay with the audio when playing the game, BUT it still works!
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid, to_move = add_XO(grid, graphical_grid, to_move)
            click_sfx.play()

            # Copy/Paste from the very first class in the code, indicating a reset
            if game_finished:
                grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                graphical_grid = [[[None, None], [None, None], [None, None]],
                                    [[None, None], [None, None], [None, None]],
                                    [[None, None], [None, None], [None, None]]]

                to_move = 'X'
                Screen.fill("white")
                Screen.blit(Board, (64, 64))
                game_finished = False

                pygame.display.update()
            
        # Audio comes out weird here as well, BUT it's working here as well
        if check_win(grid) is not None:
            game_finished = True
            win_sfx.play()

        pygame.display.update()


#======================================================================================================================


