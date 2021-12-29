# 游戏逻辑模块,运行可通过键盘操纵,向外提供调用接口

import pygame
from pygame.locals import *
import math
import game_logic.my_item as my_item
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# 墙体的颜色
WALL_COLOR = (75, 60, 40)
# 墙体的宽度
WALL_WIDE = 12
lines = []

long_press = {'up': False, 'down': False, 'left': False, 'right': False}


# 根据键盘更新小车的状态
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


# 使小车绕车中心旋转
def rot_center(image, angle, topleft):
    """rotate an image while keeping its center and size"""
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    return rotated_image, rotated_rect


# 绘制小车
def carPaint(pygame, screen, car, image_car):
    rotated_image, rotated_rect = rot_center(image_car, 360 * (-1 * car.r) / (2 * math.pi), (car.x, car.y))
    screen.blit(rotated_image, rotated_rect.topleft)

    # 画车中心
    pygame.draw.circle(screen, YELLOW, car.get_center(), 4)

    # 画线
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.dis_pos[0], car.dis_pos[1]))

    pygame.draw.line(screen, YELLOW, car.get_center(), (car.ldis_pos[0], car.ldis_pos[1]))
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.lldis_pos[0], car.lldis_pos[1]))
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.rdis_pos[0], car.rdis_pos[1]))
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.rrdis_pos[0], car.rrdis_pos[1]))


# 用于计算地图的线
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


# 初始化地图的数据,用于计算小车离路边的距离
def initMap():
    from game_logic.map_data import map_lines
    line_num = 26
    for i in range(line_num):
        lines.append(Line(i + 1, map_lines[i][0][0], map_lines[i][0][1], map_lines[i][1][0], map_lines[i][1][1]))


# 绘制地图
def mapPaint(pygame, screen, bg):
    screen.blit(bg, Rect((0, 0), (0, 0)))
    pygame.draw.line(screen, RED, (10, 210), (120, 210), 4)


# 游戏控制逻辑
def gameStart():
    # 初始化
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    initMap()
    # 加载背景图片也就是地图
    bg = pygame.transform.scale(pygame.image.load("../image/bg.png"), (800, 600))
    # new小车类
    car = my_item.Car(50, 220)
    # 加载小车图片
    image_car = pygame.transform.scale(pygame.image.load("../image/car_r.png"), car.size)
    # 定义时钟类,用于控制主循环的速度
    clock = pygame.time.Clock()

    running = True

    start_time = time.time()

    while running:
        # 40FPS
        clock.tick(40)
        # 如果游戏未结束
        if car.alive:
            # 移动小车
            car.postion_move(0.01)
            # 更新小车的距离位置参数
            car.computer_and_update(lines)
            # 判断游戏是否结束
            car.is_live(lines)
            # 按键盘更新方向
            car = car_update(car)
            # 判断是否到达终点
            if car.is_goal():
                print("用时：", time.time() - start_time)
        # 处理键盘响应事件并更新对应的标记
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
        # 绘制地图也就是背景
        mapPaint(pygame, screen, bg)
        # 绘制小车
        carPaint(pygame, screen, car, image_car)
        pygame.display.flip()


if __name__ == "__main__":
    gameStart()
