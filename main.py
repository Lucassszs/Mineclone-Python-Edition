#import libraries
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import Configs 

noise = PerlinNoise(octaves=2, seed=random.randint(1, 1000))

#instancia do app
app = Ursina()

# Variaveis do game
selected_block = "grass"

# player
player = FirstPersonController(
  mouse_sensitivity=Vec2(100, 100),
  position=(0, 5, 0),
  inventario = []
  )


# texturas 
block_textures = {
  "grass": load_texture("textures/grass.png"),
  "dirt": load_texture("textures/dirt.png"),
  "stone": load_texture("textures/stone.png"),
  "bedrock": load_texture("textures/sand.png"),
  "log": load_texture("textures/log_side.png"),
  "leaves": load_texture("textures/leaves.png"),
}

#classe de que cria cada bloco

class Block(Entity):
  def __init__(self, position, block_type):
    super().__init__(
      position=position,
      model="cube",
      scale=1,
      origin_y= 0,
      texture=block_textures.get(block_type),
      block_type = block_type,
      collider="box"
      )
    self.block_type = block_type


# bloco qaue fica na mão do personagem
mini_block = Entity(
  parent=camera,
  model="cube",
  scale=0.2,
  texture=block_textures.get(selected_block),
  position=(0.35, -0.25, 0.5),
  rotation=(-15, -30, -5)
  )


# classe para gerar árvores
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
            Block((position[0] , position[1] + y ,position[2]),"log"
                  )
            
            '''
            Entity(
                model='cube',
                color=color.rgb(142,35,107),  # Cor marrom para o tronco
                texture = 'log_side.png',
                position= (position[0] , position[1] + y ,position[2]),
                parent=self,
                collider = 'box'
            )
            '''
            
            
    def Folhas_arvore(self, position):
        topo_do_tronco = position[1] + 3
        for x in range(-1, 2):
            for z in range(-1, 2):
                for y in range(4, 6):
                    Block((position[0] + x, topo_do_tronco + y - 3 , position[2] + z),"leaves"
                    )


# cria um espaço simples
min_height = -5
for x in range(-40, 10):
  for z in range(-40, 10):
    height = noise([x * 0.02, z * 0.02])
    height = math.floor(height * 7.5)
    for y in range(height, min_height - 1, -1):
     # if y == min_height:
      #  block = Block((x, y + min_height, z), "bedrock")
      if y == height:
        block = Block((x, y + min_height, z), "grass")
        if random.random() < 0.01:  # 10% chance de gerar uma árvore
          Arvore(position=(x, y + min_height + 1, z))
      #elif height - y > 2:
       # block = Block((x, y + min_height, z), "stone")
      #else:
       # block = Block((x, y + min_height, z), "dirt")


# função do teclado
def input(key):
    global selected_block
    if key == "left mouse down":
      
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
          if len(player.inventario) > 0:
            selected_block = player.inventario[0]
            Block(hit_info.entity.position + hit_info.normal, selected_block)
            del(player.inventario[0])
          else:
            Block(hit_info.entity.position + hit_info.normal, selected_block)
            
                 
                
    if key == "right mouse down" and mouse.hovered_entity:
      if not mouse.hovered_entity.block_type == "bedrock":
        player.inventario.append(mouse.hovered_entity.block_type)
        destroy(mouse.hovered_entity)
        
        
    if key == "1":
        selected_block = "grass"
    if key == "2":
        selected_block = "dirt"
    if key == "3":
        selected_block = "stone"
    if key == "4":
        selected_block = "bedrock"
    if key == "5":
        selected_block = "log"
    if key == "6":
        selected_block = "leaves"


def update():
    mini_block.texture = block_textures.get(selected_block)

app.run()