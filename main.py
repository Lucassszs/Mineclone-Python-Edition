from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import math

noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000))

app = Ursina()

def is_block_at(position):
    return any([block.position == position for block in scene.entities if isinstance(block, Block)])

selected_block = "grass"

player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0)
)

block_textures = {
    "grass": load_texture("textures/grass.png"),
    "dirt": load_texture("textures/dirt.png"),
    "stone": load_texture("textures/stone.png"),
    "bedrock": load_texture("textures/bedrock.png"),
    "log": load_texture("textures/log_side.png"),
    "leaves": load_texture("textures/leaves.png"),
}

class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position=position,
            model=None,
            scale=1,
            origin_y=0,
            texture=block_textures.get(block_type),
            collider="box"
        )
        self.block_type = block_type
        self.update_model()

    def update_model(self):
        vertices = []
        triangles = []
        uvs = []

        directions = [
            Vec3(1, 0, 0), Vec3(-1, 0, 0),
            Vec3(0, 1, 0), Vec3(0, -1, 0),
            Vec3(0, 0, 1), Vec3(0, 0, -1)
        ]

        face_vertices = [
            [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)],  # Frente
            [(0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5)],  # Trás
            [(-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5)],  # Cima
            [(-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5)],  # Baixo
            [(-0.5, -0.5, -0.5), (-0.5, -0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5)],  # Esquerda
            [(0.5, -0.5, 0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5)]  # Direita
        ]

        face_uvs = [
            [(0, 0), (1, 0), (1, 1), (0, 1)] for _ in range(6)
        ]

        for i, direction in enumerate(directions):
            if not is_block_at(self.position + direction):
                start_index = len(vertices)
                vertices.extend(face_vertices[i])
                triangles.extend([
                    start_index, start_index + 1, start_index + 2,
                    start_index, start_index + 2, start_index + 3
                ])
                uvs.extend(face_uvs[i])

        self.model = Mesh(vertices=vertices, triangles=triangles, uvs=uvs, mode='triangle')

mini_block = Entity(
    parent=camera,
    model="cube",
    scale=0.5,
    color=color.rgba(1, 1, 1, 0.5)
)

def input(key):
  global selected_block
  #place block
  if key == "left mouse down":
    hit_info = raycast(camera.world_position, camera.forward, distance=10)
    if hit_info.hit:
      block = Block(hit_info.entity.position + hit_info.normal, selected_block)
  #delete block
  if key == "right mouse down" and mouse.hovered_entity:
    if not mouse.hovered_entity.block_type == "bedrock":
      destroy(mouse.hovered_entity)
  #change block type
  if key == "1":
    selected_block = "grass"
  if key == '2':
    selected_block = "dirt"
  if key == '3':
    selected_block = "stone"

'''o bug no posicionamento da arvore se dava pelo fato da classe receber a posição dela mesma e pelo fato do tronco e das folhas terem posicionamentos distintos mas conectados oq acabava fazendo a arvore não saber as cordenadas para aparecer'''
class Arvore(Entity):
    def __init__(self, position=(0 , 0 , 0)):
        super().__init__(
            parent=scene,
            collider = 'box'
        )
        self.Tronco_arvore(position)
        self.Folhas_arvore(position)


    def Tronco_arvore(self, position):
        for y in range(4):
                Block((position[0] , position[1] + y ,position[2]), "log")
                
                
    def Folhas_arvore(self, position):
        topo_do_tronco = position[1] + 3
        for x in range(-1, 2):
            for z in range(-1, 2):
                for y in range(4, 6):
                    
                        Block((position[0] + x, topo_do_tronco + y - 4 , position[2] + z), "leaves")


min_height = -5
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

app.run()

