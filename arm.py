import pygame
import numpy as np

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
BG_COLOR = (230,230,230)
BLACK = (0,0,0)

pygame.init()
pygame.display.set_caption("20190536 박수빈 - two arm system")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def getRectangle(width, height, x = 0, y = 0):
    points = np.array([[x,     y],
                       [width, y],
                       [width, height],
                       [x,     height] ])
    return points

def R3mat(deg):
    radian = np.deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s, 0],
                  [s, c, 0],
                  [0, 0, 1]],
                  dtype = 'float')
    return R
def T3mat(tx, ty):
    T = np.array([[1, 0, tx],
                  [0, 1, ty],
                  [0, 0, 1]],
                  dtype = 'float')
    return T

def draw(M, points, color = BLACK, lineWidth = 2):
    R = M[0:2, 0:2]
    t = M[0:2, 2]
    points_transformed = (R @ points.T).T + t
    pygame.draw.polygon(screen, color, points_transformed, lineWidth)

def joint(center):
    pygame.draw.circle(screen, BLACK, center, 4, 2)
    pygame.draw.circle(screen, BLACK, center, 10, 2)

def transform(w, h, gap, angle, h2):
    return T3mat(w, 0) @ T3mat(0, h/ 2.) @ T3mat(gap, 0) @ R3mat(angle) @ T3mat(0, -h2/ 2.)

def main():
    center1 = [50., 50.]
    width1 = np.random.uniform(60, 180)
    height1 = np.random.uniform(30, 50)
    rect1 = getRectangle(width1, height1)
    width2 = np.random.uniform(60, 180)
    height2 = np.random.uniform(30, 50)
    rect2 = getRectangle(width2, height2)
    width3 = np.random.uniform(60, 180)
    height3 = np.random.uniform(30, 50)
    rect3 = getRectangle(width3, height3)
    angle1 = 30
    angle2 = -30
    angle3 = 20

    gap12 = np.random.randint(25., 60.)
    gap23 = np.random.randint(25., 60.)
    gap34 = 30
    gripperLine = 25
    angleRoller = 0
    done = False

    while not done:
        angleRoller += 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_1:
                    angle1 += 5
                elif event.key == pygame.K_2:
                    angle1 -= 5
                elif event.key == pygame.K_3:
                    angle2 += 5
                elif event.key == pygame.K_4:
                    angle2 -= 5
                elif event.key == pygame.K_5:
                    angle3 += 5
                elif event.key == pygame.K_6:
                    angle3 -= 5
                elif event.key == pygame.K_UP:
                    if gripperLine >= 8:
                        gripperLine -= 8
                    else:
                        gripperLine = 0
                elif event.key == pygame.K_DOWN:
                    gripperLine += 8

        screen.fill(BG_COLOR)

        M1 = np.eye(3) @ T3mat(center1[0], center1[1]) @ R3mat(angle1) @ T3mat(0, -height1/2.)
        draw(M1, rect1, BLACK)
        M2 = M1 @ transform(width1, height1, gap12, angle2, height2)
        draw(M2, rect2, BLACK)
        M3 = M2 @ transform(width2, height2, gap23, angle3, height3)
        draw(M3, rect3, BLACK)
        
        pygame.draw.line(screen, BLACK, [0,0], [center1[0], center1[1]],3)
        joint(center1)

        C = M1 @T3mat(width1, 0) @ T3mat(0, height1/ 2.)
        center2 = C[0:2, 2]
        joint(center2)
        C = C @ T3mat(gap12, 0)
        center3 = C[0:2, 2]
        joint(center3)
        pygame.draw.line(screen, BLACK, center2, center3, 3)

        C2 = M2 @T3mat(width2, 0) @ T3mat(0, height2/ 2.)
        center4 = C2[0:2, 2]
        joint(center4)
        C2 = C2 @ T3mat(gap23, 0)
        center5 = C2[0:2, 2]
        joint(center5)
        pygame.draw.line(screen, BLACK,center4, center5, 3)

        C3 = M3 @ T3mat(width3, 0) @ T3mat(0, height3/ 2.)
        center6 = C3[0:2, 2]
        joint(center6)

        C3 = C3 @ T3mat(gap34, 0)
        center7 = C3[0:2, 2]
        joint(center7)
        pygame.draw.line(screen, BLACK, center6, center7, 3)

        center8 = [center7[0], center7[1] + gripperLine]
        joint(center8)
        pygame.draw.line(screen, BLACK, center7, center8,3)

        center9 = [center8[0], center8[1]+25]
        pygame.draw.line(screen, BLACK, center8, center9,3)

        gripDist = 15
        keys = pygame.key.get_pressed() #continuous press
        if keys[pygame.K_SPACE]:
            if gripDist == 15:
                gripDist = 25
            elif gripDist == 25:
                gripDist = 15

        pygame.draw.line(screen, BLACK, [center9[0]-gripDist, center9[1]], [center9[0]+gripDist, center9[1]],3)
        pygame.draw.line(screen, BLACK, [center9[0]-gripDist, center9[1]], [center9[0]-gripDist, center9[1]+20],3)
        pygame.draw.line(screen, BLACK, [center9[0]+gripDist, center9[1]], [center9[0]+gripDist, center9[1]+20],3)

        pygame.display.flip()
        clock.tick(30)
    pass

if __name__ == "__main__":
    main()
    pygame.quit()