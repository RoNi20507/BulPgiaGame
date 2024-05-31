import select
import pygame
import sys
import math
import socket

# Initialize Pygame
pygame.init()

REFRESH_RATE = 60
LEFT = 1
RED_PLACE = (100, 250)
YELLOW_PLACE = (250, 250)
GREEN_PLACE = (400, 250)
BLUE_PLACE = (100, 400)
PURPLE_PLACE = (250, 400)
PINK_PLACE = (400, 400)
IP = "127.0.0.1"
PORT = 50006
PLACES = [[(550, 200), (580, 200), (610, 200), (640, 200)],
          [(550, 240), (580, 240), (610, 240), (640, 240)],
          [(550, 280), (580, 280), (610, 280), (640, 280)],
          [(550, 320), (580, 320), (610, 320), (640, 320)],
          [(550, 360), (580, 360), (610, 360), (640, 360)]]
PLACES2 = [[(550, 220), (580, 220), (610, 220), (640, 220)],
           [(550, 260), (580, 260), (610, 260), (640, 260)],
           [(550, 300), (580, 300), (610, 300), (640, 300)],
           [(550, 340), (580, 340), (610, 340), (640, 340)],
           [(550, 380), (580, 380), (610, 380), (640, 380)]]
FONT = pygame.font.Font(None, 48)
FONT2 = pygame.font.Font(None, 30)


# Set up the screen
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BUL PGIAA")
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)


def distance(point1, point2):
    """
    Calculate the distance between two points.

    :param point1: The first point as a tuple (x, y).
    :type point1: tuple
    :param point2: The second point as a tuple (x, y).
    :type point2: tuple

    :return: The distance between the two points.
    :rtype: float
    """
    x1, y1 = point1
    x2, y2 = point2
    distance1 = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance1


def return_color(point):
    """
    Determine the color index based on the clicked point.

    :param point: The point as a tuple (x, y).
    :type point: tuple

    :return: The index of the color, or 6 if no color is within range.
    :rtype: int
    """
    if distance(RED_PLACE, point) <= 50:
        return 0
    elif distance(YELLOW_PLACE, point) <= 50:
        return 1
    elif distance(GREEN_PLACE, point) <= 50:
        return 2
    elif distance(BLUE_PLACE, point) <= 50:
        return 3
    elif distance(PURPLE_PLACE, point) <= 50:
        return 4
    elif distance(PINK_PLACE, point) <= 50:
        return 5
    return 6


def send_lst(client_socket, lst, num):
    """
    Send a list of guessed colors to the server.

    :param client_socket: The client socket to send data through.
    :type client_socket: socket.socket
    :param lst: The list of guessed color indices.
    :type lst: list
    :param num: The number of guesses.
    :type num: int
    """
    data = ','.join(map(str, lst))
    print(data)
    client_socket.send(data.encode())


def draw_gussed_colors(lst):
    """
    Draw the guessed colors on the screen.

    :param lst: The list of guessed color indices.
    :type lst: list
    """
    j = 0
    num = 0
    while j < 4:
        print("printing circle")
        temp_place = PLACES[num]
        pygame.draw.circle(screen, circle_colors[lst[j]], temp_place[j], 10)
        j += 1
    num += 1

# Define circle parameters
circle_radius = 50
circle_positions = [RED_PLACE, YELLOW_PLACE, GREEN_PLACE, BLUE_PLACE, PURPLE_PLACE, PINK_PLACE]
circle_colors = [RED, YELLOW, GREEN, BLUE, PURPLE, PINK]
result_colors = [GREEN, YELLOW, RED]


def print_result(lst):
    """
    Print the result colors on the screen based on the server response.

    :param lst: The list of result color indices.
    :type lst: list
    """
    i = 0
    j = 0
    while j < 4:
        print("printing circle")
        temp_place2 = PLACES2[i]
        pygame.draw.circle(screen, result_colors[lst[j]], temp_place2[j], 5)
        j += 1
        #for el in PLACES2:
        #    el_new = (el[0], el[1] + 40)
        #    el = el_new


def main():
    """
    The main function to run the game. Initializes the connection, handles events, and manages the game state.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", PORT))
    server = [client_socket]

    # Clear the screen
    screen.fill(WHITE)
    # write on screens
    text = FONT.render("Enter your guess", True, (0, 0, 0))
    text_rect = text.get_rect(center=(250, 100))
    screen.blit(text, text_rect)
    text = FONT2.render("Previous guesses:", True, (0, 0, 0))
    text_rect = text.get_rect(center=(600, 150))
    screen.blit(text, text_rect)
    # Draw circles
    for i in range(len(circle_positions)):
        pygame.draw.circle(screen, circle_colors[i], circle_positions[i], circle_radius)

    pygame.display.flip()
    count = 0  # num of circles
    count2 = 0  # num of guesses
    list_numbers = []
    finish = False
    state = False
    data = ''

    while client_socket.recv(5) != b'START':
        pass
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if not state:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    place = pygame.mouse.get_pos()
                    if count < 4:
                        num = return_color(place)
                        if num < 6:
                            count += 1
                            list_numbers.append(num)
                            print("hi")
                            if count == 4:
                                send_lst(client_socket, list_numbers, count2)
                                draw_gussed_colors(list_numbers)
                                list_numbers.clear()
                                print(list_numbers)
                                state = True
                                count = 0
            else:
                inputs_ready, _, _ = select.select(server, [], [])
                print(inputs_ready)
                for s in inputs_ready:
                    data = s.recv(16).decode()
                    print(f"data: {data}")
                    if data == 'WON' or data == 'LOST':
                        finish = True
                        break
                    data = data.split(',')
                    data = [int(i) for i in data]
                    print("Response from server:", data)
                    print_result(data)
                    if data == [0, 0, 0, 0]:
                        finish = True
                        break
                    state = False

            for i in range(len(circle_positions)):
                pygame.draw.circle(screen, circle_colors[i], circle_positions[i], circle_radius)
                pygame.display.flip()

    client_socket.close()
    if data == 'LOST':
        print("you lost")
    else:
        print("you win")
    pygame.display.flip()
    clock.tick(REFRESH_RATE)
    pygame.quit()


if __name__ == "__main__":
    main()
