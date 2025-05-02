import pygame
from entities import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.surfarray.use_arraytype('numpy')

        self.delta_time = 0
        self.canvas = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Electromagnetism")

        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.bindings = {
            "up": pygame.K_w,
            "left": pygame.K_a,
            "down": pygame.K_s,
            "right": pygame.K_d,
            "interact": pygame.K_SPACE
        }
        self.controls = {
            "up": False,
            "left": False,
            "down": False,
            "right": False,
            "interact": False
        }
        self.player = Player()
        Charge(-100, np.array([200, 200], dtype=float))
        Charge(100, np.array([300, 300], dtype=float))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            for control in self.controls.keys():
                self.controls[control] = keys[self.bindings[control]]

            self.delta_time = self.clock.tick(self.FPS) / 1000
            self.canvas.fill((0, 0, 0))
            self.player.tick(self.controls["up"], self.controls["right"], self.controls["down"], self.controls["left"], self.delta_time)
            self.player.render(self.canvas)
            for renderable in Renderable.renderables:
                if renderable != self.player:
                    renderable.tick(self.delta_time)
                    renderable.render(self.canvas)
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()