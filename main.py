import pygame
import sys

screen_width = 750  # Increased width to include the panel
screen_height = 550
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("caro")
board_size = 11
tile_size = 50
pygame.font.init()
font_text_info = pygame.font.Font(None, 50)
font_state_info = pygame.font.Font(None, 30)
font_button_info = pygame.font.Font(None, 30) 

client_number = 0

isClicking = False
game_over = False

img_empty = pygame.image.load('Assets/caro_asset-01.png')
img_empty = pygame.transform.scale(img_empty,(50,50))
img_x = pygame.image.load('Assets/caro_asset-02.png')
img_x = pygame.transform.scale(img_x,(50,50))
img_o = pygame.image.load('Assets/caro_asset-03.png')
img_o = pygame.transform.scale(img_o,(50,50))
rect = img_empty.get_rect()


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
    play_as_text = font_text_info.render("You are X ", True, font_color)
    state_text = font_state_info.render("Your turn", True, font_color)
    
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
    global isClicking
    global game_over
    p1_turn = True
    state = ""
    board = make_empty_board(board_size)
    while True:
        draw_screen(img_empty, img_x, img_o, rect, board)
        draw_info_panel(screen,"","")
        if game_over == False:
            if is_win(board) == 1:
                game_over = True
                print("player 1 win")
            elif is_win(board) == 2:
                game_over = True
                print("player 2 win")

        mouse = pygame.mouse.get_pos()
        
        retreat_rect = pygame.Rect(600, 140, 100, 50)
        if retreat_rect.collidepoint(mouse):
            draw_button("Resign", (150,150,150), retreat_rect)
            if pygame.mouse.get_pressed()[0]:  # Kiểm tra xem nút chuột trái có được nhấn không
                print("Resign button clicked")  
        else:
            draw_button("Resign", (255,255,255), retreat_rect)

        draw_offer_rect = pygame.Rect(600, 200, 100, 50)
        if draw_offer_rect.collidepoint(mouse):
            draw_button("Draw", (150,150,150), draw_offer_rect)
            if pygame.mouse.get_pressed()[0]:  # Kiểm tra xem nút chuột trái có được nhấn không
                print("Draw button clicked")  
        else:
            draw_button("Draw", (255,255,255), draw_offer_rect)

        rematch_rect = pygame.Rect(600, 260, 100, 50)
        if rematch_rect.collidepoint(mouse):
            draw_button("Rematch", (150,150,150), rematch_rect)
            if pygame.mouse.get_pressed()[0]:  # Kiểm tra xem nút chuột trái có được nhấn không
                print("Rematch button clicked")  
        else:
            draw_button("Rematch", (255,255,255), rematch_rect)

        for event in pygame.event.get():
            if game_over == False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isClicking = True
                    mouse_pos = pygame.mouse.get_pos()
                    tile_click_x = int(mouse_pos[0]/50)
                    print(tile_click_x)
                    tile_click_y = int(mouse_pos[1]/50)
                    print(tile_click_y)
                    if tile_click_x <11:
                        if board[tile_click_x][tile_click_y] == 0 and p1_turn:
                            board[tile_click_x][tile_click_y] = 1
                            p1_turn = False
                        elif board[tile_click_x][tile_click_y] == 0 and p1_turn == False:
                            board[tile_click_x][tile_click_y] = 2
                            p1_turn = True
                if event.type == pygame.MOUSEBUTTONUP:
                    isClicking = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main() 