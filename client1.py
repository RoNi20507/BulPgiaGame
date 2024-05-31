import pygame
import sys
import math
import socket

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
PLACES = [(550, 200), (580, 200), (610, 200), (640, 200)]

# Initialize Pygame
pygame.init()

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
PINK = (255, 100, 203)


def distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.

    :param point1: First point (x1, y1)
    :type point1: tuple
    :param point2: Second point (x2, y2)
    :type point2: tuple

    :return: Euclidean distance between the points
    :rtype: float
    """
    x1, y1 = point1
    x2, y2 = point2
    distance1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance1


def return_color(point):
    """
    Return the color index based on the distance to predefined color positions.

    :param point: Coordinates of the point to check
    :type point: tuple

    :return: Color index corresponding to the point's position
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

FONT = pygame.font.Font(None, 48)
FONT2 = pygame.font.Font(None, 30)


def send_lst(client_socket, lst):
    """
    Send the list of selected colors to the server and display it on the screen.

    :param client_socket: Socket to send data through
    :type client_socket: socket.socket
    :param lst: List of selected color indices
    :type lst: list of int
    """
    data = ','.join(map(str, lst))
    client_socket.send(data.encode())
    text = FONT2.render("your code is:", True, (0, 0, 0))
    text_rect = text.get_rect(center=(600, 150))
    screen.blit(text, text_rect)
    j = 0
    while j < 4:
        pygame.draw.circle(screen, circle_colors[lst[j]], PLACES[j], 10)
        j += 1
    lst.clear()


circle_radius = 50
circle_positions = [
    RED_PLACE,
    YELLOW_PLACE,
    GREEN_PLACE,
    BLUE_PLACE,
    PURPLE_PLACE,
    PINK_PLACE
]
circle_colors = [RED, YELLOW, GREEN, BLUE, PURPLE, PINK]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
print("Connected to server")

def main():
    """
    Main game loop that handles user interaction and communication with the server.
    """
    # Initialize Pygame
    pygame.init()
    # Set up the screen
    screen_width = 700
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BUL PGIAA")
    clock = pygame.time.Clock()
    # Clear the screen
    pygame.display.flip()
    screen.fill(WHITE)
    # write on screen
    text = FONT.render("Enter your code:", True, (0,0,0))
    text_rect = text.get_rect(center=(250, 100))
    screen.blit(text, text_rect)
    # Draw circles
    for i in range(len(circle_positions)):
        pygame.draw.circle(screen, circle_colors[i], circle_positions[i], circle_radius)
        count = 0
        list_numbers = []
    pygame.display.flip()
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                place = pygame.mouse.get_pos()
                if count < 4:
                    num = return_color(place)
                    if num < 6:
                        count += 1
                        list_numbers.append(num)
                        print("hi")
                        if count == 4:
                            send_lst(client_socket, list_numbers)
                            print("sent")
                            finish = True

            for i in range(len(circle_positions)):
                pygame.draw.circle(screen, circle_colors[i], circle_positions[i], circle_radius)
            pygame.display.flip()

    data = client_socket.recv(10)
    while data == b'':
        print("hi?")

    print(data)
    if data == b'LOST':
        print("you lost")
    if data == b'WON':
        print("you won")

    client_socket.close()
    clock.tick(REFRESH_RATE)
    pygame.quit()


if __name__ == "__main__":
    main()
