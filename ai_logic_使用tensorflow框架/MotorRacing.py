# 用于模型和键盘操作比赛,键盘可以加速,键盘的小车为蓝色
import pygame
from pygame.locals import *
import math
from game_logic import my_item
from ai_logic_使用tensorflow框架.ai import get_res_by_tf
from ai_logic_自己实现神经网络.training_model import Network
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WALL_COLOR = (75, 60, 40)
WALL_WIDE = 12
lines = []

long_press = {'up': False, 'down': False, 'left': False, 'right': False}


def car_update(car):
    if long_press["up"]:
        car.speed_up()
    if long_press["down"]:
        car.speed_down()
    if long_press["left"]:
        car.left_move()
    if long_press["right"]:
        car.right_move()
    return car


def rot_center(image, angle, topleft):
    """rotate an image while keeping its center and size"""
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    return rotated_image, rotated_rect


def carPaint(pygame, screen, car, image_car):
    rotated_image, rotated_rect = rot_center(image_car, 360 * (-1 * car.r) / (2 * math.pi), (car.x, car.y))
    screen.blit(rotated_image, rotated_rect.topleft)

    # 画车中心
    pygame.draw.circle(screen, YELLOW, car.get_center(), 4)

    # 画线
    pygame.draw.line(screen, car.color, car.get_center(), (car.dis_pos[0], car.dis_pos[1]))

    pygame.draw.line(screen, car.color, car.get_center(), (car.ldis_pos[0], car.ldis_pos[1]))
    pygame.draw.line(screen, car.color, car.get_center(), (car.lldis_pos[0], car.lldis_pos[1]))
    pygame.draw.line(screen, car.color, car.get_center(), (car.rdis_pos[0], car.rdis_pos[1]))
    pygame.draw.line(screen, car.color, car.get_center(), (car.rrdis_pos[0], car.rrdis_pos[1]))


class Line:
    def __init__(self, i, x1, y1, x2, y2):
        self.index = i
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.a = (y2 - y1) / (x2 - x1 + 1)
        self.b = y1 - self.a * x1
        self.minx = min(x1, x2)
        self.miny = min(y1, y2)
        self.maxx = max(x1, x2)
        self.maxy = max(y1, y2)


def initMap():
    from game_logic.map_data import map_lines
    line_num = 26
    for i in range(line_num):
        lines.append(Line(i + 1, map_lines[i][0][0], map_lines[i][0][1], map_lines[i][1][0], map_lines[i][1][1]))


# 绘制地图
def mapPaint(pygame, font, screen, bg):

    screen.blit(bg, Rect((0, 0), (0, 0)))
    pygame.draw.rect(screen, RED, [0, 0, 20, 20], 0)
    screen.blit(font.render("TF AI", True, RED), Rect((25, 0), (0, 0)))
    pygame.draw.rect(screen, BLACK, [0, 25, 20, 20], 0)
    screen.blit(font.render("MY AI", True, BLACK), Rect((25, 25), (0, 0)))
    pygame.draw.rect(screen, YELLOW, [0, 50, 20, 20], 0)
    screen.blit(font.render("MYSELF", True, YELLOW), Rect((25, 50), (0, 0)))


def gameStart():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    font = pygame.font.Font(None, 25)

    initMap()

    bg = pygame.transform.scale(pygame.image.load("../image/bg.png"), (800, 600))

    # tensorflow训练的网络所操作小车
    car_tf_nn = my_item.Car(50, 220, color=RED)
    # 键盘所操作的小车
    car_ren = my_item.Car(50, 220, speed=600, color=YELLOW)
    # 自己实现网络操作的小车
    car_my_nn = my_item.Car(50, 220, speed=600, color=2)

    image_car_tf_nn = pygame.transform.scale(pygame.image.load("../image/car_r.png"), car_tf_nn.size)
    image_car_ren = pygame.transform.scale(pygame.image.load("../image/car_y.png"), car_ren.size)
    image_car_my_nn = pygame.transform.scale(pygame.image.load("../image/car_b.png"), car_my_nn.size)

    # 加载自己的网络
    W1 = np.loadtxt('../ai_logic_自己实现神经网络/model/W1.txt', dtype=np.float64)
    b1 = np.loadtxt('../ai_logic_自己实现神经网络/model/b1.txt', dtype=np.float64)
    W2 = np.loadtxt('../ai_logic_自己实现神经网络/model/W2.txt', dtype=np.float64)
    b2 = np.loadtxt('../ai_logic_自己实现神经网络/model/b2.txt', dtype=np.float64)
    col_max = np.loadtxt('../ai_logic_自己实现神经网络/model/col_max.txt', dtype=np.float64)
    my_nn = Network()
    my_nn.fl1.set_parameters(W1, b1.reshape(my_nn.fl1.output_size, 1))
    my_nn.fl2.set_parameters(W2, b2.reshape(my_nn.fl2.output_size, 1))

    clock = pygame.time.Clock()

    running = True
    while running:
        # 40FPS
        clock.tick(40)
        # tf控制的小车逻辑
        if car_tf_nn.alive:

            x = [car_tf_nn.dis_wall, car_tf_nn.ldis_wall, car_tf_nn.lldis_wall,
                 car_tf_nn.rdis_wall, car_tf_nn.rrdis_wall, car_tf_nn.v, car_tf_nn.r]
            res = get_res_by_tf(x)
            speed = res[0][0]
            direction = res[0][1]
            if direction < 0.2:
                # print("左转")
                car_tf_nn.left_move()
            if direction > 0.8:
                # print("右转")
                car_tf_nn.right_move()

            car_tf_nn.postion_move(0.01)
            car_tf_nn.computer_and_update(lines)
            car_tf_nn.is_live(lines)
            # car = car_update(car)

            # 打印已经移动的距离
            # print(car_tf_nn.distance)
            if car_tf_nn.is_goal():
                print("到达终点！")

        # 自己网络控制小车的逻辑
        if car_my_nn.alive:
            x = np.array([car_my_nn.dis_wall, car_my_nn.ldis_wall, car_my_nn.lldis_wall,
                 car_my_nn.rdis_wall, car_my_nn.rrdis_wall, car_my_nn.v, car_my_nn.r]) / col_max
            res = my_nn.forward(x.reshape(7, 1))
            speed = res[0][0]
            direction = res[1][0]
            if direction < 0.2:
                # print("左转")
                car_my_nn.left_move()
            if direction > 0.8:
                # print("右转")
                car_my_nn.right_move()

            car_my_nn.postion_move(0.01)
            car_my_nn.computer_and_update(lines)
            car_my_nn.is_live(lines)
            # car = car_update(car)
            # print(car_my_nn.distance)
            if car_my_nn.is_goal():
                print("到达终点！")
        # 键盘控制小车的逻辑
        if car_ren.alive:
            car_ren.postion_move(0.01)
            car_ren.computer_and_update(lines)
            car_ren.is_live(lines)
            car_ren = car_update(car_ren)

        for even in pygame.event.get():
            if even.type == QUIT:
                # pygame.image.save(screen, "bg.png")
                running = False
            elif even.type == KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_ESCAPE]:
                    print("esc")
                    running = False
                else:
                    if even.key == pygame.K_UP:
                        long_press['up'] = True
                    if even.key == pygame.K_DOWN:
                        long_press['down'] = True
                    if even.key == pygame.K_LEFT:
                        long_press['left'] = True
                    if even.key == pygame.K_RIGHT:
                        long_press['right'] = True
            elif even.type == KEYUP:
                if even.key == pygame.K_UP:
                    long_press['up'] = False
                if even.key == pygame.K_DOWN:
                    long_press['down'] = False
                if even.key == pygame.K_LEFT:
                    long_press['left'] = False
                if even.key == pygame.K_RIGHT:
                    long_press['right'] = False

        mapPaint(pygame, font, screen, bg)
        carPaint(pygame, screen, car_tf_nn, image_car_tf_nn)
        carPaint(pygame, screen, car_my_nn, image_car_my_nn)
        carPaint(pygame, screen, car_ren, image_car_ren)
        pygame.display.flip()


if __name__ == "__main__":
    gameStart()
