import pygame

def draw_rect(screen, x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect)

def draw_text(screen, x, y, w, h, color, font, text, align = None):
    rendered_text = font.render(text, True, color)  # White text
    text_rect = screen.get_rect()

    tw, th = font.size(text)

    if align == None or True:
        cx = int(x + w / 2) - tw / 2
        cy = int(y + h / 2) - th / 2
        rect = cx, cy, tw, th

    screen.blit(rendered_text, rect)

def draw_circle(screen, color, pos, radius):
    pygame.draw.circle(screen, color, pos, radius)

def draw_line(screen, color, start_pos, end_pos, width=1):
    pygame.draw.line(screen, color, start_pos, end_pos, width)  