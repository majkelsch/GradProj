import pygame
import settings
import objects
import debug
import random
import time



class Game:
    """Base class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.sprite_objects = pygame.sprite.Group()
        self.objects = []

        self.clue_number = 0
        self.actual_number = 0


    
    def generate_numbers(self):
        self.actual_number = random.randint(1,20)
        self.clue_number = random.randint(1,20)
        while self.actual_number == self.clue_number:
            self.clue_number = random.randint(1,20)
        print(self.actual_number, self.clue_number)
        for obj in self.objects:
            if isinstance(obj, objects.ClueDisplay):
                obj.set_text(self.clue_number)


    def check_guess(self, guess_type):
        if guess_type == "gt":
            print("Guessing GT")
            if self.actual_number > self.clue_number:
                self.temp_disp.set_value(int(self.temp_disp.value)+1)
            else:
                print("NAH")
        elif guess_type == "lt":
            print("Guessing LT")
            if self.actual_number < self.clue_number:
                self.temp_disp.set_value(int(self.temp_disp.value)+1)
            else:
                print("NAH")


    def begin(self):
        """Initial setup before the game loop starts."""
        
        clue = objects.ClueDisplay(pos=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2), size=(200, 150), text="ROLL", font=pygame.font.SysFont('Arial', 32))
        self.objects.append(clue)


        stored = objects.LabelDisplay(pos=(settings.SCREEN_WIDTH//2-100, 75), size=(200, 150), label="STORED", value="0", font=pygame.font.SysFont('Arial', 32))
        self.stored_disp = stored
        self.objects.append(stored)

        temporary = objects.LabelDisplay(pos=(settings.SCREEN_WIDTH//2+100, 75), size=(200, 150), label="TEMPORARY", value="0", font=pygame.font.SysFont('Arial', 32))
        self.temp_disp = temporary
        self.objects.append(temporary)

        pay = objects.LabelDisplay(pos=(100, 75), size=(200, 150), label="PAY WHAT YOU OWE", value="50", font=pygame.font.SysFont('Arial', 32))
        self.pay_display = pay
        self.objects.append(pay)

        button = objects.Button(pos=(50,settings.SCREEN_HEIGHT//2), size=(100,100), text="Roll", font=pygame.font.SysFont('Arial', 32), bg_color=(50,50,50), action=self.generate_numbers)
        self.objects.append(button)

        button_gt = objects.Button(pos=(settings.SCREEN_WIDTH-50, settings.SCREEN_HEIGHT//2-50), size=(100,100), text="Greater", font=pygame.font.SysFont('Arial', 16), bg_color=(50,50,50), action=lambda: self.check_guess("gt"))
        self.objects.append(button_gt)
        button_lt = objects.Button(pos=(settings.SCREEN_WIDTH-50, settings.SCREEN_HEIGHT//2+50), size=(100,100), text="Lower", font=pygame.font.SysFont('Arial', 16), bg_color=(50,50,50), action=lambda: self.check_guess("lt"))
        self.objects.append(button_lt)

        slider = objects.Slider(pos=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2+100), knob_radius=10, line_thickness=10, size=(200, 50))
        self.transfer_slider = slider
        self.objects.append(slider)
        pass


    def intro(self):
        print("INTRO")
        i = 0
        intro_msg = objects.LabelDisplay(pos=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2), size=(200, 150), label="GRADPROJ", value="Inspired by FLATHEAD @ Tim Oxton")
        while i != 5000:
            self.screen.fill((0, 0, 0))
            intro_msg.draw(self.screen)
            pygame.display.flip()
            i+=1
        pass



    def run(self):
        """Game loop / Update each frame"""
        while self.running:
            self.event_queue()
            self.update_queue()
            self.render_queue()
            self.clock.tick(60)
        pygame.quit()

    def event_queue(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            for obj in self.objects:
                obj.handle_event(event) 

    def update_queue(self):
        self.sprite_objects.update()
        [obj.update() for obj in self.objects]

        if self.transfer_slider.value == 100:
            self.stored_disp.set_value(int(self.stored_disp.value) + int(self.temp_disp.value))
            self.temp_disp.set_value("0")
        pass

    def render_queue(self):
        self.screen.fill((0, 0, 0))
        #
        self.sprite_objects.draw(self.screen)
        [obj.draw(self.screen) for obj in self.objects]
        #
        pygame.display.flip()



    

if __name__ == "__main__":
    game = Game()
    game.intro()
    game.begin()
    game.run()