import pygame
import constant as c
import algorithms

board = algorithms.board_ex1


def update_fps(clock, font):
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def update_num(pos, font, init):
    if init:
        num_text = font.render(str(board[pos[0]][pos[1]]), 1, c.color['black'])
    else:
        num_text = font.render(str(board[pos[0]][pos[1]]), 1, c.color['grey'])
    return num_text


# hardcoded input handling but
# I have no idea how to do it otherwise
def input_handle(event, pos):
    if pos != (-1, -1):
        if event.key == pygame.K_1:
            board[pos[0]][pos[1]] = 1
        elif event.key == pygame.K_2:
            board[pos[0]][pos[1]] = 2
        elif event.key == pygame.K_3:
            board[pos[0]][pos[1]] = 3
        elif event.key == pygame.K_4:
            board[pos[0]][pos[1]] = 4
        elif event.key == pygame.K_5:
            board[pos[0]][pos[1]] = 5
        elif event.key == pygame.K_6:
            board[pos[0]][pos[1]] = 6
        elif event.key == pygame.K_7:
            board[pos[0]][pos[1]] = 7
        elif event.key == pygame.K_8:
            board[pos[0]][pos[1]] = 8
        elif event.key == pygame.K_9:
            board[pos[0]][pos[1]] = 9
        elif event.key == pygame.K_BACKSPACE:
            board[pos[0]][pos[1]] = 0


def mouse_pos_to_cell(pos):
    row = col = -1
    for i in range(1, 10):
        if i * c.cell_side > pos[1] and row == -1:
            row = i - 1
        if i * c.cell_side > pos[0] and col == -1:
            col = i - 1
    return row, col


def main():
    # Setup screen(window)
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
    font1 = pygame.font.SysFont("comicsansms", 50)
    screen = pygame.display.set_mode((c.cell_nr * c.cell_side, c.cell_nr * c.cell_side))
    selected = (-1, -1)

    # Setup the algorithms
    run = True
    init = False
    solved = False
    solvable = algorithms.init()
    pos = algorithms.find_max()[0]

    while run:
        # Draw background color
        screen.fill(c.color['white'])

        # Events handling
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and not init:
                if event.key == pygame.K_SPACE and solvable:
                    init = True
                    # Find the constraint of the current board after altering
                    constraint = algorithms.find_max()
                    pos = constraint[0]
                    # print(constraint)
                elif event.key == pygame.K_r:
                    algorithms.board_reset()
                    run = True
                    init = False
                    solved = False
                    selected = (-1, -1)
                input_handle(event, selected)
                solvable = algorithms.init()
            elif event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Track the position of the mouse
        if pygame.mouse.get_pressed()[0] and not init and not solved:
            selected = mouse_pos_to_cell(pygame.mouse.get_pos())

        # Run the algorithms?
        if init and solvable:
            selected = (-1, -1)
            tmp = algorithms.solve_one(pos)
            if tmp != 0:
                if not algorithms.find_next(pos):
                    init = False
                    solved = True
                pos = algorithms.find_next(pos)
            elif tmp == 0:
                # Board not solvable!
                if algorithms.find_prev(pos, constraint) == constraint[0] and board[constraint[0][0]][constraint[0][1]] == constraint[1]:
                    init = False
                    solvable = False
                pos = algorithms.find_prev(pos, constraint)

        # Draw the board
        for i in range(1, 10):
            pygame.draw.line(screen, c.color['black'], (0, i * c.cell_side),
                             (c.cell_nr * c.cell_side, i * c.cell_side))
            for j in range(10):
                pygame.draw.line(screen, c.color['black'], (j * c.cell_side, 0),
                                 (j * c.cell_side, c.cell_side * c.cell_nr))

        # Display current FPS
        screen.blit(update_fps(clock, font), (520, 0))

        # Draw the number inside each cell
        for row in range(9):
            for col in range(9):
                if board[row][col] != 0:
                    screen.blit(update_num((row, col), font1, init), (col * c.cell_side, row * c.cell_side))

        # Blit the selected cell
        if selected != (-1, -1):
            rect = pygame.Surface((c.cell_side, c.cell_side), pygame.SRCALPHA, 32)
            rect.fill(c.color['rgba_red'])
            screen.blit(rect, (selected[1] * c.cell_side, selected[0] * c.cell_side))
        else:
            if not init and not solved and solvable:
                screen.blit(font1.render("Press space to solve", 1, c.color['black']), (40, 200))
                screen.blit(font1.render("or click any square", 1, c.color['black']), (40, 270))
                screen.blit(font1.render("to manually change", 1, c.color['black']), (40, 340))
                screen.blit(font1.render("any cell's value", 1, c.color['black']), (40, 410))

        # Toast the message
        if not solvable and not solved:
            screen.blit(font1.render("Invalid board!", 1, c.color['rgba_red']), (40, 200))
            screen.blit(font1.render("Press Backspace to", 1, c.color['rgba_red']), (40, 270))
            screen.blit(font1.render("delete or 'R'", 1, c.color['rgba_red']), (40, 340))
            screen.blit(font1.render("to reset Board!", 1, c.color['rgba_red']), (40, 410))

        if solved:
            screen.blit(font1.render("Board solved!", 1, c.color['green']), (40, 200))
            screen.blit(font1.render("Press R to", 1, c.color['green']), (40, 270))
            screen.blit(font1.render("reset the board", 1, c.color['green']), (40, 340))

        pygame.display.update()
        clock.tick(60)


main()
