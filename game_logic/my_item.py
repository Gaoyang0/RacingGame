import math


# 小车
class Car:
    def __init__(self, x, y, size=(40, 20), speed=400, color=(255, 255, 0)):
        # 赛车当前位置
        self.x = x
        self.y = y
        # 赛车角度
        self.r = 271 * math.pi / 180
        # self.r = 0.0
        # 赛车速度
        self.v = speed
        self.xv = self.v * math.cos(self.r)
        self.yv = self.v * math.sin(self.r)
        # 赛车是否存活
        self.alive = True
        # 赛车行驶了多远
        self.distance = 0
        # 是否抵达终点
        self.goal = False
        # 赛车距离墙距离
        self.dis_wall = 0
        self.ldis_wall = 0
        self.lldis_wall = 0
        self.rdis_wall = 0
        self.rrdis_wall = 0

        self.dis_pos = (0, 0)
        self.ldis_pos = (0, 0)
        self.lldis_pos = (0, 0)
        self.rdis_pos = (0, 0)
        self.rrdis_pos = (0, 0)

        self.color = color

        # 赛车大小
        self.size = size

    # 左转
    def left_move(self):
        if self.alive:
            self.r = (self.r - 5 * math.pi / 180) % (math.pi * 2)
            self.xv = self.v * math.cos(self.r)
            self.yv = self.v * math.sin(self.r)

    # 右转
    def right_move(self):
        if self.alive:
            self.r = (self.r + 5 * math.pi / 180) % (math.pi * 2)
            self.xv = self.v * math.cos(self.r)
            self.yv = self.v * math.sin(self.r)

    # 加速
    def speed_up(self):
        self.v += 20
        if self.v >= 500:
            self.v = 500
        self.xv = self.v * math.cos(self.r)
        self.yv = self.v * math.sin(self.r)

    # 减速
    def speed_down(self):
        self.v -= 10
        if self.v < 30:
            self.v = 30
        self.xv = self.v * math.cos(self.r)
        self.yv = self.v * math.sin(self.r)

    # 移动
    def postion_move(self, time_passed_seconds):
        if self.alive:
            self.x = self.x + time_passed_seconds * self.xv
            self.y = self.y + time_passed_seconds * self.yv
            self.distance = self.distance + (
                    (time_passed_seconds * self.xv) ** 2 + (time_passed_seconds * self.yv) ** 2) ** 0.5

    # 计算交点位置
    def computer_intersect_pos(self, lines, angle, center_x, center_y):
        points = []
        # 偏转后的角度
        r_angle = (self.r + angle * (math.pi * 2) / 360) % (math.pi * 2)
        a = math.tan(r_angle)
        b = center_y - a * center_x
        for line in lines:
            f1 = line.y1 - a * line.x1 - b
            f2 = line.y2 - a * line.x2 - b
            # 异号
            if not ((f1 > 0 and f2 > 0) or (f1 < 0 and f2 < 0)):
                '''
                l1: y = a*x + b
                l2: y = line.a*x + line.b 
                '''
                # 两直线求交点
                x = (b - line.b) / (line.a - a)
                y = x * a + b
                points.append((x, y))
        # 得到终点
        if 0.5 * math.pi <= r_angle <= 1.5 * math.pi:
            # 朝向y轴左边取x最大
            max_p = (0, 0)
            for p in points:
                # 不在所朝方向跳过
                if p[0] >= center_x:
                    continue
                if p[0] >= max_p[0]:
                    max_p = p
            return max_p
        else:
            # 朝向y轴右边取x最小
            min_p = (800, 0)
            for p in points:
                # 不在所朝方向跳过
                if p[0] <= center_x:
                    continue
                if p[0] <= min_p[0]:
                    min_p = p
            return min_p

    # 更新各项距离位置参数
    def computer_and_update(self, lines):
        center_x, center_y = self.get_center()
        self.dis_pos = self.computer_intersect_pos(lines, 0, center_x, center_y)
        self.rrdis_pos = self.computer_intersect_pos(lines, 90, center_x, center_y)
        self.rdis_pos = self.computer_intersect_pos(lines, 45, center_x, center_y)
        self.ldis_pos = self.computer_intersect_pos(lines, -45, center_x, center_y)
        self.lldis_pos = self.computer_intersect_pos(lines, -90, center_x, center_y)

        self.dis_wall = ((self.dis_pos[0] - center_x) ** 2 + (self.dis_pos[1] - center_y) ** 2) ** 0.5
        self.ldis_wall = ((self.ldis_pos[0] - center_x) ** 2 + (self.ldis_pos[1] - center_y) ** 2) ** 0.5
        self.lldis_wall = ((self.lldis_pos[0] - center_x) ** 2 + (self.lldis_pos[1] - center_y) ** 2) ** 0.5
        self.rdis_wall = ((self.rdis_pos[0] - center_x) ** 2 + (self.rdis_pos[1] - center_y) ** 2) ** 0.5
        self.rrdis_wall = ((self.rrdis_pos[0] - center_x) ** 2 + (self.rrdis_pos[1] - center_y) ** 2) ** 0.5

    # 是否存活
    def is_live(self, lines):
        center_x, center_y = self.get_center()
        for line in lines:
            # x, y均不在范围内就直接排除
            if line.minx < center_x < line.maxx or line.miny < center_y < line.maxy:
                d1 = (center_y - line.a * center_x - line.b) ** 2 / (1 + line.a * line.a)
                d2 = (line.x1 - center_x) ** 2 + (line.y1 - center_y) ** 2
                d3 = (line.x2 - center_x) ** 2 + (line.y2 - center_y) ** 2
                d = min(d1, d2, d3)
                if d < 20:
                    print("死在： ", line.index, )
                    self.alive = False
                    return False
        return True

    # 是否到达目的地
    def is_goal(self):
        # 路程大于一定值并且中点和终点线很近
        # 终点线： (10, 210), (120, 210)
        flag = False
        bias = 5
        center_x, center_y = self.get_center()
        if 10 < center_x < 210 and 210 - bias < center_y < 210 + bias:
            flag = True
        if self.distance > 2500 and flag:
            return True
        return False

    # 获取小车中心位置
    def get_center(self):
        return int(self.x + self.size[0] / 2), int(self.y + self.size[1] / 2)


if __name__ == '__main__':
    car = Car(10, 80)
