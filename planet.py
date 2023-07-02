import pygame
import numpy as np
import os

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
WINDOW_CENTER = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
BG_COLOR = (10,10,10)

pygame.init()
pygame.display.set_caption("20190536 박수빈 - solar system")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
ufo = pygame.image.load(os.path.join(current_path, "ufo.png"))
ufo = pygame.transform.scale(ufo, (125, 70))
ufoRect= ufo.get_rect()
explosion = pygame.mixer.Sound("explosion.mp3")

def getRegularPolygonVertices(N, radius = 1):
    v = []
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = np.cos(rad) * radius
        y = np.sin(rad) * radius
        v.append([x,y])
    vnp = np.array(v)
    return vnp
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
def draw(M, points, color = (10,10,10), p0 = None, lineColor = (200,200,200)):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_new = (R @ points.T).T + t
    pygame.draw.polygon(screen, color, points_new)
    # if p0 is not None:
    #     pygame.draw.line(screen, lineColor, p0, points_new[0],2)


def main():
    angleS = 0
    angleE = 0
    angleM = 0

    angleJ = 0
    angleM1 = 0
    angleM2 = 0
    
    angleSE = 0 #sun - earth
    angleEM = 0 #earth - moon

    angleSJ = 0 #sun - jupiter
    angleJM1 = 0 #jupiter - moon1
    angleJM2 = 0 #jupiter - moon2

    distSE = 155
    distEM = 55

    distSJ = 280
    distJM1 = 70
    distJM2 = 50
    
    Eorbit = []
    Jorbit = []

    isRotating = False
    done = False
    ufo_tick = 0
    ufoRect.x = - ufo.get_width()
    ufoRect.y = - ufo.get_height()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_SPACE:
                    if not isRotating:
                        isRotating = True
                    else:
                        isRotating = False
                elif event.key == pygame.K_UP:
                    ufoRect.y -= 50
                elif event.key == pygame.K_DOWN:
                    ufoRect.y += 50
                elif event.key == pygame.K_LEFT:
                    ufoRect.x -= 50
                elif event.key == pygame.K_RIGHT:
                    ufoRect.x += 50

        screen.fill(BG_COLOR)
        if isRotating:
            ufo_tick += 1
            angleS += 7
            angleE += 3
            angleJ += 1

            angleM += 4
            angleM1 += 3
            angleM2 += 6
            angleSE += 10
            angleSJ += 3
            angleEM += 10
            
            angleJM1 += 8
            angleJM2 += 15

        #sun
        sun = getRegularPolygonVertices(20, 44)
        Msun = T3mat(WINDOW_CENTER[0], WINDOW_CENTER[1]) @ R3mat(angleS)
        
        pygame.draw.circle(screen, (255,195,0), WINDOW_CENTER, np.random.randint(55,63))
        pygame.draw.circle(screen, (255,125,0), WINDOW_CENTER, np.random.randint(45,55))
        draw(Msun, sun, (255,0,0), WINDOW_CENTER)

        #other planets' orbit
        for i in range(0, 7):
            if i!=2 or i!=4:
                pygame.draw.circle(screen, (70, 70, 70), WINDOW_CENTER, 70 + 9*(i+1)*(i+2), 1)
        
        #earth
        earth = getRegularPolygonVertices(18, 20)
        Mearth = T3mat(WINDOW_CENTER[0], WINDOW_CENTER[1]) @R3mat(angleSE) @ T3mat(distSE, 0) @ R3mat(angleE)
        

        Eorbit.append(Mearth[:2,2])
        if len(Eorbit) >=2:
            pygame.draw.lines(screen, (190,190,190), False, Eorbit, 1)
                
        draw(Mearth, earth, (35,130,230), Mearth[:2,2])

        #moon
        moon = getRegularPolygonVertices(18, 9)
        Mmoon = Mearth @ R3mat(-angleE) @R3mat(angleEM) @ T3mat(distEM,0) @ R3mat(angleM)
        draw(Mmoon, moon, (110, 100, 120), Mmoon[:2,2])

        #jupiter
        jupiter = getRegularPolygonVertices(18, 25)
        Mjupiter = T3mat(WINDOW_CENTER[0], WINDOW_CENTER[1]) @ R3mat(angleSJ) @ T3mat(-distSJ, 100) @ R3mat(angleJ)

        Jorbit.append(Mjupiter[:2,2])
        if len(Jorbit) >=2:
            pygame.draw.lines(screen, (190,190,190), False, Jorbit, 1)

        draw(Mjupiter, jupiter, (140,118,104), Mjupiter[:2,2])

        #moon1 - Io
        moon1 = getRegularPolygonVertices(18, 12)
        Mmoon1 = Mjupiter @ R3mat(-angleJ) @R3mat(angleJM1) @ T3mat(distJM1,0) @ R3mat(angleM1)
        draw(Mmoon1, moon1, (112,109,143), Mmoon1[:2,2])
        #moon2 - Ganymede
        moon2 = getRegularPolygonVertices(18, 8)
        Mmoon2 = Mjupiter @ R3mat(-angleJ) @R3mat(angleJM2) @ T3mat(distJM2,-distJM2/2) @ R3mat(angleM2)
        draw(Mmoon2, moon2, (72,59,40), Mmoon2[:2,2])
        
        if isRotating:
            ufoRect.x += ufo_tick / 100
            ufoRect.y += ufo_tick / 100
        ufoDist = np.sqrt((ufoRect.x + ufoRect.width/2 - WINDOW_CENTER[0])**2 + (ufoRect.y + ufoRect.height/2 - WINDOW_CENTER[1])**2)
        if ufoDist <= 50:
            explosion.play()
        else:
            screen.blit(ufo, (ufoRect.x, ufoRect.y))
        pygame.display.flip()
        clock.tick(30)
    pass

if __name__ == "__main__":
    main()
    pygame.quit()
