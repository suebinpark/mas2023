import pygame
import numpy as np

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_CENTER = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = BLACK

pygame.init()
pygame.display.set_caption("20190536 박수빈 - clock")
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
tickingSound = pygame.mixer.Sound("tick.mp3")
bellSound = pygame.mixer.Sound("bell.mp3")

def R3mat(deg):
    rad = np.deg2rad(deg)
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([[c, -s, 0],
                 [s, c, 0],
                 [0, 0, 1]],
                 dtype = 'float')
    return R
def T3mat(tx, ty):
    T = np.eye(3, dtype = 'float')
    T[0, 2] = tx
    T[1, 2] = ty
    return T

def getNeedlePoints(width, height, x = 0, y = 0):
    points = np.array([[x,     y],
                       [width, y],
                       [width, height],
                       [x,     height] ])
    return points

def getTransformedPoints(M, points):
    R = M[0:2, 0:2]
    t = M[0:2, 2]
    new_points = (R @ points.T).T + t
    return new_points

def drawNeedles(w, h, startPoint, angle, color):
    point1 = getNeedlePoints(w, h)
    M = T3mat(startPoint[0], startPoint[1]) @ R3mat(-90 + angle)
    point2 = getTransformedPoints(M, point1)
    pygame.draw.polygon(SCREEN, color, point2)

def main():
    done = False
    tick_sec = 0
    tick_min = 0
    tick_hour = 0
    
    while not done:
        tick_sec += 6
        tickingSound.play()
        if tick_sec >= 360:
            tick_sec = 0
            tick_min += 6
        if tick_min >= 360:
            tick_min = 0
            tick_hour += 6
            bellSound.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    done = True
                elif event.type == pygame.K_SPACE:
                    print("Space")
        
        #draw the clock
        SCREEN.fill(BG_COLOR)
        pygame.draw.circle(SCREEN, WHITE, WINDOW_CENTER, WINDOW_HEIGHT*0.4, 8) #200

        #초침
        sec_angle = tick_sec
        drawNeedles(160, 5, WINDOW_CENTER, sec_angle, (255, 0, 0))

        #분침 -> 초침이 한 바퀴 돌면 한 칸 움직임
        min_angle = tick_min
        drawNeedles(140, 7, WINDOW_CENTER, min_angle, (180, 180, 180))

        #시침
        hour_angle = tick_hour
        drawNeedles(80, 7, WINDOW_CENTER, hour_angle, WHITE)

        #center dot
        pygame.draw.circle(SCREEN, WHITE, WINDOW_CENTER, 10)

        pygame.display.flip()
        CLOCK.tick(1)
    pass

if __name__ == "__main__":
    main()
    pygame.quit()