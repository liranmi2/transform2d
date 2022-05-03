"""
Liran Michaelov 204238174
Alona Rozner 315638155
Yuval Mark Berghaus 313247116
"""

import pygame
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 150)

draw_max_x, draw_max_y = 700, 530


def plot_circle_points(Xc, Yc, x, y, color):
    """Plotting circle points for every iteration in 'my_circle'"""
    global screen
    Xc, Yc, x, y = int(Xc), int(Yc), int(x), int(y)
    screen.set_at((Xc + x, Yc + y), color)
    screen.set_at((Xc + x, Yc - y), color)
    screen.set_at((Xc - x, Yc + y), color)
    screen.set_at((Xc - x, Yc - y), color)
    screen.set_at((Xc + y, Yc + x), color)
    screen.set_at((Xc + y, Yc - x), color)
    screen.set_at((Xc - y, Yc + x), color)
    screen.set_at((Xc - y, Yc - x), color)


def my_circle(Xc, Yc, r, color):
    """Calculating all available integer points on circle by (Xcenter,Ycenter) and radius"""
    global screen
    x, y = 0, r
    p = 3 - 2 * r
    while x <= y:
        plot_circle_points(Xc, Yc, x, y, color)
        if p < 0:
            p = p + 4 * x + 6
        else:
            p = p + 4 * (x - y) + 10
            y -= 1
        x += 1


def dda_line(x1, y1, x2, y2, color):
    """Plotting points on a line from (x1,y1) to (x2,y2) in requested color"""
    global screen
    dx, dy = (x2 - x1), (y2 - y1)
    d_range = int(max(abs(dx), abs(dy)))
    if d_range == 0:
        return
    dx, dy = dx / d_range, dy / d_range
    for i in range(d_range):
        screen.set_at((round(x1), round(y1)), color)
        x1 += dx
        y1 += dy


def bezier_curve(x1, y1, x2, y2, x3, y3, x4, y4, n, color):
    """Drawing a n lines Bezier curve from (x1,y1) to (x2,y2)
       according to (x3,y3) and (x4,y4) curves using dda_line function"""
    global screen
    ax = -x1 + 3 * x2 - 3 * x3 + x4
    bx = 3 * x1 - 6 * x2 + 3 * x3
    cx = -3 * x1 + 3 * x2
    dx = x1
    ay = -y1 + 3 * y2 - 3 * y3 + y4
    by = 3 * y1 - 6 * y2 + 3 * y3
    cy = -3 * y1 + 3 * y2
    dy = y1
    t = 0
    points = list()
    points.append((np.round(x1), np.round(y1)))
    for _ in range(n):
        t += 1 / n
        xt = ax * (t ** 3) + bx * (t ** 2) + cx * t + dx
        yt = ay * (t ** 3) + by * (t ** 2) + cy * t + dy
        points.append((np.round(xt), np.round(yt)))
    for i in range(len(points) - 1):
        dda_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], color)


def get_min_max_values():
    """
    Get the minimum and maximum x and y values from all the points received globally.
    Also calculates the center values.
    Result passed globally.
    """
    global lines, curves, circles, max_x, max_y , min_x, min_y, center_x, center_y

    lines_x = [l[i] for l in lines for i,t in enumerate(l) if i%2 == 0]
    lines_y = [l[i] for l in lines for i,t in enumerate(l) if i%2 != 0]

    curves_x = [l[i] for l in curves for i,t in enumerate(l) if i%2 == 0]
    curves_y = [l[i] for l in curves for i,t in enumerate(l) if i%2 != 0]

    circles_x = [l[0] + l[2] for l in circles]
    circles_x.extend([l[0] - l[2] for l in circles])

    circles_y = [l[1] + l[2] for l in circles]
    circles_y.extend([l[1] - l[2] for l in circles])

    max_x = max(max(lines_x),max(curves_x),max(circles_x))
    max_y = max(max(lines_y),max(curves_y),max(circles_y))
    min_x = min(min(lines_x),min(curves_x),min(circles_x))
    min_y = min(min(lines_y),min(curves_y),min(circles_y))
    center_x = int((max_x + min_x)/2)
    center_y = int((max_y + min_y)/2)


def data_upload_and_scale():
    """
    Uploads the data from 3 different files.
    Scaling the drawing to fit the drawing area (between the frame and buttons), and centers it.
    New values passed globally.
    """
    global lines, curves, circles, max_x, max_y

    lines = np.loadtxt(open('data/lines.csv', 'rb'), delimiter=',', skiprows=1).astype(int)
    curves = np.loadtxt(open('data/curves.csv', 'rb'), delimiter=',', skiprows=1).astype(int)
    circles = np.loadtxt(open('data/circles.csv', 'rb'), delimiter=',', skiprows=1).astype(int)
    get_min_max_values()

    if max_x < draw_max_x and max_y < draw_max_y:
        return

    x, y = draw_max_x*3/4, draw_max_y*3/4

    coeff = max((max_x/x), (max_y/y))

    lines = (lines/coeff)
    curves = (curves/coeff)
    circles = (circles/coeff)

    get_min_max_values()

    translate(draw_max_x/9, draw_max_y/9)


def draw_buttons(sidebar=True):
    """
    Draws all the buttons using pygame library.
    :param sidebar: determines whether the transformation buttons will appear
    """

    # bottom buttons
    upload_icon = pygame.image.load("src/img/upload_icon.png")
    upload_icon = pygame.transform.scale(upload_icon, (55, 55))
    pygame.draw.rect(screen, (245, 245, 245), (150,530, 75, 75), border_radius=15)
    pygame.draw.rect(screen, BLACK, (150,530, 75, 75),width=3, border_radius=15)
    screen.blit(upload_icon,(160,540))

    if sidebar:

        clear_icon = pygame.image.load("src/img/clear_icon.png")
        clear_icon = pygame.transform.scale(clear_icon, (55, 55))
        pygame.draw.rect(screen, (161, 246, 255), (450, 530, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (450, 530, 75, 75), width=3, border_radius=15)
        screen.blit(clear_icon, (460, 540))

        save_icon = pygame.image.load("src/img/save_icon.png")
        save_icon = pygame.transform.scale(save_icon, (50, 50))
        pygame.draw.rect(screen, (201, 255, 184), (300,530, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (300,530, 75, 75),width=3, border_radius=15)
        screen.blit(save_icon,(312,542))

    # side buttons
        rotate_icon = pygame.image.load("src/img/rotate_icon.png")
        rotate_icon = pygame.transform.scale(rotate_icon, (65, 65))
        pygame.draw.rect(screen, (107, 207, 50), (700,30, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (700,30, 75, 75),width=3, border_radius=15)
        screen.blit(rotate_icon,(705,35))

        move_icon = pygame.image.load("src/img/move_icon.png")
        move_icon = pygame.transform.scale(move_icon, (65, 65))
        pygame.draw.rect(screen, (74, 179, 255), (700,130, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (700,130, 75, 75),width=3, border_radius=15)
        screen.blit(move_icon,(705,135))

        resize_icon = pygame.image.load("src/img/resize_icon.png")
        resize_icon = pygame.transform.scale(resize_icon, (65, 65))
        pygame.draw.rect(screen, (255, 54, 54), (700,230, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (700,230, 75, 75),width=3, border_radius=15)
        screen.blit(resize_icon,(705,235))

        horizontal_flip_icon = pygame.image.load("src/img/horizontal_flip_icon.png")
        horizontal_flip_icon = pygame.transform.scale(horizontal_flip_icon, (65, 65))
        pygame.draw.rect(screen, (255, 238, 54), (700,330, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (700,330, 75, 75),width=3, border_radius=15)
        screen.blit(horizontal_flip_icon,(705,335))

        vertical_flip_icon = pygame.image.load("src/img/vertical_flip_icon.png")
        vertical_flip_icon = pygame.transform.scale(vertical_flip_icon, (65, 65))
        pygame.draw.rect(screen, (182, 92, 247), (700,430, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (700,430, 75, 75),width=3, border_radius=15)
        screen.blit(vertical_flip_icon,(705,435))

        shear_icon = pygame.image.load("src/img/shear_icon.png")
        shear_icon = pygame.transform.scale(shear_icon, (65, 65))
        pygame.draw.rect(screen, (245, 166, 64), (700,530, 75, 75), border_radius=15)
        pygame.draw.rect(screen, BLACK, (700,530, 75, 75),width=3, border_radius=15)
        screen.blit(shear_icon,(705,535))


def draw_car():
    """
    Draws the car using drawing functions
    """
    global lines, curves, circles

    for l in lines:
        dda_line(l[0], l[1], l[2], l[3], BLUE)

    for b in curves:
        bezier_curve(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], 25, BLUE)

    for c in circles:
        my_circle(c[0], c[1], c[2], BLUE)


def save_to_file(suffix='_new'):
    """
    Saves all the current points to a new files with a requested suffix
    :param suffix: The suffix to all files, default '_new'
    """
    global line, curves, circles

    np.savetxt("data/lines"+suffix+".csv", lines, header="x1,y1,x2,y2", comments='', delimiter=",", fmt='%d')
    np.savetxt("data/curves"+suffix+".csv", curves, header="x1,y1,x2,y2,x3,y3,x4,y4", comments='', delimiter=",", fmt='%d')
    np.savetxt("data/circles"+suffix+".csv", circles, header="xc,yc,r", comments='', delimiter=",", fmt='%d')


def scale(coeff):
    """
    First moving the drawing to (0,0) by subtracting center_x, center_y
    Scales the drawing by a given coefficient
    Then returns it to original location by adding center_x, center_y
    If the drawing is about to go out of scope, the values won't change
    :param coeff: The coefficient to scale the drawing by
    """
    global lines, curves, circles

    lines_copy = lines.copy()
    curves_copy = curves.copy()
    circles_copy = circles.copy()

    lines = [l[i] - center_x if i%2 == 0 else l[i] - center_y for l in lines for i, t in enumerate(l)]
    lines = np.array([lines[i:i + 4] for i in range(0, len(lines), 4)])

    curves = [l[i] - center_x if i%2 == 0 else l[i] - center_y for l in curves for i, t in enumerate(l)]
    curves = np.array([curves[i:i + 8] for i in range(0, len(curves), 8)])

    for l in circles:
        l[0] -= center_x
        l[1] -= center_y

    lines = (lines*coeff).astype(float)
    curves = (curves*coeff).astype(float)
    circles = (circles*coeff).astype(float)

    lines = [l[i] + center_x if i%2 == 0 else l[i] + center_y for l in lines for i, t in enumerate(l)]
    lines = np.array([lines[i:i + 4] for i in range(0, len(lines), 4)])

    curves = [l[i] + center_x if i%2 == 0 else l[i] + center_y for l in curves for i, t in enumerate(l)]
    curves = np.array([curves[i:i + 8] for i in range(0, len(curves), 8)])

    for l in circles:
        l[0] += center_x
        l[1] += center_y

    get_min_max_values()
    if max_x > draw_max_x or max_y > draw_max_y or min_x < 0 or min_y < 0:
        lines = lines_copy
        curves = curves_copy
        circles = circles_copy


def calculate_angle(x1, y1, x2, y2):
    """
    Calculates the angle between two points
    :param x1: The x of first point
    :param y1: The y of first point
    :param x2: The x of second point
    :param y2: The y of second point
    :return angle: The angle between (x1,y1) to (x2,y2)
    """
    radian = math.atan2(y1 - y2, x1 - x2)
    angle = math.degrees(radian)
    return angle


def rotate(x1, y1, x2, y2):
    """
    First moving the drawing to (0,0) by subtracting center_x, center_y
    Calculates the angle difference between angle((x1,y1),(center_x,center_y))
    to angle((x2,y2),(center_x,center_y)) using calculate_angle()
    Rotates the drawing by this angle
    Then returns it to original location by adding center_x, center_y
    If the drawing is about to go out of scope, the values won't change
    :param x1: The x of first point
    :param y1: The y of first point
    :param x2: The x of second point
    :param y2: The y of second point
    """
    global lines, curves, circles, center_x, center_y

    angle = calculate_angle(x2, y2, center_x, center_y) - calculate_angle(x1, y1, center_x, center_y)

    sinus = math.sin(angle / 180 * math.pi)
    cosinus = math.cos(angle / 180 * math.pi)

    lines_copy = lines.copy()
    curves_copy = curves.copy()
    circles_copy = circles.copy()
    lines_r = [l[i] - center_x if i%2 == 0 else l[i] - center_y for l in lines for i,t in enumerate(l)]
    lines_r = np.array([lines_r[i:i + 4] for i in range(0, len(lines_r), 4)])

    curves_r = [l[i] - center_x if i%2 == 0 else l[i] - center_y for l in curves for i,t in enumerate(l)]
    curves_r = np.array([curves_r[i:i + 8] for i in range(0, len(curves_r), 8)])

    circles_r = list()
    for l in circles:
        circles_r.append(l[0] - center_x)
        circles_r.append(l[1] - center_y)
        circles_r.append(l[2])
    circles_r = np.array([circles_r[i:i + 3] for i in range(0, len(circles_r), 3)])

    for i, line in enumerate(lines):
        x1, y1, x2, y2 = lines_r[i]
        line[0] = x1 * cosinus - y1 * sinus + center_x
        line[1] = x1 * sinus + y1 * cosinus + center_y
        line[2] = x2 * cosinus - y2 * sinus + center_x
        line[3] = x2 * sinus + y2 * cosinus + center_y

    for i, curve in enumerate(curves):
        x1, y1, x2, y2, x3, y3, x4, y4 = curves_r[i]
        curve[0] = x1 * cosinus - y1 * sinus + center_x
        curve[1] = x1 * sinus + y1 * cosinus + center_y
        curve[2] = x2 * cosinus - y2 * sinus + center_x
        curve[3] = x2 * sinus + y2 * cosinus + center_y
        curve[4] = x3 * cosinus - y3 * sinus + center_x
        curve[5] = x3 * sinus + y3 * cosinus + center_y
        curve[6] = x4 * cosinus - y4 * sinus + center_x
        curve[7] = x4 * sinus + y4 * cosinus + center_y
    #
    for i, point in enumerate(circles):
        x, y, r = circles_r[i]
        point[0] = x * cosinus - y * sinus + center_x
        point[1] = x * sinus + y * cosinus + center_y
        point[2] = r
    get_min_max_values()
    if max_x > draw_max_x or max_y > draw_max_y or min_x < 0 or min_y < 0:
        lines = lines_copy
        curves = curves_copy
        circles = circles_copy


def translate(x_dst, y_dst):
    """
    Adding x_dst to all x values and y_dst to all y values of the drawing
    If the drawing is about to go out of scope, the values won't change
    :param x_dst: (x2-x1) -  the difference between x values of two points
    :param y_dst: (y2-y1) - the difference between y values of two points
    """
    global lines, curves, circles

    lines_copy = lines.copy()
    curves_copy = curves.copy()
    circles_copy = circles.copy()

    lines = [l[i] + x_dst if i%2 == 0 else l[i] + y_dst for l in lines for i,t in enumerate(l)]
    lines = np.array([lines[i:i + 4] for i in range(0, len(lines), 4)])

    curves = [l[i] + x_dst if i%2 == 0 else l[i] + y_dst for l in curves for i,t in enumerate(l)]
    curves = np.array([curves[i:i + 8] for i in range(0, len(curves), 8)])

    for l in circles:
        l[0] += x_dst
        l[1] += y_dst

    get_min_max_values()
    if max_x > draw_max_x or max_y > draw_max_y or min_x < 0 or min_y < 0:
        lines = lines_copy
        curves = curves_copy
        circles = circles_copy


def mirror(direction='horizontal'):
    """
    Flipping/mirroring the drawing horizontally or vertically around center_x, center_y
    If the drawing is about to go out of scope, the values won't change
    :param direction: The direction to flip/mirror, default = 'horizontal'
    """
    global lines, curves, circles

    lines_copy = lines.copy()
    curves_copy = curves.copy()
    circles_copy = circles.copy()

    if direction == 'horizontal':
        lines = [l[i] + (center_x - l[i]) * 2 if i % 2 == 0 else l[i] for l in lines for i, t in enumerate(l)]
        lines = np.array([lines[i:i + 4] for i in range(0, len(lines), 4)])

        curves = [c[i] + (center_x - c[i]) * 2 if i % 2 == 0 else c[i] for c in curves for i, t in enumerate(c)]
        curves = np.array([curves[i:i + 8] for i in range(0, len(curves), 8)])

        for p in circles:
            p[0] += (center_x - p[0]) * 2
    elif direction == 'vertical':
        lines = [l[i] + (center_y - l[i]) * 2 if i % 2 != 0 else l[i] for l in lines for i, t in enumerate(l)]
        lines = np.array([lines[i:i + 4] for i in range(0, len(lines), 4)])

        curves = [c[i] + (center_y - c[i]) * 2 if i % 2 != 0 else c[i] for c in curves for i, t in enumerate(c)]
        curves = np.array([curves[i:i + 8] for i in range(0, len(curves), 8)])

        for p in circles:
            p[1] += (center_y - p[1]) * 2

    get_min_max_values()
    if max_x > draw_max_x or max_y > draw_max_y or min_x < 0 or min_y < 0:
        lines = lines_copy
        curves = curves_copy
        circles = circles_copy


def shear(shift_distance):
    """
    Shearing the drawing on x axis by a given shift distance
    Adding max_y * shift_distance / y to all x values
    If the drawing is about to go out of scope, the values won't change
    :param shift_distance: (x2-x1) - The distance to shear
    """
    global lines, curves, circles

    lines_copy = lines.copy()
    curves_copy = curves.copy()
    circles_copy = circles.copy()

    max_y_l = max([l[i] for l in lines for i,t in enumerate(l) if i%2 != 0])
    # min_y_l = min([l[i] for l in lines for i,t in enumerate(l) if i%2 != 0])
    max_y_l = (max_y_l - min_y) * 0.7

    lines = [(l[i] + (max_y_l*shift_distance/l[i+1])) if i % 2 == 0 and l[i+1] - min_y < max_y_l else l[i] for l in lines for i,t in enumerate(l)]
    lines = np.array([lines[i:i + 4] for i in range(0, len(lines), 4)])

    curves = [(l[i] + (max_y_l*shift_distance/l[i+1])) if i % 2 == 0 and l[i+1] - min_y < max_y_l else l[i] for l in curves for i,t in enumerate(l)]
    curves = np.array([curves[i:i + 8] for i in range(0, len(curves), 8)])

    for point in circles:
        if point[1] - min_y < max_y_l:
            point[0] += (max_y_l*shift_distance/point[1])

    get_min_max_values()
    if max_x > draw_max_x or max_y > draw_max_y or min_x < 0 or min_y < 0:
        lines = lines_copy
        curves = curves_copy
        circles = circles_copy


def main():
    run = True
    action = None
    drag = False
    clear_screen = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                # listening to side buttons
                if x > 700 and not clear_screen:
                    if 30 < y < 105:
                        action = 'rotate'
                    elif 130 < y < 205:
                        action = 'translate'
                    elif 230 < y < 305:
                        action = 'scale'
                    elif 330 < y < 405:
                        mirror('horizontal')
                        screen.blit(BACKGROUND, (0, 0))
                        draw_car()
                        draw_buttons()
                    elif 430 < y < 505:
                        mirror('vertical')
                        screen.blit(BACKGROUND, (0, 0))
                        draw_car()
                        draw_buttons()
                    elif 530 < y < 605:
                        action = 'shear'

                # listening to bottom buttons
                elif y > 530:
                    if 150 < x < 225:
                        screen.blit(BACKGROUND, (0, 0))
                        data_upload_and_scale()
                        draw_car()
                        draw_buttons()
                        clear_screen = False
                    elif 300 < x < 375 and not clear_screen:
                        save_to_file()
                    elif 450 < x < 525 and not clear_screen:
                        screen.blit(BACKGROUND, (0, 0))
                        draw_buttons(False)
                        clear_screen = True

                else:
                    x1, y1 = x, y
                    drag = True

            elif event.type == pygame.MOUSEMOTION:
                if drag:
                    x2, y2 = event.pos

                    if action == 'rotate':
                        rotate(x1, y1, x2, y2)

                    elif action == 'translate':
                        translate(event.rel[0], event.rel[1])

                    elif action == 'scale':
                        try:
                            scale(max(x2/x1, y2/y1))
                        except ZeroDivisionError:
                            pass

                    elif action == 'shear':
                        shear(x2 - x1)

                    screen.blit(BACKGROUND, (0, 0))
                    draw_car()
                    draw_buttons()
                    x1, y1 = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False

        pygame.display.flip()
        clock.tick(60)
    return


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 630))
    BACKGROUND = pygame.image.load("src/img/background.jpg")
    screen.blit(BACKGROUND, (0, 0))
    pygame.display.set_caption("Transform2D")
    button_font = pygame.font.SysFont('arial', 50)
    draw_buttons(False)
    main()

