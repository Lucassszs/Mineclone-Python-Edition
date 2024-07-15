from ursina import*
from screeninfo import get_monitors


# Define o tamanho da janela (largura, altura)
window.size = (1600, 960)

# Obtem a resolução da tela
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# Calcula a posição para centralizar a janela
window_x = (screen_width - window.size[0]) // 2
window_y = (screen_height - window.size[1]) // 2

# Define a posição da janela
window.position = (window_x, window_y)