from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from Configs import *
from Chunks import *
app = Ursina()
# Define as dimensões do mundo
window.title = "Mundo"


'''
# Define a classe Voxel
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
'''
        
class Arvore(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
        )
        self.Tronco_arvore(position)
        self.Folhas_arvore(position)
        
    def Tronco_arvore(self, position):
        for y in range(4):
            Entity(
                model='cube',
                color=color.rgb(142,35,107),  # Cor marrom para o tronco
                texture = 'log_side.png',
                position=(position[0], position[1] + y, position[2]),
                parent=self
            )
    def Folhas_arvore(self, position):
        topo_do_tronco = position[1] + 3
        for x in range(-1, 2):
            for z in range(-1, 2):
                for y in range(4, 6):
                    Folhas = Entity(
                        model='cube',
                        color=color.rgb(0, 255, 0),  # Cor verde para as folhas
                        texture = 'leaves.png',
                        position=(position[0] + x, topo_do_tronco + y - 4, position[2] + z),
                        parent=self,
                    )
                
# Criação dos voxels
for z in range(Profundidade):
    for x in range(Largura):
        for y in range(Altura):
         voxel = Voxel(position=(x, y, z))

# Criação de uma árvore em uma posição específica
arvore = Arvore(position=(2, 1, 2))  # Ajusta a posição inicial da árvore

# Função para colocar árvore ao clicar (Bug DETECTADO)
def colocar_arvore():
    hit_info = raycast(camera.world_position, camera.forward, distance=5)
    if hit_info.hit:
        # Cria uma nova árvore na posição exata onde ocorreu a colisão
        Arvore(position=hit_info.entity.position + hit_info.normal)
asdasdasd

def input(key):
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)
    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)
        
    if key == '2':
        colocar_arvore()

player = FirstPersonController()
app.run()
