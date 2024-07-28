# Sofia Starinnova

import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# File to store the highest score
HIGHEST_SCORE_FILE = 'highest_score.txt'

# Get the absolute path of the current directory
base_path = os.path.dirname(os.path.abspath(__file__))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.fruits = []
        self.obstacles = []
        self.spawn_fruits()
        self.spawn_obstacles()
        self.score = 0
        self.highest_score = self.load_highest_score()
        self.background_images = [
            'images/background.jpg',
            'images/background2.jpg',
            'images/background3.jpg',
            'images/background4.jpg',
            'images/background5.jpg'
        ]
        self.background_index = 0
        self.background = self.load_background(self.background_images[self.background_index])
        self.eat_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds/eat.wav'))
        self.explode_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds/explosion.wav'))
        self.wall_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds/wall.wav'))
        self.plum_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds/new.wav'))
        self.power_up_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds/power_up.wav'))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds/game_over.wav'))
        self.start_screen_sound = pygame.mixer.Sound(os.path.join(base_path, 'sounds/start_screen.wav'))

        # Game running flag
        self.running = True
        self.power_up_active = False  # Flag to track if power-up is active
        self.power_up_duration = 0  # Duration of power-up effect in seconds
        self.power_up_countdown = 0  # Countdown for power-up effect

    def load_background(self, image_path):
        background = pygame.image.load(os.path.join(base_path, image_path)).convert_alpha()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        background.set_alpha(128)
        return background

    def generate_background(self):
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for _ in range(100):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(10, 50)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pygame.draw.circle(background, color, (x, y), radius)
        return background

    def change_background(self):
        if self.background_index < len(self.background_images) - 1:
            self.background_index += 1
            self.background = self.load_background(self.background_images[self.background_index])
        else:
            self.background = self.generate_background()

    def spawn_fruits(self):
        fruit_classes = [Apple, Orange, Plum, Bomb, PowerUp]
        self.fruits = [Bomb()]
        self.fruits += [random.choice(fruit_classes[:-1])() for _ in range(2)] 
        self.power_up = PowerUp()
        self.power_up.reposition()
        self.fruits.append(self.power_up)

    def spawn_obstacles(self):
        self.obstacles = [Obstacle() for _ in range(5)]

    def load_highest_score(self):
        if os.path.exists(HIGHEST_SCORE_FILE):
            with open(HIGHEST_SCORE_FILE, 'r') as file:
                return int(file.read())
        return 0

    def save_highest_score(self):
        with open(HIGHEST_SCORE_FILE, 'w') as file:
            file.write(str(self.highest_score))

    def show_start_screen(self):
        self.start_screen_sound.play()
        self.screen.fill((0, 150, 0))

        # Load a custom font with a smaller size
        font = pygame.font.Font('font/PrStart.ttf', 14)

        # Create the text objects
        title_text = font.render("Snake Game", True, BLACK)
        credit_text = font.render("By: Sofia Starinnova", True, BLACK)
        instruction_text1 = font.render("Be a snake and eat fruits.", True, BLACK)
        instruction_text2 = font.render("Watch out for the obstacles!", True, BLACK)
        start_text = font.render("Press any key to start!", True, BLACK)

        # Draw the text objects at the center of the screen
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
        self.screen.blit(credit_text, (SCREEN_WIDTH // 2 - credit_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(instruction_text1,
                         (SCREEN_WIDTH // 2 - instruction_text1.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(instruction_text2,
                         (SCREEN_WIDTH // 2 - instruction_text2.get_width() // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    self.start_screen_sound.stop()
                    self.game_loop()
    def show_game_over_screen(self):
        self.game_over_sound.play()
        self.screen.fill((223, 64, 64))
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over", True, BLACK)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        highest_score_text = font.render(f"Highest Score: {self.highest_score}", True, BLACK)
        restart_text = font.render("Press R to restart", True, BLACK)
        exit_text = font.render("Press Esc to exit", True, BLACK)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                          SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(highest_score_text, (SCREEN_WIDTH // 2 - highest_score_text.get_width() // 2,
                                              SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.running = False

    def game_loop(self):
        # Initialize tick speed variables
        default_tick_speed = 10
        power_up_tick_speed = 25

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.change_background()
                    else:
                        self.snake.change_direction(event.key)

            self.snake.move()

            if self.snake.check_self_collision():
                print("Snake ran into itself!")
                self.game_over_sound.play()
                self.running = False

            for fruit in self.fruits:
                if self.snake.check_collision(fruit.position):
                    if isinstance(fruit, Bomb):
                        self.explode_sound.play()
                        self.running = False
                    elif isinstance(fruit, Plum):
                        self.plum_sound.play()
                        self.score += fruit.points
                        self.snake.grow()
                        fruit.reposition()
                    elif isinstance(fruit, PowerUp):
                        self.power_up_sound.play()
                        self.score += fruit.points
                        self.snake.grow()
                        fruit.reposition()
                        self.power_up_duration = 7
                        self.power_up_active = True
                        self.snake.speed += 25
                        self.power_up_countdown = self.power_up_duration
                    else:
                        self.eat_sound.play()
                        self.score += fruit.points
                        self.snake.grow()
                        fruit.reposition()

            if self.snake.check_wall_collision(SCREEN_WIDTH, SCREEN_HEIGHT):
                print("Snake hit the wall!")
                self.wall_sound.play()
                self.running = False

            if self.snake.check_obstacle_collision(self.obstacles):
                print("Snake hit an obstacle!")
                self.game_over_sound.play()
                self.running = False

            self.screen.fill(WHITE)
            self.screen.blit(self.background, (0, 0))
            self.draw_walls()
            self.snake.draw(self.screen)
            for fruit in self.fruits:
                fruit.draw(self.screen)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

            self.display_score()
            self.display_power_up_timer()

            pygame.display.update()

            if self.power_up_active:
                self.power_up_countdown -= 1
                if self.power_up_countdown <= 0:
                    self.power_up_active = False
                    self.snake.speed -= 25
                    self.power_up_countdown = 0

            tick_speed = power_up_tick_speed if self.power_up_active else default_tick_speed
            self.clock.tick(tick_speed)

        if self.score > self.highest_score:
            self.highest_score = self.score
            self.save_highest_score()

        self.show_game_over_screen()

    def draw_walls(self):
        pygame.draw.rect(self.screen, BLACK, (0, 0, SCREEN_WIDTH, 10))
        pygame.draw.rect(self.screen, BLACK, (0, 0, 10, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, (0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10))
        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT))

    def display_score(self):
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        highest_score_text = font.render(f"Highest Score: {self.highest_score}", True, BLACK)
        self.screen.blit(score_text, [20, 20])
        self.screen.blit(highest_score_text, [20, 60])

    def display_power_up_timer(self):
        if self.power_up_active:
            font = pygame.font.SysFont(None, 35)
            timer_text = font.render(f"Power-Up: {self.power_up_countdown} seconds left", True, BLACK)
            self.screen.blit(timer_text, [20, 100])

    def restart_game(self):
        self.score = 0
        self.snake.reset()
        self.spawn_fruits()
        self.spawn_obstacles()
        self.running = True
        self.power_up_duration = 0
        self.power_up_countdown = 0
        self.game_loop()


class Snake:
    def __init__(self):
        self.size = 20
        self.body = [(100, 100)]
        self.direction = pygame.K_RIGHT
        self.speed = 10
        self.head_image = pygame.image.load(os.path.join(base_path, 'images/head.png'))
        self.head_image = pygame.transform.scale(self.head_image, (self.size, self.size))
        self.body_image = pygame.image.load(os.path.join(base_path, 'images/snake_part.png'))
        self.body_image = pygame.transform.scale(self.body_image, (self.size, self.size))

    def change_direction(self, key):
        if key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            if (key == pygame.K_LEFT and self.direction != pygame.K_RIGHT) or \
               (key == pygame.K_RIGHT and self.direction != pygame.K_LEFT) or \
               (key == pygame.K_UP and self.direction != pygame.K_DOWN) or \
               (key == pygame.K_DOWN and self.direction != pygame.K_UP):
                self.direction = key

    def check_self_collision(self):
        return self.body[0] in self.body[1:]
    def move(self):
        x, y = self.body[0]
        if self.direction == pygame.K_LEFT:
            x -= self.size
        elif self.direction == pygame.K_RIGHT:
            x += self.size
        elif self.direction == pygame.K_UP:
            y -= self.size
        elif self.direction == pygame.K_DOWN:
            y += self.size
        self.body.insert(0, (x, y))
        self.body.pop()

    def grow(self):
        self.body.insert(-1, self.body[-1])

    def check_collision(self, position):
        return self.body[0] == position

    def check_wall_collision(self, screen_width, screen_height):
        x, y = self.body[0]
        return x < 10 or x >= screen_width - 10 or y < 10 or y >= screen_height - 10

    def check_obstacle_collision(self, obstacles):
        for obstacle in obstacles:
            if self.body[0] == obstacle.position:
                return True
        return False

    def reset(self):
        self.body = [(100, 100)]
        self.direction = pygame.K_RIGHT
        self.speed = 10

    def draw(self, screen):
        for i, segment in enumerate(self.body):
            if i == 0:
                screen.blit(self.head_image, segment)
            else:
                screen.blit(self.body_image, segment)


class Fruit:
    def __init__(self, image_path, points):
        self.size = 20
        self.image = pygame.image.load(os.path.join(base_path, image_path))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.position = (0, 0)
        self.points = points
        self.reposition()

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def reposition(self):
        self.position = (random.randint(1, (SCREEN_WIDTH - self.size) // self.size) * self.size,
                         random.randint(1, (SCREEN_HEIGHT - self.size) // self.size) * self.size)


class Apple(Fruit):
    def __init__(self):
        super().__init__('images/apple.jpg', 10)


class Orange(Fruit):
    def __init__(self):
        super().__init__('images/orange.jpg', 20)


class Plum(Fruit):
    def __init__(self):
        super().__init__('images/plum.jpg', 30)


class Bomb(Fruit):
    def __init__(self):
        super().__init__('images/bomb.jpg', -100)


class PowerUp(Fruit):
    def __init__(self):
        super().__init__('images/power_up.jpg', 50)

    def reposition(self):
        self.position = (random.randint(1, (SCREEN_WIDTH - self.size) // self.size) * self.size,
                         random.randint(1, (SCREEN_HEIGHT - self.size) // self.size) * self.size)


class Obstacle:
    def __init__(self):
        self.size = 20
        self.image = pygame.image.load(os.path.join(base_path, 'images/obstacle.png'))
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.position = self.generate_position()

    def generate_position(self):
        return (random.randint(1, (SCREEN_WIDTH - self.size) // self.size) * self.size,
                random.randint(1, (SCREEN_HEIGHT - self.size) // self.size) * self.size)

    def draw(self, screen):
        screen.blit(self.image, self.position)


if __name__ == '__main__':
    game = Game()
    game.show_start_screen()

