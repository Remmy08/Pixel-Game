import pygame

class DebugDisplay:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Courier', 16, bold=True)
    
    def show(self):
        if self.game.settings.SHOW_FPS:
            self._draw_text(f"FPS: {int(self.game.clock.get_fps())}", 10, 10)
        
        if self.game.settings.SHOW_POSITION:
            player = self.game.player.rect
            self._draw_text(f"Player: ({player.x}, {player.y})", 10, 30)
        
        # Информация о коллизиях
        self._draw_text(f"Collisions: {'ON' if self.game.settings.SHOW_COLLISIONS else 'OFF'} (F1)", 10, 50)
    
    def _draw_text(self, text, x, y):
        surface = self.font.render(text, True, self.game.settings.DEBUG_TEXT)
        self.game.screen.blit(surface, (x, y))