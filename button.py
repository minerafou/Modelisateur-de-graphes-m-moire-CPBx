import pygame
import draw_basic

class ButtonColor():
    def __init__(self, normal = (200, 200, 200), text = (30, 30, 30), over = (180, 180, 180), locked = (150, 150, 150)):
        self.normal = normal
        self.text = text
        self.over = over
        self.locked = locked
    
    def get_normal(self):
        return self.normal
    
    def get_text(self):
        return self.text
    
    def get_over(self):
        return self.over
    
    def get_locked(self):
        return self.locked

class Button():
    def __init__(self, x, y, w, h, text, color: ButtonColor, func = lambda x:x, font: pygame.font.Font = pygame.font.SysFont("arial", 30), locked = False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.func = func
        self.font = font
        self.locked = locked
    
    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.locked:
            draw_basic.draw_rect(screen, self.x, self.y, self.w, self.h, self.color.get_locked())
        if self.is_mouse_on(mouse_x, mouse_y):
            draw_basic.draw_rect(screen, self.x, self.y, self.w, self.h, self.color.get_over())
        else:
            draw_basic.draw_rect(screen, self.x, self.y, self.w, self.h, self.color.get_normal())
        
        draw_basic.draw_text(screen, self.x, self.y, self.w, self.h, self.color.get_text(), self.font, self.text)
    
    def lock(self):
        self.locked = True
    
    def unlock(self):
        self.locked = False
    
    def is_mouse_on(self, mouse_x, mouse_y):
        return self.x <= mouse_x < self.x + self.w and self.y <= mouse_y < self.y + self.h

    def check_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.is_mouse_on(mouse_x, mouse_y):
            self.func()
