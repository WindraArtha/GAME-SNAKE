import random
import os
import time
from pynput import keyboard
from colorama import Fore, Back, Style, init

# Inisialisasi Colorama
init()

class Snake:
    def __init__(self, y, x):
        self.body = [[y, x], [y, x - 1], [y, x - 2]]
        self.direction = "RIGHT"
        self.new_direction = "RIGHT"

    def move(self):
        head = self.body[0][:]
        if self.new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
        elif self.new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif self.new_direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif self.new_direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"

        if self.direction == "RIGHT":
            head[1] += 1
        elif self.direction == "LEFT":
            head[1] -= 1
        elif self.direction == "UP":
            head[0] -= 1
        elif self.direction == "DOWN":
            head[0] += 1
        self.body = [head] + self.body[:-1]

    def grow(self):
        tail = self.body[-1][:]
        self.body.append(tail)

    def change_direction(self, direction):
        self.new_direction = direction

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

class Food:
    def __init__(self, max_y, max_x):
        self.position = [random.randint(1, max_y - 2), random.randint(1, max_x - 2)]

    def spawn(self, max_y, max_x):
        self.position = [random.randint(1, max_y - 2), random.randint(1, max_x - 2)]

class Game:
    def __init__(self):
        self.max_y, self.max_x = 20, 40
        self.snake = Snake(self.max_y // 2, self.max_x // 2)
        self.food = Food(self.max_y, self.max_x)
        self.score = 0
        self.game_over = False

    def play(self):
        def on_press(key):
            if key == keyboard.Key.up:
                self.snake.change_direction("UP")
            elif key == keyboard.Key.down:
                self.snake.change_direction("DOWN")
            elif key == keyboard.Key.left:
                self.snake.change_direction("LEFT")
            elif key == keyboard.Key.right:
                self.snake.change_direction("RIGHT")

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        while not self.game_over:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.draw()
            self.snake.move()

            if self.snake.body[0] == self.food.position:
                self.snake.grow()
                self.food.spawn(self.max_y, self.max_x)
                self.score += 1

            head_y, head_x = self.snake.body[0]
            if head_y in [0, self.max_y - 1] or head_x in [0, self.max_x - 1] or self.snake.collides_with_self():
                self.game_over = True

            time.sleep(0.1)

        print("Game Over! Your final score is:", self.score)
        listener.stop()

    def draw(self):
        print(Back.GREEN + " " * self.max_x + Style.RESET_ALL)
        for y in range(1, self.max_y - 1):
            row = ""
            for x in range(self.max_x):
                if [y, x] == self.food.position:
                    row += Fore.RED + "*" + Style.RESET_ALL
                elif [y, x] in self.snake.body:
                    row += Fore.YELLOW + "#" + Style.RESET_ALL
                else:
                    row += " "
            print(Back.GREEN + " " + Style.RESET_ALL + row + Back.GREEN + " " + Style.RESET_ALL)
        print(Back.GREEN + " " * self.max_x + Style.RESET_ALL)

# Menjalankan permainan
game = Game()
game.play()
