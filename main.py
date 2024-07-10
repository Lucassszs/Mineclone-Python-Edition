from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random


noise = PerlinNoise(octaves=3, seed= 1)

app = Ursina()

selected_block = "grass"


player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0)
)

block_textures = {
    "grass": load_texture("textures/grass.png"),
    "dirt": load_texture("textures/dirt.png"),
    "stone": load_texture("textures/stone.png"),
    "bedrock": load_texture("textures/sand.png"),
    "log": load_texture("textures/log_side.png"),
    "leaves": load_texture("textures/leaves.png"),
}


class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position=position,
            model="cube",
            scale=1,
            origin_y=0,
            texture=block_textures.get(block_type),
            collider="box"
        )
        self.block_type = block_type

    def is_hidden(self):
        directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
        for dir in directions:
            neighbor_position = self.position + Vec3(*dir)
            hit_info = raycast(neighbor_position, dir)
            if hit_info.hit and hit_info.entity.block_type != "bedrock":
                return False
        return True
    
    
    
    
mini_block = Entity(
    parent=camera,
    model="cube",
    scale=0.2,
    texture=block_textures.get(selected_block),
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -30, -5)
)

class Arvore(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            collider='box'
        )
        self.Tronco_arvore(position)
        self.Folhas_arvore(position)

    def Tronco_arvore(self, position):
        for y in range(4):
            Block((position[0], position[1] + y, position[2]), "log")

    def Folhas_arvore(self, position):
        topo_do_tronco = position[1] + 3
        for x in range(-1, 2):
            for z in range(-1, 2):
                for y in range(4, 6):
                    Block((position[0] + x, topo_do_tronco + y - 3, position[2] + z), "leaves")

min_height = -5
blocks = []

for x in range(-10, 10):
    for z in range(-10, 10):
        height = noise([x * 0.02, z * 0.02])
        height = math.floor(height * 7.5)
        for y in range(height, min_height - 1, -1):
            if y == min_height:
                block = Block((x, y + min_height, z), "bedrock")
            elif y == height:
                block = Block((x, y + min_height, z), "grass")
                if random.random() < 0.1:
                    Arvore(position=(x, y + min_height + 1, z))
            elif height - y > 2:
                block = Block((x, y + min_height, z), "stone")
            else:
                block = Block((x, y + min_height, z), "dirt")
            blocks.append(block)

def remove_hidden_faces():
    for block in blocks:
        if block.block_type != "bedrock":
            if block.is_hidden():
                block.disable()
            else:
                block.enable()

def input(key):
    global selected_block
    if key == "left mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block)
    if key == "right mouse down" and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            destroy(mouse.hovered_entity)
    if key == "1":
        selected_block = "grass"
    if key == '2':
        selected_block = "dirt"
    if key == '3':
        selected_block = "stone"
        
remove_hidden_faces()        
def update():
    mini_block.texture = block_textures.get(selected_block)

app.run()