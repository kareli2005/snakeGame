import random
import pygame
from pygame.locals import *
import time



class Snake:
    def __init__(self, screen, length):
        self.length = length
        self.display = screen
        self.size = 20
        self.x_snake = [self.size] * self.length
        self.y_snake = [self.size] * self.length
        self.direction = None
        self.directions = ["up", "down", "left", "right"]
        self.red = [255, 0, 0]
        self.x_apple = random.randint(0, 29) * 20 + 10
        self.y_apple = random.randint(0, 29) * 20 + 10
        self.score = 0

    def random_apple(self):
        pygame.draw.circle(self.display, self.red, [self.x_apple, self.y_apple], 10)
        changed_x = self.x_snake[0] + 10
        changed_y = self.y_snake[0] + 10
        while changed_x == self.x_apple and changed_y == self.y_apple:
            self.score += 1
            self.length += 1
            self.x_snake.append(-20)
            self.y_snake.append(-20)
            self.x_apple = random.randint(0, 29) * 20 + 10
            self.y_apple = random.randint(0, 29) * 20 + 10
            for i in range(self.length - 1, 1, -1):
                if self.x_apple == self.x_snake[i] + 10 and self.y_apple == self.y_snake[i] + 10:
                    self.draw_snake()
                    self.x_apple = random.randint(0, 29) * 20 + 10
                    self.y_apple = random.randint(0, 29) * 20 + 10
                    pygame.display.flip()

    def draw_snake(self):
        self.display.fill((0, 0, 0))
        green = [0, 255, 0]
        blue = [0, 0, 255]
        self.random_apple()
        for i in range(self.length):
            if i == 0:
                pygame.draw.rect(self.display, blue, [self.x_snake[i], self.y_snake[i], 20, 20])
            else:
                pygame.draw.rect(self.display, green, [self.x_snake[i], self.y_snake[i], 20, 20])
        pygame.display.flip()

    def snake_move(self, moving):

        if moving == "true":
            for i in range(self.length - 1, 0, -1):
                self.x_snake[i] = self.x_snake[i - 1]
                self.y_snake[i] = self.y_snake[i - 1]
            if self.direction == self.directions[0]:
                self.y_snake[0] -= self.size
            if self.direction == self.directions[1]:
                self.y_snake[0] += self.size
            if self.direction == self.directions[2]:
                self.x_snake[0] -= self.size
            if self.direction == self.directions[3]:
                self.x_snake[0] += self.size
            self.draw_snake()
        if moving == "false":
            i = 3
            print("You lose, try better next time!")
            print(f"Your score is: {self.score}")
            self.score = 0
            while i > 0:
                self.draw_snake()
                time.sleep(0.3)
                self.display.fill((0, 0, 0))
                pygame.display.flip()
                time.sleep(0.3)
                i -= 1
                self.direction = None
            self.length = 1
            self.x_snake = [self.size] * self.length
            self.y_snake = [self.size] * self.length
        if moving == "paused":
            pass


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((600, 600))
        self.display.fill((0, 0, 0))
        self.default_length = 1
        self.snake = Snake(self.display, self.default_length)
        self.running = True

    def game_over(self):
        for i in range(self.snake.length - 1, 0, -1):
            if self.snake.length > 1:
                if self.snake.x_snake[0] == self.snake.x_snake[i] and\
                        self.snake.y_snake[0] == self.snake.y_snake[i]:
                    self.snake.snake_move("false")
        if (self.snake.x_snake[0] < 0 or self.snake.x_snake[0] > 580) or \
                (self.snake.y_snake[0] < 0 or self.snake.y_snake[0] > 580):
            self.snake.snake_move("false")
        else:
            self.snake.snake_move("true")

    def game_win(self):
        if self.snake.length == 900:
            print("Congratulations, you won!")
            print(f"Your score is: {self.snake.score}")
            time.sleep(2)
            self.running = False

    def play(self):
        self.snake.draw_snake()
        self.game_over()
        self.game_win()

    def game_run(self):
        self.snake.draw_snake()
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_UP:
                        self.snake.direction = self.snake.directions[0]
                    if event.key == K_DOWN:
                        self.snake.direction = self.snake.directions[1]
                    if event.key == K_LEFT:
                        self.snake.direction = self.snake.directions[2]
                    if event.key == K_RIGHT:
                        self.snake.direction = self.snake.directions[3]
                    if event.key == K_p:
                        self.snake.snake_move("paused")
                elif event.type == pygame.QUIT:
                    self.running = False

            self.play()
            time.sleep(0.1)


game = Game()
game.game_run()
