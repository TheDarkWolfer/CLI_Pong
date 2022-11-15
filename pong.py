import sys, time, argparse, os, random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
is_running = False
bounces = 0

def run(ball_speed, obstacle_count, paddle_lenght, paddle_color, ball_color, obstacle_color, sync=None, is_random=None, debug=None):
    if debug:
        print("ball_speed: ", ball_speed)
        print("obstacle_count: ", obstacle_count)
        print("paddle_lenght: ", paddle_lenght)
        print("paddle_color: ", paddle_color)
        print("ball_color: ", ball_color)
        print("obstacle_color: ", obstacle_color)
        print("screen_size: ", screen.get_size())
        print("sync: ", sync)
        print("is_random: ", is_random)
        print("debug: ", debug)
    colors = {"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255), "yellow":(255,255,0), "white":(255,255,255), "black":(10,10,10), "purple":(255,0,255), "orange":(255,165,0), "grey":(128,128,128), "cyan":(0,255,255)}
    global is_running, bounces
    class Display(pygame.sprite.Sprite):
        def __init__(self, x, y, type:str):
            global left_score, right_score
            pygame.sprite.Sprite.__init__(self)
            right_score = 0
            left_score = 0
            self.type = type
            self.display = str
            self.text = str
            self.font = pygame.font.SysFont("Arial", 50)
            self.x = x
            self.y = y
            self.image = self.font.render(str(self.display), True, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

        def update(self):
            if is_running:
                self.display = (f"{left_score} : {right_score}" if self.type == "s" else f"{bounces}")
            else:
                self.display = self.text
            self.image = self.font.render(str(self.display), True, (255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

    class Paddle(pygame.sprite.Sprite):
        def __init__(self, x, y, name):
            self.name = name
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, paddle_lenght))
            if paddle_color in colors:
                self.image.fill(colors[paddle_color])
            else:
                self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.speed = 10

        def update(self):
            keys = pygame.key.get_pressed()
            if self.name == "left":
                if keys:
                    if keys[pygame.K_w]:
                        self.rect.y -= self.speed
                        self.moving = True
                    if keys[pygame.K_s]:
                        self.moving = True
                        self.rect.y += self.speed
                    if keys[pygame.K_q]:
                        pygame.quit()
                        sys.exit()
                else:
                    self.moving = False
            elif self.name == "right":
                if keys:
                    if keys[pygame.K_DOWN]:
                        self.moving = True
                        self.rect.y += self.speed
                    if keys[pygame.K_UP]:
                        self.moving = True
                        self.rect.y -= self.speed
                else:
                    self.moving = False
            
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > 480:
                self.rect.bottom = 480

    class Ball(pygame.sprite.Sprite):
        def __init__(self, x, y, ball_speed):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((10, 10))
            if ball_color in colors:
                self.image.fill(colors[ball_color])
            else:
                self.image.fill((255,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.speed = ball_speed
            self.dx = 1
            self.dy = (1 if random.randint(0, 1) == 0 else -1)

        def update(self):
            global left_score, right_score, bounces
            self.rect.x += self.speed * self.dx
            self.rect.y += self.speed * self.dy

            if self.rect.top <= 0 or self.rect.bottom >= 480:
                self.dy *= -1

            if self.rect.left <= 0 or self.rect.right >= 640:
                self.dx *= -1

            if pygame.sprite.collide_rect(self, paddle1) or pygame.sprite.collide_rect(self, paddle2):
                bounces += 1
                self.dx *= -1
                if args.random:
                    self.dy = random.uniform(0.5, 2)

            for obstacle in obstacles:
                if pygame.sprite.collide_rect(self, obstacle):
                    bounces += 1
                    self.dx *= -1

            if self.rect.left <= 0:
                right_score += 1
                self.rect.center = (320, 240)
                time.sleep(.5)
            if self.rect.right >= 640:
                left_score += 1
                self.rect.center = (320, 240)
                time.sleep(.5)

        def reset(self):
            self.rect.center = (320, 240)
    
    class Obstacle(pygame.sprite.Sprite):
        def __init__(self, x, y, width, height):
            x, y, width, height = round(x), round(y), round(width), round(height)
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((width, height))
            if obstacle_color in colors:
                self.image.fill(colors[obstacle_color])
            else:
                self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    if args.sync == True:
        paddle1 = Paddle(10, 240, "right")
        paddle2 = Paddle(630, 240, "right")
    else:
        paddle1 = Paddle(10, 240, "left")
        paddle2 = Paddle(630, 240,"right")
    display = Display(320, 20, "s")
    bounces_display = Display(320, 460, "b")
    ball = Ball(340, 240, ball_speed)
    obstacles = pygame.sprite.Group()


    for i in range(obstacle_count):
        obstacles.add(Obstacle(320, 480 / (obstacle_count + 1) * (i + 1), 5, 640 / (obstacle_count + 1) / 5))


    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle1, paddle2, ball, display, bounces_display, obstacles)

    for i in range(3):
        ball.reset()
        display.text = f"Starting in {3-i}"
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        time.sleep(1)

    is_running = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(60)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", help="set the speed of the ball", type=int)
parser.add_argument("-o", "--obstacle", help="set the amount of obstacles on the field", type=int)
parser.add_argument("-p", "--paddle", help="set the lenght of the two paddles", type=int)
parser.add_argument("-pc", "--paddle_color", help="define the color of the paddles", type=str)
parser.add_argument("-bc", "--ball_color", help="define the color of the ball", type=str)
parser.add_argument("-oc", "--obstacles_color", help="define the color of the obstacles", type=str)
parser.add_argument("-y","--sync",help="sync the two paddles together", action="store_true")
parser.add_argument("-r", "--random", help="randomize the ball's bounce angle on each bounce", action="store_true")
parser.add_argument("-d", "--debug", help="show debug information", action="store_true")
args = parser.parse_args()

run(ball_speed=(args.speed if args.speed else 2),
obstacle_count=(args.obstacle if args.obstacle else 0), 
paddle_lenght=(args.paddle if args.paddle else 100), 
paddle_color=(args.paddle_color if args.paddle_color else "white"), 
ball_color=(args.ball_color if args.ball_color else "red"),
obstacle_color=(args.obstacles_color if args.obstacles_color else "white"),
sync=args.sync, 
is_random=args.random, 
debug=args.debug)