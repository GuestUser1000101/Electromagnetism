import pygame
from entities import *

class KeyState:
    def __init__(self):
        self.is_held = False
        self.is_released = False
        self.is_pressed = False

class Game:
    def __init__(self):
        pygame.init()
        pygame.surfarray.use_arraytype('numpy')

        self.delta_time = 0
        self.WIDTH, self.HEIGHT = 500, 500
        self.canvas = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Electromagnetism")

        self.running = True
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.bindings = {
            pygame.K_w: "up",
            pygame.K_a: "left",
            pygame.K_s: "down",
            pygame.K_d: "right",
            pygame.K_SPACE: "interact"
        }
        self.controls = {
            "up": KeyState(),
            "left": KeyState(),
            "down": KeyState(),
            "right": KeyState(),
            "interact": KeyState()
        }
        self.player = Player()
        Charge(0, np.array([250, 250], dtype=float))
        Charge(30, np.array([200, 200], dtype=float))
        Charge(60, np.array([220, 400], dtype=float))
        Charge(90, np.array([260, 400], dtype=float))
        Charge(120, np.array([280, 10], dtype=float))
        Charge(150, np.array([300, 200], dtype=float))
        Charge(180, np.array([60, 110], dtype=float))
        Charge(200, np.array([100, 160], dtype=float))

    def run(self):
        while self.running:
            for control in self.controls.values():
                control.is_pressed = False
                control.is_released = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key in self.bindings.keys():
                        self.controls[self.bindings[event.key]].is_pressed = True

                if event.type == pygame.KEYUP:
                    if event.key in self.bindings.keys():
                        self.controls[self.bindings[event.key]].is_released = True
                            

            keys = pygame.key.get_pressed()
            for key in self.bindings.keys():
                self.controls[self.bindings[key]].is_held = keys[key]

            self.delta_time = self.clock.tick(self.FPS) / 1000
            self.canvas.fill((0, 0, 0))
            self.player.tick(self.controls["up"], self.controls["right"], self.controls["down"], self.controls["left"], self.controls["interact"], self.delta_time)
            self.player.render(self.canvas)
            Charge.calculate_interactions(self.delta_time)

            for renderable in Renderable.renderables:
                if renderable != self.player:
                    renderable.calculate_wall_collision(self.WIDTH, self.HEIGHT)
                    renderable.tick(self.delta_time)
                    renderable.render(self.canvas)
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()