import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import groq_client

# =========================================================
#          ALGORITMO DEL METODO HUNGARO (sin librerias)
# =========================================================

def metodo_hungaro(matriz_costos, maximizar=False):
    n = len(matriz_costos)
    if n == 0:
        return [], 0
    m = len(matriz_costos[0])
    size = n if n > m else m
    costo_original = []
    for i in range(n):
        costo_original.append(list(matriz_costos[i]))

    if maximizar:
        max_val = matriz_costos[0][0]
        for i in range(n):
            for j in range(m):
                if matriz_costos[i][j] > max_val:
                    max_val = matriz_costos[i][j]
        matriz_convertida = []
        for i in range(n):
            fila = []
            for j in range(m):
                fila.append(max_val - matriz_costos[i][j])
            matriz_convertida.append(fila)
    else:
        matriz_convertida = matriz_costos

    C = []
    for i in range(size):
        fila = []
        for j in range(size):
            if i < n and j < m:
                fila.append(matriz_convertida[i][j])
            else:
                fila.append(0)
        C.append(fila)

    INF = 0
    for i in range(size):
        for j in range(size):
            if C[i][j] > INF:
                INF = C[i][j]
    INF = INF * size + 1

    for i in range(size):
        min_fila = C[i][0]
        for j in range(1, size):
            if C[i][j] < min_fila:
                min_fila = C[i][j]
        for j in range(size):
            C[i][j] -= min_fila

    for j in range(size):
        min_col = C[0][j]
        for i in range(1, size):
            if C[i][j] < min_col:
                min_col = C[i][j]
        for i in range(size):
            C[i][j] -= min_col

    pasos = []
    pasos.append(("Matriz tras reducción por filas y columnas:", [list(row) for row in C]))

    def encontrar_cobertura_minima(C, size):
        asignacion_fila = [-1] * size
        asignacion_col = [-1] * size
        for i in range(size):
            for j in range(size):
                if C[i][j] == 0 and asignacion_fila[i] == -1 and asignacion_col[j] == -1:
                    asignacion_fila[i] = j
                    asignacion_col[j] = i
        filas_marcadas = [False] * size
        cols_marcadas = [False] * size
        for i in range(size):
            if asignacion_fila[i] == -1:
                filas_marcadas[i] = True
        cambio = True
        while cambio:
            cambio = False
            for i in range(size):
                if filas_marcadas[i]:
                    for j in range(size):
                        if C[i][j] == 0 and not cols_marcadas[j]:
                            cols_marcadas[j] = True
                            cambio = True
            for j in range(size):
                if cols_marcadas[j]:
                    if asignacion_col[j] != -1 and not filas_marcadas[asignacion_col[j]]:
                        filas_marcadas[asignacion_col[j]] = True
                        cambio = True
        lineas_fila = []
        lineas_col = []
        for i in range(size):
            if not filas_marcadas[i]:
                lineas_fila.append(i)
        for j in range(size):
            if cols_marcadas[j]:
                lineas_col.append(j)
        return lineas_fila, lineas_col

    def asignar_optimo(C, size):
        asignacion = [-1] * size
        cols_usadas = [False] * size
        def backtrack(fila):
            if fila == size:
                return True
            candidatas = []
            for j in range(size):
                if C[fila][j] == 0 and not cols_usadas[j]:
                    candidatas.append(j)
            for j in candidatas:
                asignacion[fila] = j
                cols_usadas[j] = True
                if backtrack(fila + 1):
                    return True
                asignacion[fila] = -1
                cols_usadas[j] = False
            return False
        backtrack(0)
        return asignacion

    max_iteraciones = size * size * 10
    iteracion = 0
    while iteracion < max_iteraciones:
        iteracion += 1
        lineas_fila, lineas_col = encontrar_cobertura_minima(C, size)
        num_lineas = len(lineas_fila) + len(lineas_col)
        if num_lineas >= size:
            pasos.append((f"Líneas de cobertura suficientes ({num_lineas} >= {size}). Óptimo encontrado.", [list(row) for row in C]))
            break
        cubierta_fila = [False] * size
        cubierta_col = [False] * size
        for i in lineas_fila:
            cubierta_fila[i] = True
        for j in lineas_col:
            cubierta_col[j] = True
        min_val = INF
        for i in range(size):
            if not cubierta_fila[i]:
                for j in range(size):
                    if not cubierta_col[j]:
                        if C[i][j] < min_val:
                            min_val = C[i][j]
        if min_val == 0 or min_val == INF:
            break
        
        pasos.append((f"Líneas insuficientes ({num_lineas} < {size}). Valor mín no cubierto: {min_val}", [list(row) for row in C]))
        for i in range(size):
            for j in range(size):
                if not cubierta_fila[i] and not cubierta_col[j]:
                    C[i][j] -= min_val
                elif cubierta_fila[i] and cubierta_col[j]:
                    C[i][j] += min_val

    asignacion = asignar_optimo(C, size)
    resultado = []
    costo_total = 0
    for i in range(n):
        j = asignacion[i]
        if j < m:
            resultado.append((i, j))
            costo_total += costo_original[i][j]
    return resultado, costo_total, pasos


# =========================================================
#              INTERFAZ GRAFICA CON TKINTER
# =========================================================

# --- Paleta de colores ---
BG_DARK = "#1a1b2e"
BG_PANEL = "#232540"
BG_CARD = "#2a2d4a"
BG_INPUT = "#353860"
BG_INPUT_FOCUS = "#3d4170"
ACCENT = "#6c63ff"
ACCENT_HOVER = "#7b73ff"
ACCENT_2 = "#00d4aa"
ACCENT_2_HOVER = "#00e8bb"
TEXT_PRIMARY = "#e8e9f3"
TEXT_SECONDARY = "#9ca0b8"
TEXT_MUTED = "#6b6f8a"
BORDER = "#3a3d5c"
SUCCESS = "#00d4aa"
ERROR = "#ff6b6b"
HIGHLIGHT = "#ffdd57"
HIGHLIGHT_BG = "#3d3a20"
ROW_HEADER_BG = "#2e2554"
COL_HEADER_BG = "#1e3a4a"


class HungaroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Húngaro — Asignación Óptima")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(850, 650)

        # Estado
        self.dimension = 3
        self.nombres_filas = []
        self.nombres_cols = []
        self.celdas_entries = []       # Entries de la matriz
        self.fila_name_entries = []    # Entries de nombres de filas
        self.col_name_entries = []     # Entries de nombres de columnas
        self._ultimo_resultado = None  # Almacena ultimo calculo para IA

        # Fuentes
        self.font_title = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.font_subtitle = tkfont.Font(family="Segoe UI", size=11)
        self.font_label = tkfont.Font(family="Segoe UI", size=10)
        self.font_entry = tkfont.Font(family="Consolas", size=11)
        self.font_btn = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        self.font_result = tkfont.Font(family="Consolas", size=10)
        self.font_result_title = tkfont.Font(family="Segoe UI", size=12, weight="bold")

        self._crear_estilos()
        self._crear_interfaz()
        self._generar_matriz()

    # ----- Estilos ttk -----
    def _crear_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("Dark.TFrame", background=BG_DARK)
        self.style.configure("Panel.TFrame", background=BG_PANEL)
        self.style.configure("Card.TFrame", background=BG_CARD)

        self.style.configure("Title.TLabel", background=BG_DARK,
                             foreground=TEXT_PRIMARY, font=self.font_title)
        self.style.configure("Subtitle.TLabel", background=BG_DARK,
                             foreground=TEXT_SECONDARY, font=self.font_subtitle)
        self.style.configure("Label.TLabel", background=BG_PANEL,
                             foreground=TEXT_SECONDARY, font=self.font_label)
        self.style.configure("CardLabel.TLabel", background=BG_CARD,
                             foreground=TEXT_SECONDARY, font=self.font_label)

        self.style.configure("Accent.TButton", background=ACCENT,
                             foreground="white", font=self.font_btn,
                             padding=(16, 8), borderwidth=0)
        self.style.map("Accent.TButton",
                       background=[("active", ACCENT_HOVER)])

        self.style.configure("Green.TButton", background=ACCENT_2,
                             foreground="#1a1b2e", font=self.font_btn,
                             padding=(16, 8), borderwidth=0)
        self.style.map("Green.TButton",
                       background=[("active", ACCENT_2_HOVER)])

        self.style.configure("Dark.TButton", background=BG_INPUT,
                             foreground=TEXT_PRIMARY, font=self.font_btn,
                             padding=(12, 6), borderwidth=0)
        self.style.map("Dark.TButton",
                       background=[("active", BG_INPUT_FOCUS)])

    # ----- Layout principal -----
    def _crear_interfaz(self):
        # --- Header ---
        header = ttk.Frame(self.root, style="Dark.TFrame")
        header.pack(fill="x", padx=30, pady=(20, 5))

        ttk.Label(header, text="⬡  Método Húngaro", style="Title.TLabel").pack(side="left")
        ttk.Label(header, text="Asignación óptima de recursos",
                  style="Subtitle.TLabel").pack(side="left", padx=(15, 0), pady=(5, 0))

        # Línea decorativa
        linea = tk.Canvas(self.root, height=2, bg=ACCENT, highlightthickness=0)
        linea.pack(fill="x", padx=30, pady=(5, 15))

        # --- Contenedor principal (scroll) ---
        main_container = ttk.Frame(self.root, style="Dark.TFrame")
        main_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        # Panel izquierdo: controles + matriz
        left = ttk.Frame(main_container, style="Dark.TFrame")
        left.pack(side="left", fill="both", expand=True)

        # Panel derecho: resultados
        self.right = ttk.Frame(main_container, style="Dark.TFrame")
        self.right.pack(side="right", fill="both", padx=(15, 0), expand=False)

        # -- Controles superiores --
        ctrl_frame = ttk.Frame(left, style="Panel.TFrame")
        ctrl_frame.pack(fill="x", pady=(0, 12), ipady=10, ipadx=12)

        inner_ctrl = ttk.Frame(ctrl_frame, style="Panel.TFrame")
        inner_ctrl.pack(padx=14, pady=10)

        ttk.Label(inner_ctrl, text="Dimensión  N×N :",
                  style="Label.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8))

        self.dim_var = tk.StringVar(value=str(self.dimension))
        dim_spin = tk.Spinbox(inner_ctrl, from_=2, to=10, width=4,
                              textvariable=self.dim_var,
                              font=self.font_entry,
                              bg=BG_INPUT, fg=TEXT_PRIMARY,
                              buttonbackground=BG_CARD,
                              insertbackground=TEXT_PRIMARY,
                              selectbackground=ACCENT,
                              highlightthickness=1, highlightcolor=ACCENT,
                              highlightbackground=BORDER, bd=0,
                              command=self._on_dim_change)
        dim_spin.grid(row=0, column=1, padx=(0, 20))
        dim_spin.bind("<Return>", lambda e: self._on_dim_change())

        ttk.Button(inner_ctrl, text="⟳  Aplicar dimensión",
                   style="Dark.TButton",
                   command=self._on_dim_change).grid(row=0, column=2, padx=(0, 10))

        ttk.Button(inner_ctrl, text="🎲  Aleatorio",
                   style="Dark.TButton",
                   command=self._rellenar_aleatorio).grid(row=0, column=3, padx=(0, 10))

        ttk.Button(inner_ctrl, text="🗑  Limpiar",
                   style="Dark.TButton",
                   command=self._limpiar_matriz).grid(row=0, column=4)

        # -- Zona de la matriz --
        self.matrix_frame_outer = ttk.Frame(left, style="Panel.TFrame")
        self.matrix_frame_outer.pack(fill="both", expand=True, ipady=10)

        # -- Botones Resolver --
        btn_frame = ttk.Frame(left, style="Dark.TFrame")
        btn_frame.pack(fill="x", pady=(12, 0))

        ttk.Button(btn_frame, text="▼  Minimizar",
                   style="Accent.TButton",
                   command=lambda: self._resolver(False)).pack(side="left", padx=(0, 10))

        ttk.Button(btn_frame, text="▲  Maximizar",
                   style="Green.TButton",
                   command=lambda: self._resolver(True)).pack(side="left")

        ttk.Button(btn_frame, text="🤖  Analizar con Groq",
                   style="Accent.TButton",
                   command=self.analizar_ia).pack(side="left", padx=(10, 0))

        # -- Zona de resultados --
        self._crear_panel_resultados()

    # ----- Panel de resultados -----
    def _crear_panel_resultados(self):
        res_card = ttk.Frame(self.right, style="Card.TFrame")
        res_card.pack(fill="both", expand=True)

        header_res = ttk.Frame(res_card, style="Card.TFrame")
        header_res.pack(fill="x", padx=14, pady=(12, 5))
        ttk.Label(header_res, text="📊  Resultados",
                  font=self.font_result_title,
                  background=BG_CARD, foreground=TEXT_PRIMARY).pack(side="left")

        self.result_text = tk.Text(res_card, wrap="word", width=38, height=25,
                                   font=self.font_result,
                                   bg=BG_CARD, fg=TEXT_PRIMARY,
                                   insertbackground=TEXT_PRIMARY,
                                   selectbackground=ACCENT,
                                   highlightthickness=0, bd=0,
                                   padx=14, pady=8, state="disabled")
        self.result_text.pack(fill="both", expand=True)

        # Tags para formato
        self.result_text.tag_configure("titulo", foreground=ACCENT,
                                        font=tkfont.Font(family="Segoe UI", size=11, weight="bold"))
        self.result_text.tag_configure("asignacion", foreground=ACCENT_2)
        self.result_text.tag_configure("total", foreground=HIGHLIGHT,
                                        font=tkfont.Font(family="Consolas", size=12, weight="bold"))
        self.result_text.tag_configure("info", foreground=TEXT_SECONDARY)
        self.result_text.tag_configure("error", foreground=ERROR)
        self.result_text.tag_configure("ia", foreground="#a5f3fc")
        self.result_text.tag_configure("ia_title", foreground="#38bdf8", font=tkfont.Font(family="Segoe UI", size=10, weight="bold"))

    # ----- Generar / regenerar la grilla -----
    def _generar_matriz(self):
        # Limpiar
        for w in self.matrix_frame_outer.winfo_children():
            w.destroy()
        self.celdas_entries = []
        self.fila_name_entries = []
        self.col_name_entries = []

        n = self.dimension

        # Contenedor interno centrado
        container = ttk.Frame(self.matrix_frame_outer, style="Panel.TFrame")
        container.pack(anchor="center", padx=14, pady=10)

        # Esquina vacía
        corner = tk.Label(container, text="", width=12, bg=BG_PANEL)
        corner.grid(row=0, column=0, padx=1, pady=1)

        # Encabezados de columnas (editables)
        for j in range(n):
            e = tk.Entry(container, width=10, justify="center",
                         font=self.font_label,
                         bg=COL_HEADER_BG, fg=TEXT_PRIMARY,
                         insertbackground=TEXT_PRIMARY,
                         selectbackground=ACCENT,
                         highlightthickness=1, highlightcolor=ACCENT_2,
                         highlightbackground=BORDER, bd=0)
            e.grid(row=0, column=j + 1, padx=1, pady=1, sticky="ew")
            if j < len(self.nombres_cols):
                e.insert(0, self.nombres_cols[j])
            else:
                e.insert(0, "Tarea " + str(j))
            self.col_name_entries.append(e)

        # Filas
        for i in range(n):
            # Nombre de fila (editable)
            ef = tk.Entry(container, width=12, justify="center",
                          font=self.font_label,
                          bg=ROW_HEADER_BG, fg=TEXT_PRIMARY,
                          insertbackground=TEXT_PRIMARY,
                          selectbackground=ACCENT,
                          highlightthickness=1, highlightcolor=ACCENT,
                          highlightbackground=BORDER, bd=0)
            ef.grid(row=i + 1, column=0, padx=1, pady=1, sticky="ew")
            if i < len(self.nombres_filas):
                ef.insert(0, self.nombres_filas[i])
            else:
                ef.insert(0, "Trabajador " + str(i))
            self.fila_name_entries.append(ef)

            fila_entries = []
            for j in range(n):
                e = tk.Entry(container, width=10, justify="center",
                             font=self.font_entry,
                             bg=BG_INPUT, fg=TEXT_PRIMARY,
                             insertbackground=TEXT_PRIMARY,
                             selectbackground=ACCENT,
                             highlightthickness=1,
                             highlightcolor=ACCENT,
                             highlightbackground=BORDER, bd=0)
                e.grid(row=i + 1, column=j + 1, padx=1, pady=1, sticky="ew")
                e.insert(0, "0")
                # Efecto focus
                e.bind("<FocusIn>", lambda ev, entry=e: entry.configure(bg=BG_INPUT_FOCUS))
                e.bind("<FocusOut>", lambda ev, entry=e: entry.configure(bg=BG_INPUT))
                fila_entries.append(e)
            self.celdas_entries.append(fila_entries)

    # ----- Eventos -----
    def _on_dim_change(self):
        try:
            new_dim = int(self.dim_var.get())
        except ValueError:
            return
        if new_dim < 2:
            new_dim = 2
        if new_dim > 10:
            new_dim = 10
        self.dim_var.set(str(new_dim))

        # Guardar valores actuales
        old_values = self._leer_valores_actuales()
        old_n = len(old_values) if old_values else 0
        self._guardar_nombres()

        self.dimension = new_dim
        self._generar_matriz()

        # Restaurar lo que se pueda
        if old_values:
            for i in range(min(old_n, new_dim)):
                for j in range(min(old_n, new_dim)):
                    self.celdas_entries[i][j].delete(0, "end")
                    self.celdas_entries[i][j].insert(0, str(old_values[i][j]))

    def _guardar_nombres(self):
        self.nombres_filas = []
        for e in self.fila_name_entries:
            self.nombres_filas.append(e.get())
        self.nombres_cols = []
        for e in self.col_name_entries:
            self.nombres_cols.append(e.get())

    def _leer_valores_actuales(self):
        if not self.celdas_entries:
            return None
        valores = []
        for fila_e in self.celdas_entries:
            fila = []
            for e in fila_e:
                try:
                    fila.append(int(e.get()))
                except ValueError:
                    fila.append(0)
            valores.append(fila)
        return valores

    def _rellenar_aleatorio(self):
        # Generador congruencial lineal simple (sin import random)
        import time
        seed = int(time.time() * 1000) % (2**31)
        for fila_e in self.celdas_entries:
            for e in fila_e:
                seed = (seed * 1103515245 + 12345) % (2**31)
                val = (seed >> 16) % 100 + 1
                e.delete(0, "end")
                e.insert(0, str(val))

    def _limpiar_matriz(self):
        for fila_e in self.celdas_entries:
            for e in fila_e:
                e.delete(0, "end")
                e.insert(0, "0")
        self._limpiar_resultados()

    def _limpiar_resultados(self):
        self._ultimo_resultado = None
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.configure(state="disabled")
        # Restaurar colores normales de celdas
        for fila_e in self.celdas_entries:
            for e in fila_e:
                e.configure(bg=BG_INPUT, highlightbackground=BORDER,
                            highlightcolor=ACCENT)

    # ----- Resolver -----
    def _resolver(self, maximizar):
        n = self.dimension
        self._guardar_nombres()

        # Leer matriz
        matriz = []
        for i in range(n):
            fila = []
            for j in range(n):
                txt = self.celdas_entries[i][j].get().strip()
                if txt == "":
                    txt = "0"
                try:
                    fila.append(int(txt))
                except ValueError:
                    self._mostrar_error(
                        "Valor inválido en Fila " + str(i) + ", Col " + str(j)
                        + ": '" + txt + "'\nIngrese solo números enteros.")
                    return
            matriz.append(fila)

        # Ejecutar algoritmo
        asignacion, total, pasos = metodo_hungaro(matriz, maximizar=maximizar)
        asignados = set()
        for (f, c) in asignacion:
            asignados.add((f, c))

        # Resaltar celdas asignadas
        for i in range(n):
            for j in range(n):
                if (i, j) in asignados:
                    self.celdas_entries[i][j].configure(
                        bg="#2d4a2d", highlightbackground=SUCCESS,
                        highlightcolor=SUCCESS)
                else:
                    self.celdas_entries[i][j].configure(
                        bg=BG_INPUT, highlightbackground=BORDER,
                        highlightcolor=ACCENT)

        # Mostrar resultados
        modo = "MAXIMIZACIÓN" if maximizar else "MINIMIZACIÓN"
        etiqueta = "Beneficio" if maximizar else "Costo"

        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")

        self.result_text.insert("end", "  " + modo + "\n", "titulo")
        self.result_text.insert("end", "─" * 34 + "\n\n", "info")

        self.result_text.insert("end", "Asignaciones óptimas:\n\n", "info")
        for (f, c) in asignacion:
            nf = self.nombres_filas[f] if f < len(self.nombres_filas) else "Fila " + str(f)
            nc = self.nombres_cols[c] if c < len(self.nombres_cols) else "Col " + str(c)
            linea = "  " + nf + "  →  " + nc + "\n"
            self.result_text.insert("end", linea, "asignacion")
            self.result_text.insert("end",
                                    "    " + etiqueta + ": " + str(matriz[f][c]) + "\n", "info")

        self.result_text.insert("end", "\n" + "─" * 34 + "\n\n", "info")
        self.result_text.insert("end", "Iteraciones del método:\n\n", "info")
        for desc, mat in pasos:
            self.result_text.insert("end", f"  {desc}\n", "info")
            for row in mat:
                r_str = " ".join(f"{v:4}" for v in row)
                self.result_text.insert("end", f"    {r_str}\n", "info")
            self.result_text.insert("end", "\n")

        self.result_text.insert("end", "─" * 34 + "\n", "info")
        if maximizar:
            self.result_text.insert("end",
                                    "  Beneficio total máximo: " + str(total) + "\n", "total")
        else:
            self.result_text.insert("end",
                                    "  Costo total mínimo: " + str(total) + "\n", "total")

        self.result_text.configure(state="disabled")

        self._ultimo_resultado = {
            "matriz_costos": matriz,
            "nombres_filas": self.nombres_filas.copy(),
            "nombres_cols": self.nombres_cols.copy(),
            "asignacion": asignacion,
            "total": total,
            "maximizar": maximizar,
        }

    def _mostrar_error(self, mensaje):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", "  ⚠ ERROR\n\n", "error")
        self.result_text.insert("end", mensaje, "info")
        self.result_text.configure(state="disabled")

    def analizar_ia(self):
        if not hasattr(self, '_ultimo_resultado') or self._ultimo_resultado is None:
            messagebox.showwarning("Aviso", "Primero resuelve el problema para analizarlo.")
            return

        d = self._ultimo_resultado
        matriz = d["matriz_costos"]
        asignacion = d["asignacion"]
        nombres_filas = d["nombres_filas"]
        nombres_cols = d["nombres_cols"]
        maximizar = d["maximizar"]
        total = d["total"]

        modo = "Maximización" if maximizar else "Minimización"

        asignaciones_txt = []
        for (f, c) in asignacion:
            nf = nombres_filas[f] if f < len(nombres_filas) else f"Fila {f}"
            nc = nombres_cols[c] if c < len(nombres_cols) else f"Col {c}"
            val = matriz[f][c]
            asignaciones_txt.append(f"  {nf} → {nc}: valor {val}")

        prompt = (
            "Eres un experto en investigación de operaciones y problemas de asignación.\n"
            f"Se ha resuelto un problema de asignación con el Método Húngaro en modo de {modo}.\n\n"
            f"Trabajadores/Orígenes: {nombres_filas}\n"
            f"Tareas/Destinos: {nombres_cols}\n\n"
            f"Asignaciones óptimas realizadas:\n" + "\n".join(asignaciones_txt) + "\n\n"
            f"Valor óptimo total: {total}\n\n"
            "Por favor:\n"
            "1. Explica brevemente la solución óptima y qué significa en términos prácticos.\n"
            "2. Interpreta si las asignaciones tienen sentido para maximizar/minimizar el resultado.\n"
            "Responde en español, de forma concisa (máx. 150 palabras) y en formato amigable."
        )

        try:
            respuesta = groq_client.consultar_groq(prompt, max_tokens=300)
            self._mostrar_ia(respuesta, error=False)
        except RuntimeError as e:
            self._mostrar_ia(str(e), error=True)

    def _mostrar_ia(self, texto: str, error: bool):
        self.result_text.configure(state="normal")
        if error:
            self.result_text.insert("end", f"\n Error IA: {texto}\n", "error")
        else:
            self.result_text.insert("end", "\n Análisis IA:\n", "ia_title")
            for linea in texto.splitlines():
                self.result_text.insert("end", "  " + linea + "\n", "ia")
        self.result_text.insert("end", "\n" + "─" * 34 + "\n", "info")
        self.result_text.configure(state="disabled")
        self.result_text.see("end")


# =========================================================
#                        MAIN
# =========================================================

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1050x680")

    # Intentar centrar ventana
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry("+{}+{}".format(x, y))

    app = HungaroApp(root)
    root.mainloop()
