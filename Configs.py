from ursina import*
from screeninfo import get_monitors


# Defina o tamanho da janela (largura, altura)
window.size = (1024, 768)

# Obtenha a resolução da tela
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Calcule a posição para centralizar a janela
window_x = (screen_width - window.size[0]) // 2
window_y = (screen_height - window.size[1]) // 2

# Defina a posição da janela
window.position = (window_x, window_y)




Largura = 16
Altura = 2
Profundidade = 16