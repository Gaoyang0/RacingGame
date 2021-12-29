# 地图信息,地图由26条直线所绘制,
# 因为直线好求交点,其他赛道绘制算法我不会,只好出此下策
map_lines = [
    [(340, 100), (340, 220)],
    [(340, 100), (410, 10)],
    [(410, 10), (580, 10)],
    [(580, 10), (790, 140)],
    [(790, 140), (720, 380)],
    [(470, 140), (650, 220)],
    [(650, 220), (550, 415)],
    [(720, 380), (790, 460)],
    [(790, 460), (700, 590)],
    [(550, 415), (670, 470)],
    [(700, 590), (380, 475)],
    [(550, 415), (340, 350)],
    [(340, 220), (510, 270)],
    [(340, 220), (225, 300)],
    [(340, 350), (205, 460)],
    [(380, 475), (280, 590)],
    [(280, 590), (160, 590)],
    [(160, 590), (10, 420)],
    [(205, 460), (120, 340)],
    [(10, 420), (10, 80)],
    [(10, 80), (80, 10)],
    [(80, 10), (250, 10)],
    [(120, 130), (215, 145)],
    [(120, 130), (120, 340)],
    [(215, 145), (120, 245)],
    [(340, 100), (250, 10)],
]
# # 1
# pygame.draw.line(screen, WALL_COLOR, (340, 100), (340, 220), WALL_WIDE)
# # 2
# pygame.draw.line(screen, WALL_COLOR, (340, 100), (410, 10), WALL_WIDE)
# # 3
# pygame.draw.line(screen, WALL_COLOR, (410, 10), (580, 10), WALL_WIDE)
# # 4
# pygame.draw.line(screen, WALL_COLOR, (580, 10), (790, 140), WALL_WIDE)
# # 5
# pygame.draw.line(screen, WALL_COLOR, (790, 140), (720, 380), WALL_WIDE)
# # 6
# pygame.draw.line(screen, WALL_COLOR, (470, 140), (650, 220), WALL_WIDE)
# # 7
# pygame.draw.line(screen, WALL_COLOR, (650, 220), (550, 415), WALL_WIDE)
# # 8
# pygame.draw.line(screen, WALL_COLOR, (720, 380), (790, 460), WALL_WIDE)
# # 9
# pygame.draw.line(screen, WALL_COLOR, (790, 460), (700, 590), WALL_WIDE)
# # 10
# pygame.draw.line(screen, WALL_COLOR, (550, 415), (670, 470), WALL_WIDE)
# # 11
# pygame.draw.line(screen, WALL_COLOR, (700, 590), (380, 475), WALL_WIDE)
# # 12
# pygame.draw.line(screen, WALL_COLOR, (550, 415), (340, 350), WALL_WIDE)
# # 13
# pygame.draw.line(screen, WALL_COLOR, (340, 220), (510, 270), WALL_WIDE)
# # 14
# pygame.draw.line(screen, WALL_COLOR, (340, 220), (225, 300), WALL_WIDE)
# # 15
# pygame.draw.line(screen, WALL_COLOR, (340, 350), (205, 460), WALL_WIDE)
# # 16
# pygame.draw.line(screen, WALL_COLOR, (380, 475), (280, 590), WALL_WIDE)
# # 17
# pygame.draw.line(screen, WALL_COLOR, (280, 590), (160, 590), WALL_WIDE)
# # 18
# pygame.draw.line(screen, WALL_COLOR, (160, 590), (10, 420), WALL_WIDE)
# # 19
# pygame.draw.line(screen, WALL_COLOR, (205, 460), (120, 340), WALL_WIDE)
# # 20
# pygame.draw.line(screen, WALL_COLOR, (10, 420), (10, 80), WALL_WIDE)
# # 21
# pygame.draw.line(screen, WALL_COLOR, (10, 80), (80, 10), WALL_WIDE)
# # 22
# pygame.draw.line(screen, WALL_COLOR, (80, 10), (250, 10), WALL_WIDE)
# # 23
# pygame.draw.line(screen, WALL_COLOR, (120, 130), (215, 145), WALL_WIDE)
# # 24
# pygame.draw.line(screen, WALL_COLOR, (120, 130), (120, 340), WALL_WIDE)
# # 25
# pygame.draw.line(screen, WALL_COLOR, (215, 145), (120, 245), WALL_WIDE)
# # 26
# pygame.draw.line(screen, WALL_COLOR, (340, 100), (250, 10), WALL_WIDE)
