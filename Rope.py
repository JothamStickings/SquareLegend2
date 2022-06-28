import math


class Rope:
    def __init__(self, player, point):
        self.player = player
        self.point = point
        self.length = math.sqrt((player.x-point[0])**2+(player.y-point[1])**2)

    def get_true_length(self):
        return math.sqrt((self.player.x-self.point[0])**2+(self.player.y-self.point[1])**2)

    def pull(self):
        if self.length <= 3:
            del self
        else:
            vector = (self.player.x-self.point[0], self.player.y-self.point[1])
            distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            stretch = self.get_true_length()-self.length
            if stretch < 0:
                stretch = 0
            if stretch > 3:
                stretch = 3
            multiplier = -stretch / distance
            self.player.xspeed += 0.15 * vector[0] * multiplier
            self.player.yspeed += 0.15 * vector[1] * multiplier
            self.length -= 4
