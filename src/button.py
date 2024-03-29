class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hovered = False
    
    def draw_button(self, screen):
        if self.hovered:
            image_copy = self.image.copy()
            image_copy.set_alpha(220)
            screen.blit(image_copy, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, pos):
        if self.rect.collidepoint(pos):
            self.hovered = True
        else:
            self.hovered = False
    
    def selected(self, pos):
        if (pos[0] > self.rect.x and pos[0] < self.rect.x + self.rect.width) and (pos[1] > self.rect.y and pos[1] < self.rect.y + self.rect.height):
            return True
        return False