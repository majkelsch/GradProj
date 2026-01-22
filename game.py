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

        self.clue_number = None
        self.actual_number = None
        self.debt = 50

        self.WAIT_EVENT = pygame.USEREVENT + 100


    
    def generate_numbers(self):
        for obj in self.objects:
            if isinstance(obj, objects.Button) and obj.action == self.generate_numbers:
                obj.disabled = True
        self.actual_number = random.randint(1,20)
        self.clue_number = random.randint(1,20)
        while self.actual_number == self.clue_number:
            self.clue_number = random.randint(1,20)
        print(self.actual_number, self.clue_number)
        for obj in self.objects:
            if isinstance(obj, objects.ClueDisplay):
                obj.set_text(self.clue_number)


    def reset_round(self):
        self.clue_number = None
        self.actual_number = None
        for obj in self.objects:
            if isinstance(obj, objects.ClueDisplay):
                obj.set_text("ROLL")
                obj.text_color = (255,255,255)
            if isinstance(obj, objects.Button) and obj.action == self.generate_numbers:
                obj.disabled = False




    def guess_fail(self):
        for obj in self.objects:
            if isinstance(obj, objects.ClueDisplay):
                obj.text_color = (255,0,0)
            if isinstance(obj, objects.Button) and obj.action == self.generate_numbers:
                obj.disabled = True

        self.temp_disp.set_value(0)

        pygame.time.set_timer(self.WAIT_EVENT, 1500)
        self.waiting_for_reset = True


    def guess_success(self):
        for obj in self.objects:
            if isinstance(obj, objects.ClueDisplay):
                obj.text_color = (0,255,0)
            if isinstance(obj, objects.Button) and obj.action == self.generate_numbers:
                obj.disabled = True
        self.temp_disp.set_value(int(self.temp_disp.value)+1)

        pygame.time.set_timer(self.WAIT_EVENT, 1500)
        self.waiting_for_reset = True

    def check_guess(self, guess_type):
        if self.clue_number is not None and self.actual_number is not None:
            if guess_type == "gt":
                if self.actual_number > self.clue_number:
                    self.guess_success()
                else:
                    self.guess_fail()
            elif guess_type == "lt":
                if self.actual_number < self.clue_number:
                    self.guess_success()
                else:
                    self.guess_fail()


    def begin(self):
        """Initial setup before the game loop starts."""
        
        clue = objects.ClueDisplay(pos=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2), size=(250, 250), text="ROLL", font=pygame.font.SysFont('Arial', 32))
        self.objects.append(clue)


        stored = objects.LabelDisplay(pos=(settings.SCREEN_WIDTH//2+175, settings.SCREEN_HEIGHT//2+75), size=(100, 100), label="STORED", value="0", font=pygame.font.SysFont('Arial', 16), bg_image_path="assets/clue_display.png")
        self.stored_disp = stored
        self.objects.append(stored)

        temporary = objects.LabelDisplay(pos=(settings.SCREEN_WIDTH//2+175, settings.SCREEN_HEIGHT//2-75), size=(100, 100), label="TEMPORARY", value="0", font=pygame.font.SysFont('Arial', 16), bg_image_path="assets/clue_display.png")
        self.temp_disp = temporary
        self.objects.append(temporary)

        pay = objects.LabelDisplay(pos=(100, 75), size=(200, 150), label="PAY WHAT YOU OWE", value=str(self.debt), font=pygame.font.SysFont('Arial', 16), bg_image_path="assets/clue_display.png")
        self.pay_display = pay
        self.objects.append(pay)

        button = objects.Button(pos=(settings.SCREEN_WIDTH//2-175,settings.SCREEN_HEIGHT//2), size=(100,70), text="Roll", font=pygame.font.SysFont('Arial', 32), bg_color=(50,50,50), action=self.generate_numbers, bg_image_path="assets/btn_blank.png")
        self.objects.append(button)

        button_gt = objects.Button(pos=(settings.SCREEN_WIDTH//2-75, settings.SCREEN_HEIGHT//2+175), size=(100,70), text="Greater", font=pygame.font.SysFont('Arial', 16), bg_color=(50,50,50), action=lambda: self.check_guess("gt"), bg_image_path="assets/btn_blank.png")
        self.objects.append(button_gt)
        button_lt = objects.Button(pos=(settings.SCREEN_WIDTH//2+75, settings.SCREEN_HEIGHT//2+175), size=(100,70), text="Lower", font=pygame.font.SysFont('Arial', 16), bg_color=(50,50,50), action=lambda: self.check_guess("lt"), bg_image_path="assets/btn_blank.png")
        self.objects.append(button_lt)

        slider = objects.SliderY(pos=(settings.SCREEN_WIDTH//2+250, settings.SCREEN_HEIGHT//2), knob_radius=10, line_thickness=10, size=(50,250))
        self.transfer_slider = slider
        self.objects.append(slider)

        pay_slider = objects.SliderY(pos=(settings.SCREEN_WIDTH//2+300, settings.SCREEN_HEIGHT//2), knob_radius=10, line_thickness=10, size=(50,250))
        self.pay_slider = pay_slider
        self.objects.append(pay_slider)

        pass


    def intro(self):
        timer_interval = 5000
        timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(timer_event , timer_interval)

        intro_msg = objects.LabelDisplay(pos=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2), size=(400, 400), label="_GRADPROJ_", value="Inspired by FLATHEAD @ Tim Oxton", bg_image_path="assets/main_screen.png")

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == timer_event:
                    run = False

            # INTRO
            self.screen.fill((0, 0, 0))
            intro_msg.draw(self.screen)
            pygame.display.flip()
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

            elif event.type == self.WAIT_EVENT and getattr(self, 'waiting_for_reset', False):
                # Timer fired – reset the round
                pygame.time.set_timer(self.WAIT_EVENT, 0)
                self.reset_round()
                self.waiting_for_reset = False

            for obj in self.objects:
                obj.handle_event(event) 

    def update_queue(self):
        self.sprite_objects.update()
        [obj.update() for obj in self.objects]

        if self.transfer_slider.value == 100:
            self.stored_disp.set_value(int(self.stored_disp.value) + int(self.temp_disp.value))
            self.temp_disp.set_value("0")

        if self.pay_slider.value == 100:
            self.debt = self.debt - int(self.stored_disp.value)
            self.stored_disp.set_value(str(0))
            self.pay_display.set_value(str(self.debt))

    def render_queue(self):
        self.screen.fill((0, 0, 0))
        #
        self.sprite_objects.draw(self.screen)
        [obj.draw(self.screen) for obj in self.objects]
        #
        pygame.display.flip()



    

if __name__ == "__main__":
    game = Game()
    #game.intro()
    game.begin()
    game.run()