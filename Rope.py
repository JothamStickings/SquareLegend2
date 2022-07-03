import math


class Rope:
    def __init__(self, player, point, plat):
        self.player = player
        self.point = point
        self.length = math.sqrt((player.x-point[0])**2+(player.y-point[1])**2)
        self.plat = plat

    def get_true_length(self):
        return math.sqrt((self.player.x-self.point[0])**2+(self.player.y-self.point[1])**2)

    def shorten(self):
        self.length -= 3

    def pull(self, count):
        if self.length <= 3:
            del self
        else:
            vector = (self.player.x-self.point[0], self.player.y-self.point[1])
            distance = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            stretch = self.get_true_length()-self.length
            if stretch < 1:
                stretch = 0
            if stretch > 4:
                stretch = 4
            multiplier = -stretch / distance
            self.player.xspeed += 0.2 * vector[0] * multiplier
            self.player.yspeed += 0.2 * vector[1] * multiplier
            self.player.yspeed *= 0.999
            self.player.xspeed *= 0.999
            if stretch > 2:
                self.length += stretch/10
            
            # move point
            self.point[0] -= 1
            for m in self.plat.move:
                if m[0] == "y":
                    if count % m[2] < m[2] / 2:
                        self.point[1] -= m[1]
                    else:
                        self.point[1] += m[1]
                if m[0] == "x":
                    if count % m[2] < m[2] / 2:
                        self.point[0] -= m[1]
                    else:
                        self.point[0] += m[1]


