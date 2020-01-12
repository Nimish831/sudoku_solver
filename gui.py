# Author: Nimish Mishra
# Email: nmishra36@gatech.edu

import pygame
import sudoku_solver as solver
import time

# Initialize the pygame module
pygame.font.init()

# Initialize key variables
rows = 9
cols = 9
width = 540
height = 540
gap = width / 9
fnt = pygame.font.SysFont("comicsans", 40)

# Gets the board position of the user's click
def click(pos):
    if pos[0] < width and pos[1] < height:
        return int(pos[1] // gap), int(pos[0] // gap)
    else:
        return None

# Helper method to format the time
def format_time(seconds):
    sec = seconds % 60
    minute = seconds // 60
    if sec < 10:
        formatted = " " + str(minute) + ":0" + str(sec)
    else:
        formatted = " " + str(minute) + ":" + str(sec)
    return formatted

# Updates the display screen
def update_window(screen, board, curr_time):
    screen.fill((255, 255, 255))

    # Updating time
    text = fnt.render("Time: " + format_time(curr_time), 1, (0, 0, 0))
    screen.blit(text, (540 - 160, 560))

    # Draw grid lines
    for i in range(rows + 1):
        if i % 3 == 0 and i != 0:
            thick = 4
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * gap), (width, i * gap), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * gap, 0), (i * gap, height), thick)

    # Draw each square
    for i in range(rows):
        for j in range(cols):
            x = j * gap
            y = i * gap

            if board.selected_key == (i, j) and board.temp is not None and board.playing_board[i][j] == 0:
                text = fnt.render(str(board.temp), 1, (128, 128, 128))
                screen.blit(text, (x + 5, y + 5))
            elif not (board.playing_board[i][j] == 0):
                text = fnt.render(str(board.playing_board[i][j]), 1, (0, 0, 0))
                screen.blit(text, (x + int(gap / 2 - text.get_width() / 2), y + int(gap / 2 - text.get_height() / 2)))

            if board.selected_key == (i, j):
                pygame.draw.rect(screen, (255, 0, 0), (x, y, gap, gap), 3)


# Defines a board class with several useful properties
class Board:

    def __init__(self, selected_key=None, playing_board=None, temp=None):
        self.selected_key = selected_key
        self.playing_board = playing_board
        self.temp = temp

    # Creates a new playable board
    def initialize_board(self):
        self.playing_board = solver.get_new_board(81 - 17)

    # Selects a box in the board based on passed in coordinates
    # Typically used when a user clicks a box
    def select(self, xcoord, ycoord):
        self.selected_key = (xcoord, ycoord)


def main():
    # Initializing game and play time
    pygame.init()
    play_time = 0

    finished = False
    key = None

    screen = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")

    # Initializing board and sudoku table
    play_board = Board()
    play_board.initialize_board()
    sudoku_board = play_board.playing_board

    # Starting the time
    start = time.time()

    running = True

    # Game loop
    while running:
        # Updates time as long as game isn't finished yet
        if not finished:
            play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    play_board.temp = None
                    key = None

                # Solves the board if user clicks space bar
                # TODO: Change this to a "Solve it!" button at the bottom
                if event.key == pygame.K_SPACE:
                    solver.solve(sudoku_board, True)
                    finished = True

                # Checks if current move is valid
                # Allows if so, does nothing if not
                # TODO: show clearly to the user that the move is invalid, rather than just doing nothing
                if event.key == pygame.K_RETURN:
                    i, j = play_board.selected_key

                    # Checks if user actually put in a move and if selected space is empty
                    if play_board.temp is not None and sudoku_board[i][j] == 0:

                        # Checks if move is valid
                        if solver.valid(i, j, play_board.temp, play_board.playing_board):

                            sudoku_board[i][j] = play_board.temp

                            # Checks if the board created by valid move is solvable
                            # Negates the move if not
                            if solver.solve(play_board.playing_board):
                                sudoku_board[i][j] = play_board.temp
                                play_board.temp = None
                            else:
                                sudoku_board[i][j] = 0
                        key = None

                        if solver.find_empty_element(sudoku_board) is None:
                            finished = True
                            print("You win!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                play_board.temp = None

                pos = pygame.mouse.get_pos()
                button_clicked = click(pos)
                if button_clicked:
                    play_board.select(button_clicked[0], button_clicked[1])
                    key = None

        if play_board.selected_key and key is not None:
            play_board.temp = key

        update_window(screen, play_board, play_time)
        pygame.display.flip()


main()
pygame.quit()
