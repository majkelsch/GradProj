import pygame
import settings
import random
import math

pygame.font.init()




class ClueDisplay():
    def __init__(self, pos, size, *, text="", font=None, text_color=(255, 255, 255)):
        """
        :param pos: (x, y) tuple for the top‑left corner.
        :param size: (width, height) tuple.
        :param text: Text to display on the button.
        :param font: pygame.font.Font instance. If None, default font is used.
        :param text_color: RGB colour of the text.
        """

        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = pos
        self.size = size

        self.text = text
        self.font = font
        self.text_color = text_color

        

    def draw(self, surface):
        """Blit the button onto another surface."""

        # ---- Text setup ----------------------------------------------------
        if self.font is None:
            self.font = pygame.font.SysFont(None, 24)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # ---- Background setup ---------------------------------------------
        bg_image_path = "assets/main_screen.png"
        if bg_image_path:
            img = pygame.image.load(bg_image_path).convert_alpha()
            self.bg_surf = pygame.transform.smoothscale(img, self.size)
        else:  # fallback to a light gray if image is not supplied
            self.bg_surf = pygame.Surface(self.size)
            self.bg_surf.fill((200, 200, 200))



        surface.blit(self.bg_surf, self.rect.topleft)
        surface.blit(self.text_surf, self.text_rect)

    def set_text(self, new_text):
        self.text = str(new_text)

    def roll_number(self):
        self.text = str(random.randint(1,16))

    def handle_event(self, event):
        pass

    def update(self):
        pass



class LabelDisplay():
    def __init__(self, pos, size, *, label="", value="", font=None, text_color=(255, 255, 255), bg_image_path=None):
        """
        :param pos: (x, y) tuple for the top‑left corner.
        :param size: (width, height) tuple.
        :param text: Text to display on the button.
        :param font: pygame.font.Font instance. If None, default font is used.
        :param text_color: RGB colour of the text.
        """

        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = pos
        self.size = size

        self.label = label
        self.value = value
        self.font = font
        self.text_color = text_color
        self.bg_image_path = bg_image_path

        

    def draw(self, surface):
        """Blit the button onto another surface."""

        # ---- Label setup ----------------------------------------------------
        if self.font is None:
            self.font = pygame.font.SysFont(None, 24)
        self.label_surf = self.font.render(self.label, True, self.text_color)
        self.label_rect = self.label_surf.get_rect(center=self.rect.center)

        # ---- Value setup ----------------------------------------------------
        if self.font is None:
            self.font = pygame.font.SysFont(None, 12)
        self.value_surf = self.font.render(self.value, True, self.text_color)
        self.value_rect = self.value_surf.get_rect(center=(self.rect.centerx, self.rect.centery+25))

        # ---- Background setup ---------------------------------------------
        if self.bg_image_path:
            img = pygame.image.load(self.bg_image_path).convert_alpha()
            self.bg_surf = pygame.transform.smoothscale(img, self.size)
        else:  # fallback to a light gray if image is not supplied
            self.bg_surf = pygame.Surface(self.size)
            self.bg_surf.fill((200, 200, 200))



        surface.blit(self.bg_surf, self.rect.topleft)
        surface.blit(self.label_surf, self.label_rect)
        surface.blit(self.value_surf, self.value_rect)

    def set_label(self, new_label):
        self.label = str(new_label)

    def set_value(self, new_value):
        self.value = str(new_value)

    def handle_event(self, event):
        pass

    def update(self):
        pass








class Button():
    def __init__(self, pos, size, *, text="", font=None, text_color=(255, 255, 255), bg_color=None, bg_image_path=None, action=lambda: None, disabled=False):
        """
        :param pos: (x, y) tuple for the top‑left corner.
        :param size: (width, height) tuple.
        :param text: Text to display on the button.
        :param font: pygame.font.Font instance. If None, default font is used.
        :param text_color: RGB colour of the text.
        :param bg_color: Solid background colour (RGB). Ignored if an image
                         path is provided.
        :param bg_image_path: Path to a PNG/JPG that will be stretched to the
                             button size. If None, a solid colour is used.
        :param action: Function to call when the button is clicked.
        """

        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = pos
        self.text = text

        # ---- Text setup ----------------------------------------------------
        if font is None:
            font = pygame.font.SysFont(None, 24)
        self.text_surf = font.render(self.text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # ---- Background setup ---------------------------------------------
        if bg_image_path:
            img = pygame.image.load(bg_image_path).convert_alpha()
            self.bg_surf = pygame.transform.smoothscale(img, size)
        elif bg_color:
            self.bg_surf = pygame.Surface(size)
            self.bg_surf.fill(bg_color)
        else:  # fallback to a light gray if nothing supplied
            self.bg_surf = pygame.Surface(size)
            self.bg_surf.fill((200, 200, 200))

        # ---- Action -------------------------------------------------------
        self.action = action
        self.disabled = disabled

    def draw(self, surface):
        """Blit the button onto another surface."""
        surface.blit(self.bg_surf, self.rect.topleft)
        surface.blit(self.text_surf, self.text_rect)

    def handle_event(self, event):
        """
        Call this from your main loop's event handler.
        If the mouse clicks inside the button, run the action.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.disabled:
            if self.rect.collidepoint(event.pos):
                #print(f"Button '{self.text}' clicked")
                self.action()

    def update(self):
        pass













class Slider:
    def __init__(self, pos, knob_radius, line_thickness, size, min_val=0, max_val=100, start_val=0):
        """
        :param pos: (x, y) tuple for the top-left corner.
        :param size: (width, height) tuple.
        :param min_val: Minimum value.
        :param max_val: Maximum value.
        :param start_val: Starting value.
        """


        # Position & size
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = pos
        self.size = size

        self.knob_radius = knob_radius
        self.line_thickness = line_thickness

        # Value range
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val if start_val is not None else (min_val + max_val) // 2

        # Knob attributes
        self.knob_radius = knob_radius
        self.knob_pos = self._value_to_position(self.value)

        # Interaction state
        self.dragging = False

        self.target_value = self.value          
        self.spring_speed = 5                  

    def _value_to_position(self, val):
        """Convert a slider value to an x-coordinate."""
        ratio = (val - self.min_val) / (self.max_val - self.min_val)
        return int(self.rect.x + ratio * self.rect.width)

    def _position_to_value(self, pos_x):
        """Convert an x-coordinate back to a slider value."""
        rel_x = max(0, min(pos_x - self.rect.x, self.rect.width))
        ratio = rel_x / self.rect.width
        return int(self.min_val + ratio * (self.max_val - self.min_val))

    def update_knob_position(self):
        self.knob_pos = self._value_to_position(self.value)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the knob was clicked
            mouse_pos = event.pos
            if (mouse_pos[0] - self.knob_pos) ** 2 + (mouse_pos[1] - self.rect.centery) ** 2 <= self.knob_radius ** 2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.target_value = self.min_val
                
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update value based on mouse movement
            new_val = self._position_to_value(event.pos[0])
            self.value = max(self.min_val, min(new_val, self.max_val))
            self.update_knob_position()

    def draw(self, surface):
        # Draw track
        pygame.draw.line(surface, (200, 200, 200), (self.rect.x, self.rect.centery), (self.rect.x+self.rect.width, self.rect.centery), self.line_thickness)
        #pygame.draw.rect(surface, (200, 200, 200), self.rect, self.line_thickness)

        # Draw knob
        pygame.draw.circle(surface, (150, 0, 0), (self.knob_pos, self.rect.centery), self.knob_radius)
        
        

    def update(self):
        """Call once per frame to move toward the target."""
        if not self.dragging:
            # Move the current value a little closer to the target
            diff = self.target_value - self.value
            if abs(diff) > 0.5:                     # stop when close enough
                step = diff / self.spring_speed     # smaller steps → smoother
                self.value += step
                self.update_knob_position()

        if self.value == 100:
            print("DUMP")






class SliderY:
    def __init__(self, pos, knob_radius, line_thickness, size, min_val=0, max_val=100, start_val=0):
        """
        :param pos: (x, y) tuple for the top-left corner.
        :param size: (width, height) tuple.
        :param min_val: Minimum value.
        :param max_val: Maximum value.
        :param start_val: Starting value.
        """


        # Position & size
        self.rect = pygame.Rect(0, 0, *size)
        self.rect.center = pos
        self.size = size

        self.knob_radius = knob_radius
        self.line_thickness = line_thickness

        # Value range
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val if start_val is not None else (min_val + max_val) // 2

        # Knob attributes
        self.knob_radius = knob_radius
        self.knob_pos = self._value_to_position(self.value)

        # Interaction state
        self.dragging = False

        self.target_value = self.value          
        self.spring_speed = 5                  

    def _value_to_position(self, val):
        """Convert a slider value to an y-coordinate."""
        ratio = (val - self.min_val) / (self.max_val - self.min_val)
        return int(self.rect.y + ratio * self.rect.height)

    def _position_to_value(self, pos_y):
        """Convert an y-coordinate back to a slider value."""
        rel_y = max(0, min(pos_y - self.rect.y, self.rect.height))
        ratio = rel_y / self.rect.height
        return int(self.min_val + ratio * (self.max_val - self.min_val))

    def update_knob_position(self):
        self.knob_pos = self._value_to_position(self.value)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the knob was clicked
            mouse_pos = event.pos
            if (mouse_pos[0] - self.rect.centerx) ** 2 + (mouse_pos[1] - self.knob_pos) ** 2 <= self.knob_radius ** 2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.target_value = self.min_val
                
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update value based on mouse movement
            new_val = self._position_to_value(event.pos[1])
            self.value = max(self.min_val, min(new_val, self.max_val))
            self.update_knob_position()

    def draw(self, surface):
        # Draw track
        pygame.draw.line(surface, (200, 200, 200), (self.rect.centerx, self.rect.y), (self.rect.centerx, self.rect.y + self.rect.height), self.line_thickness)
        #pygame.draw.rect(surface, (200, 200, 200), self.rect, self.line_thickness)

        # Draw knob
        pygame.draw.circle(surface, (150, 0, 0), (self.rect.centerx, self.knob_pos), self.knob_radius)
        
        

    def update(self):
        """Call once per frame to move toward the target."""
        if not self.dragging:
            # Move the current value a little closer to the target
            diff = self.target_value - self.value
            if abs(diff) > 0.5:                     # stop when close enough
                step = diff / self.spring_speed     # smaller steps → smoother
                self.value += step
                self.update_knob_position()