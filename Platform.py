class Platform:
    def __init__(self, x, y, width, height, move=None):
        if move is None:
            move = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move = move
