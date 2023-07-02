import pygame
import numpy as np

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 400
WINDOW_CENTER = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTGRAY = (200, 200, 200)
BG_COLOR = BLACK

pygame.init()
pygame.display.set_caption("20190536 박수빈 - clock")
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

ballHome = [WINDOW_WIDTH/2 - 15, WINDOW_HEIGHT - 15]

def getRectangle(x = 0, y = 0, r = 30):
    v = np.array([[x,   y],
                  [x+r, y],
                  [x+r, y+r],
                  [x,   y+r]],
                  dtype = "float")
    return v
def R3mat(deg):
    theta = np.deg2rad(deg)
    c = np.cos(theta)
    s = np.sin(theta)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return R
def T3mat(a, b):
    t = np.eye(3)
    t[0, 2] = a
    t[1, 2] = b
    return t

class myBall:
    def __init__(self):
        self.x = ballHome[0]
        self.y = ballHome[1]-20
        self.vecX = 0
        self.vecY = 0
        pass
    def update(self, mx, my):
        self.vecX = mx - self.x
        self.vecY = my - self.y
        self.x += self.vecX
        self.y += self.vecY
    def draw(self):
        if self.y >= 32 * 3:
            pygame.draw.rect(SCREEN, LIGHTGRAY, [self.x, self.y, 30, 30])

def main():
    done = False
    center = []
    ball = myBall()
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                ball.update(mouseX, mouseY)

        SCREEN.fill(BG_COLOR)
        ball.draw()

        for i in range(15):
            for j in range(3):
                color = np.random.randint(0,256, size=3)
                box = getRectangle(32*i, 32*j, 29)
                pygame.draw.polygon(SCREEN, color, box, 0)
                center.append([32*i+29/2, 32*j+29/2])
        
        pygame.display.flip()
        CLOCK.tick(10)
    pass

if __name__ == "__main__":
    main()
    pygame.quit()