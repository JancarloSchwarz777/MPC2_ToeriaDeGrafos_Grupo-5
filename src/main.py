import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
from graph import Graph  

# Adaptamos la ruta usando pathlib
ASSETS_DIR = Path.home() / 'Desktop' / 'MPC2' / 'assets'

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Grafos - BFS & DFS")
        self.graph = Graph()

        # Crear el directorio de assets si no existe
        ASSETS_DIR.mkdir(parents=True, exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("600x600")
        self.canvas = tk.Canvas(self.root, bg='lightblue')
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='lightblue')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Variables para la interfaz
        self.vertex_entry = tk.Entry(self.scrollable_frame)
        self.edge_entry = tk.Entry(self.scrollable_frame)
        self.vertex_listbox = tk.Listbox(self.scrollable_frame, height=6)
        self.edge_listbox = tk.Listbox(self.scrollable_frame, height=6)
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.scrollable_frame, text="Vértice:", bg='lightblue', font=('Helvetica', 12)).grid(row=0, column=0)
        self.vertex_entry.grid(row=0, column=1)
        tk.Button(self.scrollable_frame, text="Agregar Vértice", command=self.add_vertex, bg='green', fg='white', font=('Helvetica', 10)).grid(row=0, column=2)

        tk.Label(self.scrollable_frame, text="Arista (formato: A-B):", bg='lightblue', font=('Helvetica', 12)).grid(row=1, column=0)
        self.edge_entry.grid(row=1, column=1)
        tk.Button(self.scrollable_frame, text="Agregar Arista", command=self.add_edge, bg='green', fg='white', font=('Helvetica', 10)).grid(row=1, column=2)

        tk.Button(self.scrollable_frame, text="Generar Grafo", command=self.render_graph, bg='blue', fg='white', font=('Helvetica', 10)).grid(row=2, column=1)

        self.setup_listboxes()
        self.setup_graph_display()
        self.setup_run_buttons()
        self.setup_clear_button()

    def setup_listboxes(self):
        vertex_frame = tk.Frame(self.scrollable_frame, bg='lightblue')
        vertex_frame.grid(row=3, column=0)
        tk.Label(vertex_frame, text="Vértices Agregados:", bg='lightblue', font=('Helvetica', 12)).pack()
        self.vertex_listbox = tk.Listbox(vertex_frame, height=6, bg='lightyellow', font=('Helvetica', 10))
        self.vertex_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        vertex_scrollbar = tk.Scrollbar(vertex_frame, orient=tk.VERTICAL, command=self.vertex_listbox.yview)
        vertex_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vertex_listbox.config(yscrollcommand=vertex_scrollbar.set)

        edge_frame = tk.Frame(self.scrollable_frame, bg='lightblue')
        edge_frame.grid(row=3, column=1)
        tk.Label(edge_frame, text="Aristas Agregadas:", bg='lightblue', font=('Helvetica', 12)).pack()
        self.edge_listbox = tk.Listbox(edge_frame, height=6, bg='lightyellow', font=('Helvetica', 10))
        self.edge_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        edge_scrollbar = tk.Scrollbar(edge_frame, orient=tk.VERTICAL, command=self.edge_listbox.yview)
        edge_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.edge_listbox.config(yscrollcommand=edge_scrollbar.set)

    def setup_graph_display(self):
        tk.Label(self.scrollable_frame, text="Grafo Original:", bg='lightblue', font=('Helvetica', 12)).grid(row=5, column=0)
        self.original_canvas = tk.Label(self.scrollable_frame, bg='white')
        self.original_canvas.grid(row=6, column=0, columnspan=3)

        tk.Label(self.scrollable_frame, text="Grafo BFS:", bg='lightblue', font=('Helvetica', 12)).grid(row=8, column=0)
        self.bfs_canvas = tk.Label(self.scrollable_frame, bg='white')
        self.bfs_canvas.grid(row=9, column=0, columnspan=3)

        tk.Label(self.scrollable_frame, text="Grafo DFS:", bg='lightblue', font=('Helvetica', 12)).grid(row=10, column=0)
        self.dfs_canvas = tk.Label(self.scrollable_frame, bg='white')
        self.dfs_canvas.grid(row=11, column=0, columnspan=3)

    def setup_run_buttons(self):
        tk.Button(self.scrollable_frame, text="Ejecutar BFS", command=self.run_bfs, bg='orange', fg='black', font=('Helvetica', 10)).grid(row=7, column=0)
        tk.Button(self.scrollable_frame, text="Ejecutar DFS", command=self.run_dfs, bg='orange', fg='black', font=('Helvetica', 10)).grid(row=7, column=2)

    def setup_clear_button(self):
        tk.Button(self.scrollable_frame, text="Limpiar", command=self.clear_graph, bg='red', fg='white', font=('Helvetica', 10)).grid(row=12, column=1)

    def clear_graph(self):
        self.vertex_entry.delete(0, tk.END)
        self.edge_entry.delete(0, tk.END)
        self.vertex_listbox.delete(0, tk.END)
        self.edge_listbox.delete(0, tk.END)

        self.original_canvas.config(image='')
        self.bfs_canvas.config(image='')
        self.dfs_canvas.config(image='')
        self.graph = Graph()
        messagebox.showinfo("Limpiar", "Todos los datos han sido limpiados.")

    def add_vertex(self):
        vertex = self.vertex_entry.get()
        if vertex:
            self.graph.add_vertex(vertex)
            self.vertex_listbox.insert(tk.END, vertex)
            messagebox.showinfo("Éxito", f"Vértice {vertex} agregado.")
        else:
            messagebox.showerror("Error", "Debe ingresar un vértice.")

    def add_edge(self):
        edge = self.edge_entry.get()
        try:
            u, v = edge.split('-')
            self.graph.add_edge(u.strip(), v.strip())
            self.edge_listbox.insert(tk.END, f"{u} -- {v}")
            messagebox.showinfo("Éxito", f"Arista {u} -- {v} agregada.")
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto. Use A-B.")

    def render_graph(self):
        self.graph.render_graph('original')
        self.show_image(ASSETS_DIR / 'original.png', self.original_canvas)

    def run_bfs(self):
        start_vertex = self.vertex_entry.get()
        if start_vertex not in self.graph.graph:
            messagebox.showerror("Error", "Vértice no encontrado.")
            return
        _, bfs_edges = self.graph.bfs(start_vertex)
        self.graph.render_graph('bfs', bfs_edges)
        self.show_image(ASSETS_DIR / 'bfs.png', self.bfs_canvas)

    def run_dfs(self):
        start_vertex = self.vertex_entry.get()
        if start_vertex not in self.graph.graph:
            messagebox.showerror("Error", "Vértice no encontrado.")
            return
        _, dfs_edges = self.graph.dfs(start_vertex)
        self.graph.render_graph('dfs', dfs_edges)
        self.show_image(ASSETS_DIR / 'dfs.png', self.dfs_canvas)

    def show_image(self, image_path, canvas):
        if image_path.exists():
            img = Image.open(image_path)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            canvas.config(image=img_tk)
            canvas.image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
