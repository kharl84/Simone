import pygame
import numpy
import math
import random

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)
DARKBLUE = (0, 0, 155)
RED = (255, 0, 0)
DARKRED = (155, 0, 0)
YELLOW = (255, 255, 0)
DARKYELLOW = (155, 155, 0)
BGCOLOUR = BLACK

# Game settings
WIDTH = 640
HEIGHT = 500
FPS = 60
TITLE = "Simon Says"
BUTTON_SIZE = 200
ANIMATION_SPEED = 20
BEEP1 = 880
BEEP2 = 659
BEEP3 = 554
BEEP4 = 440

pygame.mixer.init()

# Class for game buttons
class Button:
    def __init__(self, x, y, colour):
        self.x, self.y = x, y
        self.colour = colour

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, BUTTON_SIZE, BUTTON_SIZE))

    def clicked(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + BUTTON_SIZE and self.y <= mouse_y <= self.y + BUTTON_SIZE

# Class for handling game audio
class Audio:
    def __init__(self, frequency: int):
        duration = 0.5
        bits = 16
        sample_rate = 44100
        total_samples = int(round(duration * sample_rate))
        data = numpy.zeros((total_samples, 2), dtype=numpy.int16)
        max_sample = 2 ** (bits - 1) - 1
        for sample in range(total_samples):
            sample_time = float(sample) / sample_rate
            for channel in range(2):
                data[sample][channel] = int(round(max_sample * math.sin(2 * math.pi * frequency * sample_time)))
        self.sound = pygame.sndarray.make_sound(data)
        self.current_channel = None

    def play(self):
        self.current_channel = pygame.mixer.find_channel(True)
        self.current_channel.play(self.sound)

# Class for UI elements
class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Consolas", 16)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))

# Main Game Class
class Game:
    DARKYELLOW = (155, 155, 0)  # Define the color
    DARKBLUE = (0, 0, 155)  # Define the color
    DARKRED = (155, 0, 0)  # Define the color
    DARKGREEN = (0, 155, 0)  # Define the color
    YELLOW = (255, 255, 0)  # Add the YELLOW attribute   

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.beeps = [Audio(BEEP1), Audio(BEEP2), Audio(BEEP3), Audio(BEEP4)]
        self.flash_colours = [YELLOW, BLUE, RED, GREEN]
        self.pattern = []  # Add the pattern attribute 1
        self.current_step = 0 # Add the current_step attribute 2
        self.score = 0  # Add the score attribute 3
        self.waiting_input = False  # Add the waiting_input attribute 4
        self.colours = [DARKYELLOW, DARKBLUE, DARKRED, DARKGREEN]
        self.high_score = self.get_high_score()

        

        # Initialize game buttons
        self.buttons = [
            Button(110, 50, DARKYELLOW),    # Top left button
            Button(330, 50, DARKBLUE),      # Top right button
            Button(110, 270, DARKRED),      # Bottom left button
            Button(330, 270, DARKGREEN),    # Bottom right button
        ]

    def get_high_score(self):
         with open("high_score.txt", "r") as file:
            score_str = file.read().strip()
            try:
                score = int(score_str)
            except ValueError:
                print(f"Error: '{score_str}' is not a valid integer.")
                score = 0  # or any default value you prefer
         return score                       

    def save_scores(self, new_score):
       scores = self.get_top_scores()

    # Add the new score to the list
       scores.append(new_score)

    # Sort the scores in descending order
       scores.sort(reverse=True)

    # Save the top 10 scores
       with open("high_score.txt", "w") as file:
         for score in scores[:10]:
            file.write(f"{score}\n")
 #initializenuevo game
    def new(self):
        self.waiting_input = False
        self.pattern = []
        self.current_step = 0
        self.score = 0
        self.high_score = self.get_high_score()

   
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.clicked(mouse_x, mouse_y):
                        self.clicked_button = button.colour

   #gameloop
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.clicked_button = None
            self.events()
            self.draw()
            self.update()
            

 
    def update(self):
        if not self.waiting_input:
            pygame.time.delay(1000)
            self.pattern.append(random.choice(self.colours))
            for button in self.pattern:
                self.button_animation(button)
                pygame.time.wait(200)
            self.waiting_input = True
            
        else:
        
            if self.clicked_button and self.clicked_button == self.pattern[self.current_step]:
                self.button_animation(self.clicked_button)
                self.current_step += 1

                if self.current_step == len(self.pattern):
                    self.score += 1
                    self.waiting_input = False
                    self.current_step = 0

            elif self.clicked_button and self.clicked_button != self.pattern[self.current_step]:
             self.game_over_animation()
             self.save_scores(self.score)
             self.playing = False   


    def button_animation(self, colour):
        for i in range(len(self.colours)):
            if self.colours[i] == colour:
                sound = self.beeps[i]
                flash_colour = self.flash_colours[i]
                button = self.buttons[i]

        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
        flash_surface = flash_surface.convert_alpha()
        r, g, b = flash_colour
        sound.play()
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, ANIMATION_SPEED * step):
                self.screen.blit(original_surface, (0, 0))
                flash_surface.fill((r, g, b, alpha))
                self.screen.blit(flash_surface, (button.x, button.y))
                pygame.display.update()
                self.clock.tick(FPS)       
        self.screen.blit(original_surface, (0, 0))

 
    def game_over_animation(self):
        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((self.screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
        for beep in self.beeps:
            beep.play()
        r, g, b = WHITE
        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    self.screen.blit(original_surface, (0, 0))
                    flash_surface.fill((r, g, b, alpha))
                    self.screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    self.clock.tick(FPS)



    def draw(self):
        self.screen.fill(BGCOLOUR)
        UIElement(170, 20, f" {str(self.score)}").draw(self.screen)

        # Display current score
        UIElement(20, 20, "Current Score:").draw(self.screen)
        UIElement(20, 40, str(self.score)).draw(self.screen)

        # Display top 10 scores
        UIElement(470,20,"Top 10 Scores:").draw(self.screen)
        top_scores = self.get_top_scores()
        for i, score in enumerate(top_scores):
            UIElement(540, 40 + i * 20, f"{i + 1}. {score}").draw(self.screen)

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.update()


    def get_top_scores(self):
     scores = []
     with open("high_score.txt", "r") as file:
        for line in file:
            score = line.strip()
            try:
                score = int(score)
            except ValueError:
                score = 0  # or any default value you prefer
            scores.append(score)
            if len(scores) == 10:
                break

    # Fill remaining slots with 0
     while len(scores) < 10:
        scores.append(0)

     return scores
   
                                                                   

if __name__ == "__main__":
     game = Game()
     while True:
        game.new()
        game.run()
