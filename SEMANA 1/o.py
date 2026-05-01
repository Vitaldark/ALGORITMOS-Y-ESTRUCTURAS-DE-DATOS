import pygame
import sys
import random

# ----- CONFIGURACIÓN VISUAL (Tema Hacker / Consola) -----
FPS = 60
WIDTH, HEIGHT = 1200, 800

BG_COLOR = (5, 5, 5)             # Negro casi absoluto
SURFACE_COLOR = (15, 20, 15)     # Gris muy oscuro con levísimo tono verde
PRIMARY_COLOR = (0, 255, 0)      # Verde Neón
SECONDARY_COLOR = (0, 180, 0)    # Verde un poco más opaco para acentos
ERROR_COLOR = (255, 0, 80)       # Rojo brillante luminoso
SUCCESS_COLOR = (0, 255, 255)    # Cian / Azul eléctrico
TEXT_COLOR = (0, 230, 0)         # Verde para textos normales
TEXT_MUTED = (0, 110, 0)         # Verde opaco/oscuro para textos secundarios
BAR_DEFAULT = (0, 130, 0)        # Verde intermedio para barras
BAR_DISCARDED = (20, 30, 20)     # Gris/Verde muy oscuro para descartados

def init_fonts():
    global font_title, font_body, font_code, font_small
    # Estilo hacker: todo monoespaciado
    font_title = pygame.font.SysFont("Consolas", 24, bold=True)
    font_body = pygame.font.SysFont("Consolas", 18)
    font_small = pygame.font.SysFont("Consolas", 14)
    font_code = pygame.font.SysFont("Consolas", 16)

# ----- ALGORITMOS BÚSQUEDA (Optimizados usando Generadores `yield`) -----
# El uso de 'yield' me permite pausar la ejecución de una función normal
# para que el entorno gráfico pueda dibujar exactamente el estado actual
# en ese paso de la búsqueda, sin usar banderas globales raras.

def busqueda_lineal(datos, objetivo):
    for i in range(len(datos)):
        yield {"actual": i, "activa": 1} # Resalta la línea del 'for'
        if datos[i] == objetivo:
            yield {"actual": i, "encontrado": True, "activa": 2}
            return
        yield {"actual": i, "descartado": i, "activa": 1}

def busqueda_binaria(datos, objetivo):
    izq, der = 0, len(datos) - 1
    yield {"actual": None, "izq": izq, "der": der, "activa": 1}
    while izq <= der:
        m = izq + (der - izq) // 2
        yield {"actual": m, "izq": izq, "der": der, "activa": 3}
        if datos[m] == objetivo:
            yield {"actual": m, "encontrado": True, "activa": 4}
            return
        elif datos[m] < objetivo:
            yield {"actual": m, "descartar_rango": (izq, m), "activa": 5}
            izq = m + 1
        else:
            yield {"actual": m, "descartar_rango": (m, der), "activa": 6}
            der = m - 1
    yield {"actual": None, "encontrado": False, "activa": 7}

def busqueda_exponencial(datos, objetivo):
    if len(datos) == 0: return
    yield {"actual": 0, "activa": 1}
    if datos[0] == objetivo:
        yield {"actual": 0, "encontrado": True, "activa": 1}
        return
    
    i = 1
    yield {"actual": i, "activa": 2}
    while i < len(datos) and datos[i] <= objetivo:
        yield {"actual": i, "descartar_rango": (0, i-1), "activa": 3}
        if datos[i] == objetivo:
            yield {"actual": i, "encontrado": True, "activa": 4}
            return
        i *= 2
        yield {"actual": min(i, len(datos)-1), "activa": 4}
    
    izq, der = i // 2, min(i, len(datos) - 1)
    
    yield {"actual": None, "izq": izq, "der": der, "activa": 5}
    while izq <= der:
        m = izq + (der - izq) // 2
        yield {"actual": m, "izq": izq, "der": der, "activa": 5}
        if datos[m] == objetivo:
            yield {"actual": m, "encontrado": True, "activa": 5}
            return
        elif datos[m] < objetivo:
            yield {"actual": m, "descartar_rango": (izq, m), "activa": 5}
            izq = m + 1
        else:
            yield {"actual": m, "descartar_rango": (m, der), "activa": 5}
            der = m - 1

def busqueda_interpolacion(datos, objetivo):
    izq, der = 0, len(datos) - 1
    while izq <= der and objetivo >= datos[izq] and objetivo <= datos[der]:
        yield {"actual": None, "izq": izq, "der": der, "activa": 2}
        if izq == der:
            if datos[izq] == objetivo:
                yield {"actual": izq, "encontrado": True, "activa": 4}
            return
        
        denominador = datos[der] - datos[izq]
        if denominador == 0: p = izq
        else: p = izq + int(((float(der - izq) / denominador) * (objetivo - datos[izq])))
        
        yield {"actual": p, "izq": izq, "der": der, "activa": 3}
        
        if datos[p] == objetivo:
            yield {"actual": p, "encontrado": True, "activa": 4}
            return
        if datos[p] < objetivo:
            yield {"actual": p, "descartar_rango": (izq, p), "activa": 5}
            izq = p + 1
        else:
            yield {"actual": p, "descartar_rango": (p, der), "activa": 6}
            der = p - 1

ALGORITMOS = {
    "Lineal": busqueda_lineal,
    "Binaria": busqueda_binaria,
    "Exponencial": busqueda_exponencial,
    "Interpolación": busqueda_interpolacion
}

CODIGOS = {
    "Lineal": ["def lineal(arr, x):", "    for i in range(len(arr)):", "        if arr[i] == x: return i", "    return -1"],
    "Binaria": ["def binaria(arr, x):", "    l, r = 0, len(arr)-1", "    while l <= r:", "        m = (l+r)//2", "        if arr[m] == x: return m", "        elif arr[m] < x: l = m+1", "        else: r = m-1", "    return -1"],
    "Exponencial": ["def exponencial(arr, x):", "    if arr[0] == x: return 0", "    i = 1", "    while i < len(arr) and arr[i] <= x:", "        i *= 2", "    return busqueda_binaria(...)"],
    "Interpolación": ["def interpolacion(arr, x):", "    l, r = 0, len(arr)-1", "    while l<=r and x>=arr[l] and x<=arr[r]:", "        p = l + int((r-l)*(x-arr[l])/(arr[r]-arr[l]))", "        if arr[p] == x: return p", "        elif arr[p] < x: l = p+1", "        else: r = p-1", "    return -1"]
}

# ----- UI CLASSES -----
class BotonUI:
    def __init__(self, x, y, width, height, text, callback, color=PRIMARY_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hovered = False

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered: self.callback()

    def draw(self, surface):
        c = (min(255, self.color[0]+30), min(255, self.color[1]+30), min(255, self.color[2]+30)) if self.hovered else self.color
        pygame.draw.rect(surface, c, self.rect, border_radius=6)
        txt = font_body.render(self.text, True, BG_COLOR if sum(c) > 300 else TEXT_COLOR)
        surface.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))

# ----- APP PRINCIPAL (Orientada a Objetos) -----
class SimuladorApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ROOT@ALG-VISUALIZER:~# TEMA HACKER")
        init_fonts()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Variables de estado encapsuladas en clase (adiós a globales)
        self.tam_arreglo = 45
        self.arreglo = []
        self.objetivo = 0
        self.entrada_objetivo = ""
        self.algoritmo_actual = "Binaria"
        self.generador_pasos = None
        
        self.velocidad = 200 
        self.ultimo_paso_time = 0
        self.simulando = False
        self.encontrado = False
        
        self.indice_evaluando = -1
        self.rango_izq = -1
        self.rango_der = -1
        self.indices_descartados = set()
        self.linea_codigo = -1
        self.comparaciones = 0
        
        self.botones = [
            BotonUI(40, 150, 40, 30, "-", lambda: self.cambiar_tam(-5), SECONDARY_COLOR),
            BotonUI(90, 150, 40, 30, "+", lambda: self.cambiar_tam(5), SECONDARY_COLOR),
            BotonUI(40, 220, 40, 30, "-", lambda: self.cambiar_vel(50), SECONDARY_COLOR),
            BotonUI(90, 220, 40, 30, "+", lambda: self.cambiar_vel(-50), SECONDARY_COLOR),
            BotonUI(40, 320, 100, 40, "REINICIAR", self.generar_nuevos_datos, PRIMARY_COLOR),
            BotonUI(150, 320, 100, 40, "BUSCAR", self.iniciar_busqueda, SUCCESS_COLOR)
        ]
        self.generar_nuevos_datos()

    def cambiar_tam(self, delta):
        self.tam_arreglo = max(10, min(100, self.tam_arreglo + delta))
        self.generar_nuevos_datos()

    def cambiar_vel(self, delta):
        self.velocidad = max(20, min(1000, self.velocidad + delta))

    def generar_nuevos_datos(self):
        self.arreglo = sorted(random.sample(range(10, 500), self.tam_arreglo))
        self.objetivo = random.choice(self.arreglo)
        self.entrada_objetivo = str(self.objetivo)
        self.preparar_simulacion()

    def preparar_simulacion(self):
        self.simulando = False
        self.encontrado = False
        self.indice_evaluando = -1
        self.rango_izq = -1
        self.rango_der = -1
        self.indices_descartados.clear()
        self.linea_codigo = -1
        self.comparaciones = 0
        self.generador_pasos = None

    def iniciar_busqueda(self):
        if self.entrada_objetivo.isdigit(): self.objetivo = int(self.entrada_objetivo)
        self.preparar_simulacion()
        self.generador_pasos = ALGORITMOS[self.algoritmo_actual](self.arreglo, self.objetivo)
        self.simulando = True
        self.ultimo_paso_time = pygame.time.get_ticks()

    def avanzar_paso(self):
        if not self.generador_pasos: return
        try:
            estado = next(self.generador_pasos)
            self.comparaciones += 1
            if "actual" in estado: self.indice_evaluando = estado["actual"]
            if "izq" in estado: self.rango_izq = estado["izq"]
            if "der" in estado: self.rango_der = estado["der"]
            if "activa" in estado: self.linea_codigo = estado["activa"]
            
            if "descartado" in estado: self.indices_descartados.add(estado["descartado"])
            if "descartar_rango" in estado:
                for i in range(estado["descartar_rango"][0], estado["descartar_rango"][1] + 1):
                    self.indices_descartados.add(i)
                    
            if estado.get("encontrado", False):
                self.encontrado = True; self.simulando = False
        except StopIteration:
            self.simulando = False

    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Panel Izquierdo
        pygame.draw.rect(self.screen, SURFACE_COLOR, (20, 20, 300, 400), border_radius=10)
        self.screen.blit(font_title.render("Configuración", True, PRIMARY_COLOR), (40, 35))
        self.screen.blit(font_body.render(f"Algoritmo: {self.algoritmo_actual} (L, B, E, I)", True, TEXT_COLOR), (40, 75))
        self.screen.blit(font_body.render("Objetivo a buscar:", True, TEXT_MUTED), (40, 105))
        
        pygame.draw.rect(self.screen, BG_COLOR, (180, 100, 100, 30), border_radius=5)
        self.screen.blit(font_code.render(self.entrada_objetivo + ("_" if not self.simulando and pygame.time.get_ticks() % 1000 < 500 else ""), True, ERROR_COLOR), (190, 105))
        
        self.screen.blit(font_body.render(f"Elementos: {self.tam_arreglo}", True, TEXT_MUTED), (150, 155))
        self.screen.blit(font_body.render(f"Velocidad: {self.velocidad}ms", True, TEXT_MUTED), (150, 225))
        self.screen.blit(font_title.render(f"Pases: {self.comparaciones}", True, SECONDARY_COLOR), (40, 275))

        for b in self.botones: b.draw(self.screen)
        
        # Panel Derecho (Código Fuente)
        pygame.draw.rect(self.screen, SURFACE_COLOR, (340, 20, WIDTH-360, 250), border_radius=10)
        self.screen.blit(font_title.render(f"Algoritmo en Python", True, PRIMARY_COLOR), (360, 35))
        
        for i, linea in enumerate(CODIGOS[self.algoritmo_actual]):
            color = TEXT_COLOR
            if i == self.linea_codigo:
                pygame.draw.rect(self.screen, (50, 50, 70), (355, 75 + i*22, WIDTH-390, 22), border_radius=3)
                color = SECONDARY_COLOR
            self.screen.blit(font_code.render(linea, True, color), (365, 76 + i*22))

        # Renderizado de Barras
        margen_x = 40
        area_w = WIDTH - (margen_x * 2)
        if self.arreglo:
            ancho_b = max(2, (area_w // self.tam_arreglo) - 4)
            sep = (area_w - (ancho_b * self.tam_arreglo)) // self.tam_arreglo
            max_h = HEIGHT - 350
            max_val = max(self.arreglo)
            
            for i, val in enumerate(self.arreglo):
                x = margen_x + i * (ancho_b + sep)
                y = HEIGHT - 40 - ((val / max_val) * max_h)
                color = BAR_DEFAULT
                
                if i in self.indices_descartados: color = BAR_DISCARDED
                elif self.simulando and self.rango_izq <= i <= self.rango_der: color = (70, 70, 100) 
                if i == self.indice_evaluando: color = ERROR_COLOR if not self.encontrado else SUCCESS_COLOR
                
                pygame.draw.rect(self.screen, color, (x, y, ancho_b, ((val / max_val) * max_h)), border_radius=2)
                if val == self.objetivo: pygame.draw.rect(self.screen, ERROR_COLOR, (x, HEIGHT - 30, ancho_b, 5))
                
                # Renderizar el valor numérico
                texto_val = font_small.render(str(val), True, TEXT_COLOR if color != BAR_DISCARDED else TEXT_MUTED)
                if ancho_b >= texto_val.get_width() + 2:
                    # Mostrar horizontal si cabe
                    pos_x = x + ancho_b // 2 - texto_val.get_width() // 2
                    pos_y = y - texto_val.get_height() - 2
                    self.screen.blit(texto_val, (pos_x, pos_y))
                else:
                    # Rotar si la barra es delgada
                    texto_rotado = pygame.transform.rotate(texto_val, 90)
                    pos_x = x + ancho_b // 2 - texto_rotado.get_width() // 2
                    pos_y = y - texto_rotado.get_height() - 2
                    self.screen.blit(texto_rotado, (pos_x, pos_y))

        # Mensaje de estado inferior
        estado_t, c_estado = "LISTO (Pulsa ENTER o BUSCAR)", TEXT_MUTED
        if self.simulando: estado_t, c_estado = "SIMULANDO BÚSQUEDA...", SECONDARY_COLOR
        elif self.encontrado: estado_t, c_estado = f"¡ENCONTRADO EN ÍNDICE {self.indice_evaluando}!", SUCCESS_COLOR
        elif self.indice_evaluando != -1 and not self.simulando: estado_t, c_estado = "NO SE ENCONTRÓ EL VALOR.", ERROR_COLOR
            
        estado_surface = font_title.render(estado_t, True, c_estado)
        self.screen.blit(estado_surface, (WIDTH//2 - estado_surface.get_width()//2, 290))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.running = False
                for b in self.botones: b.check_event(event)
                if event.type == pygame.KEYDOWN:
                    if not self.simulando:
                        if event.key == pygame.K_BACKSPACE: self.entrada_objetivo = self.entrada_objetivo[:-1]
                        elif event.unicode.isdigit(): self.entrada_objetivo += event.unicode
                        elif event.key == pygame.K_RETURN: self.iniciar_busqueda()
                        elif event.key == pygame.K_l: self.algoritmo_actual = "Lineal"; self.preparar_simulacion()
                        elif event.key == pygame.K_b: self.algoritmo_actual = "Binaria"; self.preparar_simulacion()
                        elif event.key == pygame.K_e: self.algoritmo_actual = "Exponencial"; self.preparar_simulacion()
                        elif event.key == pygame.K_i: self.algoritmo_actual = "Interpolación"; self.preparar_simulacion()

            t_actual = pygame.time.get_ticks()
            if self.simulando and t_actual - self.ultimo_paso_time > self.velocidad:
                self.avanzar_paso()
                self.ultimo_paso_time = t_actual

            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit(); sys.exit()

if __name__ == "__main__":
    SimuladorApp().run()