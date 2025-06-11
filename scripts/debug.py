import pygame

class DebugDisplay:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Courier', 16, bold=True)
    
    def show(self, surface=None):
        # Если surface не указан, используем основной экран
        target_surface = surface if surface is not None else self.game.screen
        
        if self.game.settings.SHOW_FPS:
            self._draw_text(target_surface, f"FPS: {int(self.game.clock.get_fps())}", 10, 10)
        
        if self.game.settings.SHOW_POSITION:
            player = self.game.player.rect
            self._draw_text(target_surface, f"Player: ({player.x}, {player.y})", 10, 30)
            self._draw_text(target_surface, f"Player Rect: {player}", 10, 50)
            self._draw_text(target_surface, f"Player Pos: {self.game.player.position}", 10, 70)
        
        # Информация о коллизиях
        self._draw_text(target_surface, 
                       f"Collisions: {'ON' if self.game.settings.SHOW_COLLISIONS else 'OFF'} (F1)", 
                       10, 90)
    
    def _draw_text(self, surface, text, x, y):
        text_surface = self.font.render(text, True, self.game.settings.DEBUG_TEXT)
        surface.blit(text_surface, (x, y))
        
    def show_collisions(self, surface, camera):
        if not self.game.settings.SHOW_COLLISIONS:
            return
        
        for collision in self.game.tilemap.collisions:
            pygame.draw.rect(
                surface, 
                (255, 0, 0),
                camera.apply(collision),
                1
            )