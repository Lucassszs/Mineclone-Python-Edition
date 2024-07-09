from ursina import *
from Configs import *


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            color=color.hsv(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.white,
        )
        # Aplica a textura com base na posição y do voxel
        if position[1] >= Altura:
            self.Grass()
        elif position[1] < Altura:
            self.Dirt()

    def Grass(self):
        self.texture = 'grass.png'

    def Dirt(self):
        self.texture = 'dirt.png'