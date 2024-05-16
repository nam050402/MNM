import pygame
import sys
from network import Network

screen_width = 750 
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("caro")
board_size = 11
tile_size = 50

pygame.font.init()
font_text_info = pygame.font.Font(None, 50)
font_state_info = pygame.font.Font(None, 30)
font_button_info = pygame.font.Font(None, 30) 

img_empty = pygame.image.load('Assets/caro_asset-01.png')
img_empty = pygame.transform.scale(img_empty,(tile_size,tile_size))
img_x = pygame.image.load('Assets/caro_asset-02.png')
img_x = pygame.transform.scale(img_x,(tile_size,tile_size))
img_o = pygame.image.load('Assets/caro_asset-03.png')
img_o = pygame.transform.scale(img_o,(tile_size,tile_size))
rect = img_empty.get_rect()
retreat_rect = pygame.Rect(600, 140, 100, 50)
rematch_rect = pygame.Rect(600, 200, 100, 50)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([0]*sz)
    return board

def draw_screen(img_empty, img_x, img_o, rect, board):
    for x in range(11):
        rect.center = (50*x+25, -25)
        for y in range(11):
            rect.centery += 50
            if board[x][y] == 0:
                screen.blit(img_empty, rect)
            elif board[x][y] == 1:
                screen.blit(img_x, rect)
            else:
                screen.blit(img_o, rect)

def draw_info_panel(screen, play_as, state):
    panel_width = screen_width - (board_size * tile_size)  # Width of the panel
    panel_color = (255, 155, 155, 150)
    info_panel = pygame.Surface((panel_width, screen_height), pygame.SRCALPHA)
    info_panel.fill(panel_color)

    font_color = (50, 50, 50)  # Màu trắng
    play_as_text = font_text_info.render(play_as, True, font_color)
    state_text = font_state_info.render(state, True, font_color)
    
    info_panel.blit(play_as_text, (5, 20))
    info_panel.blit(state_text, (5,70))
    screen.blit(info_panel, (550, 0))

def draw_button(text, color, rect):
    font_color = (50, 50, 50)  # Màu trắng
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font_button_info.render(text, True, font_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
                
def is_win(board):
    for x in range(board_size):
        for y in range (board_size):
            if board[x][y] != 0:
                score = 0
                if x<=6:
                    for t in range(4):
                        if board[x+t+1][y] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
                if x<=6 and y<=6:
                    for t in range(4):
                        if board[x+t+1][y+t+1] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
                if y<=6:
                    for t in range(4):
                        if board[x][y+t+1] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
                if x >=4 and y<=6:
                    for t in range(4):
                        if board[x-(t+1)][y+t+1] == board[x][y]:
                            score += 1
                        else:
                            score = 0
                            break;
                        if score == 4:
                            return board[x][y]
    return -1

def main():
    isClicking = False
    move_counter = 0
    game_over = False
    your_turn = True
    play_as_x = True
    waiting_for_opponent = False
    has_resign = False
    play_as = ""
    state = ""
    board = make_empty_board(board_size)
    data = []
    n = Network()
    start = n.get_client_state()
    if start[2] < 2:
        n.send(["waiting for opponent", -1])
        game_over = True
        move_counter = 0
        waiting_for_opponent = True
        state = "Waiting for opponent"
    else:
        n.send(["start game",-1])
        print("has sent")
        if start[1] == 2:
            your_turn = False
            state = "Your opponent turn!"
        else:
            state = "Your turn!"

    if start[1] == 2:
        # your_turn = False
        # state = "Your opponent turn!"
        play_as_x = False
        play_as = "You are O"
    else:
        # state = "Your turn!"
        play_as = "You are X"


    while True:
        data_recieve = n.recieve()
        print(data_recieve[0])
        if data_recieve[0] == "send client num":
            if data_recieve[1] >= 2: 
                # n.send(["waiting for opponent", -1])
                data =["start game",-1]
                game_over = False
                waiting_for_opponent = False
                if start[1] == 2:
                    your_turn = False
                    state = "Your opponent turn!"
                else:
                    state = "Your turn!"
        elif data_recieve[0]=="board data":
            if board != data_recieve[2]:
                board = data_recieve[2]
                move_counter += 1
                your_turn = True
                state = "Your turn!"
        elif data_recieve[0]=="player has disconnected":
            state = "opponent has disconnected"
            board = make_empty_board(11)
            waiting_for_opponent = True
            if start[1]==2:
                your_turn = False
            else:
                your_turn = True
        elif data_recieve[0] == "you has resign":
            has_resign = True
        elif data_recieve[0] == "you have offer rematch":
            state = data_recieve[0]
        elif data_recieve[0] == "you opponent has resign":
            game_over = True
            move_counter = 0
            if has_resign:
                state = "you has resign"
            else:
                state = data_recieve[0]
        elif data_recieve[0] == "start again":
            board = make_empty_board(11)
            game_over = False
            print("has false")
            if start[1] == 2:
                your_turn = False
                state = "Your opponent turn!"
            else:
                your_turn = True
                state = "Your turn!"

        if waiting_for_opponent:
            data = ["waiting for opponent", -1]
        else:
            data = ["maintain connection",-1] # chơi ở vị trí nào

        if game_over == False:
            if is_win(board) == 1:
                game_over = True
                move_counter = 0
                print("player 1 win")
                state = "X win"
            elif is_win(board) == 2:
                game_over = True
                move_counter = 0
                print("player 2 win")
                state = "O win"
        if move_counter >= 121 and game_over==False:
            game_over = True
            state = "draw"
            move_counter = 0

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                isClicking = True
                mouse_pos = pygame.mouse.get_pos()
                tile_click_x = int(mouse_pos[0]/50)
                print(tile_click_x)
                tile_click_y = int(mouse_pos[1]/50)
                print(tile_click_y)
                if waiting_for_opponent == False:
                    if tile_click_x <11 and game_over == False:
                        if board[tile_click_x][tile_click_y] == 0 and your_turn:
                            if play_as_x:
                                board[tile_click_x][tile_click_y] = 1
                                data = ["play pos data"]
                                data.append([tile_click_x, tile_click_y,1])
                                your_turn = False
                                move_counter += 1
                                state = "Your opponent turn!"
                            else:
                                board[tile_click_x][tile_click_y] = 2
                                data = ["play pos data"]
                                data.append([tile_click_x, tile_click_y,2])
                                your_turn = False
                                move_counter += 1
                                state = "Your opponent turn!"
                    else:
                        if retreat_rect.collidepoint(mouse_pos) and game_over == False:
                            draw_button("Resign", (150,150,150), retreat_rect)
                            print("Resign button clicked")
                            data = ["Resign", start[1]]
                        if rematch_rect.collidepoint(mouse_pos) and game_over:
                            draw_button("Rematch", (150,150,150), rematch_rect)
                            print("Rematch button clicked")
                            data = ["Rematch", start[1]]
            if event.type == pygame.MOUSEBUTTONUP:
                isClicking = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        draw_screen(img_empty, img_x, img_o, rect, board)
        draw_info_panel(screen,play_as,state)
        draw_button("Resign", (255,255,255), retreat_rect)
        draw_button("Rematch", (255,255,255), rematch_rect)

        n.send(data)
        pygame.display.update()

main() 