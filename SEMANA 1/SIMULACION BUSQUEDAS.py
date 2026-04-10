import pygame
import sys
import random
pygame.init()
ANCHO, ALTO = 1250, 800 
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualizador de Búsquedas ")

COLOR_FONDO = (10, 10, 15)
COLOR_PANEL = (20, 20, 28)
COLOR_ACENTO = (0, 180, 255)
COLOR_OBJETIVO = (255, 85, 85)
COLOR_EXITO = (0, 255, 120)
COLOR_RESALTADO = (45, 45, 70) 
COLOR_TEXTO = (175, 190, 200)
COLOR_BARRA = (60, 60, 80)
COLOR_DESCARTADO = (30, 30, 35)
COLOR_BOTON = (40, 40, 50)
COLOR_BOTON_HOVER = (60, 60, 75)

fuente_codigo = pygame.font.SysFont("Consolas", 16)
fuente_md = pygame.font.SysFont("Segoe UI", 18, bold=True)
fuente_btn = pygame.font.SysFont("Segoe UI", 16, bold=True)

FRAG_COD = {
    "Lineal": ["int buscar(vector<int>& a, int x) {", "  for(int i=0; i<a.size(); ++i) {", "    if(a[i] == x) return i;", "  }", "  return -1;", "}"],
    "Binaria": ["int buscar(vector<int>& a, int x) {", "  int l=0, r=a.size()-1;", "  while(l <= r) {", "    int m = l+(r-l)/2;", "    if(a[m] == x) return m;", "    else if(a[m]<x) l=m+1;", "    else r=m-1;", "  }", "  return -1;", "}"],
    "Exponencial": ["int buscar(vector<int>& a, int x) {", "  if(a[0] == x) return 0;", "  int i = 1;", "  while(i < a.size() && a[i] <= x)", "    i = i * 2;", "  return busquedaBinaria(a, x, i/2, ", "                      min(i, n-1));", "}"],
    "Interpolación": ["int buscar(vector<int>& a, int x) {", "  int l=0, r=a.size()-1;", "  while(l<=r && x>=a[l] && x<=a[r]) {", "    int p = l + (double)(r-l) * ", "            (x-a[l]) / (a[r]-a[l]);", "    if(a[p] == x) return p;", "    ...", "  }", "  return -1;", "}"]
}
datos, valor_objetivo = [], 0
texto_entrada = ""
comparaciones = 0
algoritmo = "Binaria"
linea_activa = -1
corriendo = encontrado = False
tam_lista, velocidad_ms = 25, 350
indice_actual, izq, der = -1, 0, 0
exp_i, fase_binaria = 1, False
descartados = set()

def generar_datos(tam):
    global datos, valor_objetivo, texto_entrada, tam_lista
    tam_lista = max(5, min(tam, 75))
    datos = sorted(random.sample(range(10, 400), tam_lista))
    valor_objetivo = random.choice(datos)
    texto_entrada = str(valor_objetivo)
    reiniciar_busqueda()

def reiniciar_busqueda():
    global indice_actual, izq, der, exp_i, comparaciones, encontrado, descartados, corriendo, fase_binaria, linea_activa
    indice_actual = -1
    izq, der = 0, len(datos) - 1
    exp_i, fase_binaria = 1, False
    comparaciones = encontrado = corriendo = False
    linea_activa = -1
    descartados.clear()

def paso_busqueda():
    global indice_actual, izq, der, exp_i, comparaciones, encontrado, corriendo, fase_binaria, linea_activa
    comparaciones += 1
    
    if algoritmo == "Lineal":
        indice_actual += 1
        linea_activa = 1
        if indice_actual < len(datos):
            if datos[indice_actual] == valor_objetivo: encontrado = True; corriendo = False; linea_activa = 2
            else: descartados.add(indice_actual)
        else: corriendo = False

    elif algoritmo == "Binaria":
        if izq <= der:
            linea_activa = 3
            m = izq + (der - izq) // 2
            indice_actual = m
            if datos[m] == valor_objetivo: encontrado = True; corriendo = False; linea_activa = 4
            elif datos[m] < valor_objetivo:
                for i in range(izq, m + 1): descartados.add(i)
                izq = m + 1; linea_activa = 5
            else:
                for i in range(m, der + 1): descartados.add(i)
                der = m - 1; linea_activa = 6
        else: corriendo = False

    elif algoritmo == "Exponencial":
        if not fase_binaria:
            linea_activa = 3
            if datos[0] == valor_objetivo: indice_actual = 0; encontrado = True; corriendo = False; return
            if exp_i < len(datos) and datos[exp_i] <= valor_objetivo:
                indice_actual = exp_i
                for i in range(exp_i): descartados.add(i)
                if datos[exp_i] == valor_objetivo: encontrado = True; corriendo = False; return
                exp_i *= 2
            else:
                izq, der = exp_i // 2, min(exp_i, len(datos) - 1)
                fase_binaria = True
        else:
            if izq <= der:
                m = izq + (der - izq) // 2
                indice_actual = m
                if datos[m] == valor_objetivo: encontrado = True; corriendo = False
                elif datos[m] < valor_objetivo: izq = m + 1
                else: der = m - 1
            else: corriendo = False

    elif algoritmo == "Interpolación":
        if izq <= der and valor_objetivo >= datos[izq] and valor_objetivo <= datos[der]:
            linea_activa = 3
            den = datos[der] - datos[izq]
            pos = izq + int((float(der - izq) * (valor_objetivo - datos[izq])) / den) if den != 0 else izq
            indice_actual = pos
            if datos[pos] == valor_objetivo: encontrado = True; corriendo = False
            elif datos[pos] < valor_objetivo:
                for i in range(izq, pos + 1): descartados.add(i)
                izq = pos + 1
            else:
                for i in range(pos, der + 1): descartados.add(i)
                der = pos - 1
        else: corriendo = False

class Boton:
    def __init__(self, x, y, w, h, texto, funcion):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto, self.funcion = texto, funcion
        self.hover = False
    def dibujar(self, surf):
        color = COLOR_BOTON_HOVER if self.hover else COLOR_BOTON
        pygame.draw.rect(surf, color, self.rect, border_radius=5)
        t = fuente_btn.render(self.texto, True, COLOR_TEXTO)
        surf.blit(t, (self.rect.centerx - t.get_width()//2, self.rect.centery - t.get_height()//2))
    def revisar_evento(self, evento):
        if evento.type == pygame.MOUSEMOTION: self.hover = self.rect.collidepoint(evento.pos)
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.hover: self.funcion()

botones = [
    Boton(420, 160, 40, 30, "-", lambda: generar_datos(tam_lista - 5)),
    Boton(470, 160, 40, 30, "+", lambda: generar_datos(tam_lista + 5)),
    Boton(580, 160, 40, 30, "-", lambda: globals().update(velocidad_ms=max(50, velocidad_ms+50))),
    Boton(630, 160, 40, 30, "+", lambda: globals().update(velocidad_ms=max(50, velocidad_ms-50)))
]

def dibujar():
    pantalla.fill(COLOR_FONDO)
    
    pygame.draw.rect(pantalla, COLOR_PANEL, (30, 30, 350, 200), border_radius=12)
    pantalla.blit(fuente_md.render("CONFIGURACIÓN", True, COLOR_ACENTO), (50, 45))
    for i, nombre in enumerate(FRAG_COD.keys()):
        seleccionado = algoritmo == nombre
        color = COLOR_ACENTO if seleccionado else (100, 100, 110)
        pantalla.blit(fuente_md.render(f"{'> ' if seleccionado else '  '}{i+1}. {nombre}", True, color), (50, 85 + i*28))
    
    pygame.draw.rect(pantalla, (10, 10, 15), (240, 45, 110, 32), border_radius=5)
    pantalla.blit(fuente_md.render(texto_entrada, True, COLOR_OBJETIVO), (250, 49))
    pantalla.blit(fuente_codigo.render("OBJETIVO:", True, COLOR_TEXTO), (160, 52))

    pygame.draw.rect(pantalla, COLOR_PANEL, (400, 30, 350, 200), border_radius=12)
    pantalla.blit(fuente_md.render("CONTROL SIMULACIÓN", True, COLOR_ACENTO), (420, 45))
    pantalla.blit(fuente_md.render(f"COMPARACIONES: {comparaciones}", True, COLOR_TEXTO), (420, 85))
    pantalla.blit(fuente_md.render(f"VELOCIDAD: {velocidad_ms}ms", True, COLOR_TEXTO), (420, 115))
    
    pantalla.blit(fuente_codigo.render(f"VALORES: {tam_lista}", True, COLOR_TEXTO), (420, 145))
    pantalla.blit(fuente_codigo.render(f"TIEMPO: {velocidad_ms}ms", True, COLOR_TEXTO), (580, 145))
    for b in botones: b.dibujar(pantalla)

    pygame.draw.rect(pantalla, COLOR_PANEL, (770, 30, 400, 200), border_radius=12)
    pantalla.blit(fuente_md.render("CÓDIGO FUENTE (C++)", True, COLOR_ACENTO), (790, 45))
    for i, linea in enumerate(FRAG_COD[algoritmo][:6]):
        if i == linea_activa: pygame.draw.rect(pantalla, COLOR_RESALTADO, (780, 75 + i*20, 380, 20), border_radius=4)
        pantalla.blit(fuente_codigo.render(linea, True, COLOR_TEXTO), (790, 75 + i*20))

    if datos:
        max_h, area_barras_w = 400, ANCHO - 100
        ancho_b = max(2, (area_barras_w // len(datos)) - 6)
        for i, val in enumerate(datos):
            h = (val / max(datos)) * max_h
            x, y = 50 + i * (ancho_b + 6), ALTO - 150 - h
            color = COLOR_BARRA
            if i in descartados: color = COLOR_DESCARTADO
            if i == indice_actual: color = COLOR_EXITO if encontrado else COLOR_ACENTO
            if val == valor_objetivo: pygame.draw.rect(pantalla, (40, 30, 30), (x-2, ALTO-150-max_h, ancho_b+4, max_h), border_radius=4)
            pygame.draw.rect(pantalla, color, (x, y, ancho_b, h), border_radius=3)
            if len(datos) < 35:
                v_t = fuente_codigo.render(str(val), True, COLOR_TEXTO)
                pantalla.blit(v_t, (x + ancho_b//2 - v_t.get_width()//2, y - 22))

    pygame.draw.rect(pantalla, COLOR_PANEL, (30, 780, ANCHO-60, 50), border_radius=10)
    estado = "VALOR ENCONTRADO" if encontrado else ("BUSCANDO..." if corriendo else "LISTO - ENTER")
    pantalla.blit(fuente_md.render(f"MODO: {algoritmo.upper()} | {estado}", True, COLOR_EXITO if encontrado else COLOR_TEXTO), (60, 793))

generar_datos(tam_lista)
reloj, temp = pygame.time.Clock(), pygame.time.get_ticks()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()
        for b in botones: b.revisar_evento(e)
        if e.type == pygame.KEYDOWN:
            if not corriendo:
                if e.key == pygame.K_BACKSPACE: texto_entrada = texto_entrada[:-1]
                elif e.unicode.isdigit(): texto_entrada += e.unicode
                elif e.key == pygame.K_RETURN: valor_objetivo = int(texto_entrada) if texto_entrada else valor_objetivo; reiniciar_busqueda(); corriendo = True
            if e.key == pygame.K_1: algoritmo = "Lineal"; reiniciar_busqueda()
            if e.key == pygame.K_2: algoritmo = "Binaria"; reiniciar_busqueda()
            if e.key == pygame.K_3: algoritmo = "Exponencial"; reiniciar_busqueda()
            if e.key == pygame.K_4: algoritmo = "Interpolación"; reiniciar_busqueda()
            if e.key == pygame.K_r: generar_datos(tam_lista)

    if corriendo and pygame.time.get_ticks() - temp > velocidad_ms:
        paso_busqueda(); temp = pygame.time.get_ticks()

    dibujar(); pygame.display.flip(); reloj.tick(60)