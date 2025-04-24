import logica.Graph as Graph
import logica.Uniform_Cost as Uniform_Cost
from logica.printPP import printPP
from logica.printPQtGrpah import crearGraph

import sys, os
from pathlib import Path


# Rutas absolutas para los archivos de recursos
def absPath(file):
    #print("Ruta absoluta: ", str(Path(__file__).parent.absolute() / file))
    return str(Path(__file__).parent.absolute() / file)


from PySide6.QtWidgets import (QApplication, QMainWindow, QStatusBar, QLabel, QVBoxLayout, QFileDialog, QDialog, QDialogButtonBox, 
                               QComboBox, QSpacerItem, QSizePolicy, QHBoxLayout, QToolBar, QWidget, QDockWidget, QTextEdit)

from PySide6.QtCore import Qt

from PySide6.QtGui import QAction, QIcon

import pyqtgraph as pg

class DialogoInicio(QDialog):
    
    def __init__(self, parent=None, grafo=None):
        super().__init__(parent)
        self.setWindowTitle("Selección de nodo de inicio")
        self.setModal(True)  # Hacer el diálogo modal
        self.setWindowIcon(QIcon(absPath("recursos\\inicio.png")))
        self.setFixedSize(240, 120)
        
        self.inicio = None

        # creamos un layout y lo establecemos en el widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # podemos añadir una etiqueta
        layout.addWidget(QLabel("Selecciona el nodo de inicio:"))
        
        # Layout horizontal para centrar el comboBox
        h_layout = QHBoxLayout()
        spacer_izq = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_der = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # añadimos un comboBox para seleccionar el nodo de inicio
        self.comboBox = QComboBox(self)
        self.comboBox.setMinimumWidth(150)
        
        # añadimos los nodos del grafo al comboBox
        self.comboBox.addItem("Selecciona un nodo")
        for nodo in grafo.nodes(data=True):
            self.comboBox.addItem(str(nodo[0]))

        h_layout.addItem(spacer_izq)
        h_layout.addWidget(self.comboBox)
        h_layout.addItem(spacer_der)

        layout.addLayout(h_layout)

        # conectamos los botones a sus funciones
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.aceptar)
        botones.rejected.connect(self.reject)
        botones.button(QDialogButtonBox.Ok).setText("Aceptar")
        botones.button(QDialogButtonBox.Cancel).setText("Cancelar")
        layout.addWidget(botones)

    def aceptar(self):
        texto = self.comboBox.currentText()
        if texto != "Selecciona un nodo":
            self.inicio = texto
            self.accept()
        else:
            self.reject()


class DialogoFinal(QDialog):
    
    def __init__(self, parent=None, grafo=None):
        super().__init__(parent)
        self.setWindowTitle("Selección de nodo objetivo")
        self.setModal(True)  # Hacer el diálogo modal
        self.setWindowIcon(QIcon(absPath("recursos\\meta.png")))
        self.setFixedSize(240, 120)
        
        self.objetivo = None

        # creamos un layout y lo establecemos en el widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # podemos añadir una etiqueta
        layout.addWidget(QLabel("Selecciona el nodo objetivo:"))
        
        # Layout horizontal para centrar el comboBox
        h_layout = QHBoxLayout()
        spacer_izq = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacer_der = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # añadimos un comboBox para seleccionar el nodo de inicio
        self.comboBox = QComboBox(self)
        self.comboBox.setMinimumWidth(150)
        
        # añadimos los nodos del grafo al comboBox
        self.comboBox.addItem("Selecciona un nodo")
        for nodo in grafo.nodes(data=True):
            self.comboBox.addItem(str(nodo[0]))

        h_layout.addItem(spacer_izq)
        h_layout.addWidget(self.comboBox)
        h_layout.addItem(spacer_der)

        layout.addLayout(h_layout)

        # conectamos los botones a sus funciones
        botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botones.accepted.connect(self.aceptar)
        botones.rejected.connect(self.reject)
        botones.button(QDialogButtonBox.Ok).setText("Aceptar")
        botones.button(QDialogButtonBox.Cancel).setText("Cancelar")
        layout.addWidget(botones)

    def aceptar(self):
        texto = self.comboBox.currentText()
        if texto != "Selecciona un nodo":
            self.objetivo = texto
            self.accept()
        else:
            self.reject()


class MainWindow(QMainWindow):
    
    inicio = None
    objetivo = None
    grafo = None
    net = None
    
    inicio_o_final = 0
    reiniciar = 0
    
    def __init__(self):
        super().__init__()
        
        self.inicio_o_final = 0
        
        # Para el tamaño inicial de la ventana
        self.setGeometry(100, 100, 1150, 600)
        
        self.setStyleSheet("background-color: #21262c;")

        self.setWindowTitle("Uniform Cost Search")  # Título de la ventana
        
        self.setWindowIcon(QIcon(absPath("recursos\\nodo.ico")))    # Para el icono de la ventana
        
        self.setStatusBar(QStatusBar(self)) # Barra de estado
        
        
        # Crear un único central widget y layout principal
        central_widget = QWidget()
        
        self.setCentralWidget(central_widget)
        
        self.layout = QVBoxLayout()
        
        central_widget.setLayout(self.layout)
        
        central_widget.setStyleSheet("background-color: #1d2125;")
        
        # Construir elementos de UI
        self.construir_menu()    # Para la barra de menú:
        
        self.construir_herramientas()   # Para la Barra de herramientas:
        
        self.construir_Etiquetas_Nodos()    # Etiqueta de estado de nodos:
        
        self.construir_area_grafo() # Para el área del grafo:
        
        self.construir_dock_editor() # Para el editor de texto:


    def construir_dock_editor(self):
        # Crear el dock widget
        dock = QDockWidget("Método paso a paso", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea | Qt.BottomDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        
        # Agrandar
        dock.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        dock.setFixedWidth(500)

        # Crear el cuadro de texto
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Aquí se mostrará el método paso a paso... Ejecuta el algoritmo para ver los resultados.")
        self.text_edit.setStyleSheet("background-color: #444d56;")

        # Establecer el QTextEdit como contenido del dock
        dock.setWidget(self.text_edit)
        
        dock.setStyleSheet("""
                            QDockWidget::title {
                                background-color: #1d2125;
                                color: white;
                                padding: 5px;
                                font-weight: bold;
                            }
                        """)

        # Añadir el dock a la ventana principal
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    
    def cambiar_color_nodo(self, nodo, color):
        
        if nodo in self.node_list:
            index = self.node_list.index(nodo)
            self.node_colors[index] = pg.mkColor(color)
            self.graph_item.setData(
                pos=self.node_positions,
                adj=self.edges,
                size=self.node_sizes,
                symbol='o',
                pxMode=True,
                brush=self.node_colors,
                pen={'color': 'w', 'width': 1},
                width=self.edge_widths,
                symbolPen='w'
            )
                        
    
    def construir_area_grafo(self):
    
        # Crear el área de visualización del grafo
        self.area_grafo = QWidget(self)
        
        # Crear un layout vertical para el área del grafo
        layout = QVBoxLayout()
        self.area_grafo.setLayout(layout)
        
        # Crear el widget de pyqtgraph donde se dibujará el grafo
        self.plot_widget = pg.PlotWidget()
        
        # Ocultar los ejes X e Y
        self.plot_widget.getPlotItem().hideAxis('left')
        self.plot_widget.getPlotItem().hideAxis('bottom')
        self.plot_widget.setBackground('#444d56')
        
        # para detectar clics en el área de visualización
        self.plot_widget.scene().sigMouseClicked.connect(self.on_mouse_click)
        
        # Agregar el plot al layout
        layout.addWidget(self.plot_widget)
        
        # Agregar al layout principal
        self.layout.addWidget(self.area_grafo)
       
       
    def on_mouse_click(self, event):
        if self.grafo is not None:
            pos = event.scenePos()
            mouse_point = self.plot_widget.getPlotItem().vb.mapSceneToView(pos)
            x, y = mouse_point.x(), mouse_point.y()

            threshold = 0.05 # distancia máxima en píxeles para detectar clic

            # Buscar nodo más cercano
            for i, (nx, ny) in enumerate(self.node_positions):
                distance = ((x - nx)**2 + (y - ny)**2) ** 0.5
                if distance < threshold:
                    #print(f"Nodo {i} clicado en posición ({nx}, {ny})")
                    self.nodo_clicado(i)
                    break
    
    
    def nodo_clicado(self, index):
        # Mostrar el nombre del nodo clicado en la barra de estado
        nombre = self.labels[index].toPlainText()
        
        if self.reiniciar == 1:
            
            # Limpiamos ruta:
            self.limpiar_ruta()
            
            self.reiniciar = 0
        
        # Cambiar el color del nodo clicado
        if self.inicio_o_final == 0:
            self.cambiar_color_nodo(self.inicio, (0, 122, 255))  # Regresar el color del nodo de inicio anterior
            self.inicio = nombre
            self.inicio_o_final = 1
            self.statusBar().showMessage(f"Nodo de inicio seleccionado: {self.inicio}")
            self.info_label.setText(f"Inicio: {self.inicio}  |  Objetivo: {self.objetivo if self.objetivo else 'Ninguno'}")
            self.cambiar_color_nodo(self.inicio, '#c40e56')  # Cambiar el color del nodo de inicio
        
        elif self.inicio_o_final == 1:
            self.cambiar_color_nodo(self.objetivo, (0, 122, 255))  # Regresar el color del nodo de inicio anterior
            self.objetivo = nombre
            self.inicio_o_final = 0
            self.statusBar().showMessage(f"Nodo objetivo seleccionado: {self.objetivo}")
            self.info_label.setText(f"Inicio: {self.inicio if self.inicio else 'Ninguno'}  |  Objetivo: {self.objetivo}")
            self.cambiar_color_nodo(self.objetivo, '#c40e56')  # Cambiar el color del nodo objetivo
          

    def actualizar_area_grafo( self ):
        
        # Limpiar el área de visualización
        self.plot_widget.clear()
        
        # Crear el grafo en el área de visualización
        self.plot_widget.addItem(self.graph_item)
        
        # Añadir etiquetas a los nodos
        for label in self.labels:
            self.plot_widget.addItem(label)
        
        # Mostrar pesos en las aristas
        for text in self.texts:
            self.plot_widget.addItem(text)
        
    
    def construir_Etiquetas_Nodos(self):
        
        # Etiqueta de estado de nodos
        self.info_label = QLabel("Inicio: Ninguno  |  Objetivo: Ninguno")
        
        # Establecer el estilo de la etiqueta
        self.info_label.setAlignment(Qt.AlignCenter)
        
        # Añadir la etiqueta de estado al layout
        self.layout.addWidget(self.info_label)
                
        
    def construir_menu(self):
        
        # Crear la barra de menú
        menu_bar = self.menuBar()
        
        menu_bar.setStyleSheet("""
                QMenuBar {
                    background-color: #1d2125;
                    color: white;
                }

                QMenuBar::item {
                    background-color: transparent;
                    padding: 5px 15px;
                }

                QMenuBar::item:selected {
                    background-color: #21262c;
                }

                QMenu {
                    background-color: #444d56;
                    color: white;
                }

                QMenu::item:selected {
                    background-color: #21262c;
                }
            """)
        
        # Crear el menú "Archivo"
        archivo_menu = menu_bar.addMenu("&Archivo")
        
        # Crear las acciones del menú
        self.crearAccionesArchivo(archivo_menu)

        
        # Crear el menú "Selección"
        seleccion_menu = menu_bar.addMenu("&Selección")
        
        # Crear las acciones del menú
        self.crearAccionesSeleccion(seleccion_menu)
        
        
    def construir_herramientas(self):
        
        # Crear la barra de herramientas
        tool_bar = QToolBar("Herramientas")
        
        tool_bar.setStyleSheet(" QToolBar { border: none; } ")
        
        # Crear las accioenses de la barra de herramientas
        self.crearHerramientas( tool_bar )
        
        # Añadir la barra de herramientas a la ventana principal
        self.addToolBar(tool_bar)
        
        
    def crearHerramientas(self, tool_bar):
        
        # Acción: Abrir archivo
        abrir_action = QAction(QIcon(absPath("recursos\\abrir.png")), "&Abrir", self)
        abrir_action.setStatusTip("Abrir archivo JSON para la construcción del grafo.")
        abrir_action.triggered.connect(self.open_file)
        tool_bar.addAction(abrir_action)
        
        # Acción: Descargar archivo
        descargar_action = QAction(QIcon(absPath("recursos\\descargar.png")), "&Descargar", self)
        descargar_action.setStatusTip("Guardar método paso a paso en un archivo.")
        descargar_action.triggered.connect(self.descargar_archivo)
        tool_bar.addAction(descargar_action)
        
        # Separador
        espacio = QWidget()
        espacio.setFixedWidth(20)
        tool_bar.addWidget(espacio)
        
        # Acción: Nodo de inicio
        inicio_action = QAction(QIcon(absPath("recursos\\inicio.png")), "Nodo de &inicio", self)
        inicio_action.setStatusTip("Seleccionar nodo de inicio")
        inicio_action.triggered.connect(self.seleccionar_inicio)
        tool_bar.addAction(inicio_action)
        
        # Acción: Nodo objetivo
        objetivo_action = QAction(QIcon(absPath("recursos\\meta.png")), "Nodo &objetivo", self)
        objetivo_action.setStatusTip("Seleccionar nodo objetivo")
        objetivo_action.triggered.connect(self.seleccionar_objetivo)
        tool_bar.addAction(objetivo_action)
        
        # Separador
        espacio = QWidget()
        espacio.setFixedWidth(20)
        tool_bar.addWidget(espacio)
        
        # Ejecutar Uniform Cost Search
        ejecutar_action = QAction(QIcon(absPath("recursos\\ejecutar.png")), "&Ejecutar", self)
        ejecutar_action.setStatusTip("Ejecutar Uniform Cost Search")
        ejecutar_action.setShortcut("Ctrl+Return")
        ejecutar_action.triggered.connect(self.ejecutar_uniform_cost_search)
        tool_bar.addAction(ejecutar_action)
        
        # Limpiar grafo
        limpiar_action = QAction(QIcon(absPath("recursos\\limpiar.png")), "&Limpiar", self)
        limpiar_action.setStatusTip("Limpiar ruta del grafo")
        limpiar_action.setShortcut("Ctrl+L")
        limpiar_action.triggered.connect(self.limpiar_ruta)
        tool_bar.addAction(limpiar_action)
    
        
    def crearAccionesArchivo(self, archivo_menu):
        # Acción: Abrir archivo
        abrir_action = QAction(QIcon(absPath("recursos\\abrir.png")), "&Abrir", self)
        abrir_action.setShortcut("Ctrl+O")
        abrir_action.setStatusTip("Abrir archivo JSON para la construcción del grafo.")
        abrir_action.triggered.connect(self.open_file)
        archivo_menu.addAction(abrir_action)

        # Acción: Descargar archivo
        descargar_action = QAction(QIcon(absPath("recursos\\descargar.png")), "&Descargar", self)
        descargar_action.setShortcut("Ctrl+S")
        descargar_action.setStatusTip("Guardar método paso a paso en un archivo.")
        descargar_action.triggered.connect(self.descargar_archivo)
        archivo_menu.addAction(descargar_action)

        # Separador
        archivo_menu.addSeparator()

        # Acción: Acerca de
        acerca_action = QAction(QIcon(absPath("recursos\\info.png")), "A&cerca de", self)
        acerca_action.setStatusTip("Muestra la documentación de la aplicación.")
        acerca_action.triggered.connect(self.mostrar_acerca_de)
        archivo_menu.addAction(acerca_action)

        # Acción: Salir
        salir_action = QAction(QIcon(absPath("recursos\\salida.png")), "S&alir", self)
        salir_action.setShortcut("Ctrl+Q")
        salir_action.setStatusTip("Cerrar la aplicación")
        salir_action.triggered.connect(self.close)
        archivo_menu.addAction(salir_action)
    
    
    def crearAccionesSeleccion(self, seleccion_menu):
        
        # Acción: Seleccionar nodo de inicio
        inicio_action = QAction(QIcon(absPath("recursos\\inicio.png")), "Nodo de &inicio", self)
        inicio_action.setStatusTip("Seleccionar nodo de inicio")
        inicio_action.triggered.connect(self.seleccionar_inicio)
        seleccion_menu.addAction(inicio_action)
        
        # Acción: Seleccionar nodo objetivo
        objetivo_action = QAction(QIcon(absPath("recursos\\meta.png")), "Nodo &objetivo", self)
        objetivo_action.setStatusTip("Seleccionar nodo objetivo")
        objetivo_action.triggered.connect(self.seleccionar_objetivo)
        seleccion_menu.addAction(objetivo_action)
        
        
    def seleccionar_inicio(self):
        if self.grafo:
            
            if self.reiniciar == 1:
            
                # Limpiamos ruta:
                self.limpiar_ruta()
                
                self.inicio_o_final = 1
                self.reiniciar = 0
            
            # Obtenemos el nodo de inicio
            dialogo = DialogoInicio(self, grafo=self.grafo)
            if dialogo.exec() == QDialog.Accepted:
                self.cambiar_color_nodo(self.inicio, (0, 122, 255))  # Regresar el color del nodo de inicio anterior
                self.inicio = dialogo.inicio
                self.statusBar().showMessage(f"Nodo de inicio seleccionado: {self.inicio}")
                self.info_label.setText(f"Inicio: {self.inicio}  |  Objetivo: {self.objetivo if self.objetivo else 'Ninguno'}")
                self.cambiar_color_nodo(self.inicio, '#c40e56')  # Cambiar el color del nodo de inicio
        else:
            self.statusBar().showMessage("Primero debes abrir un archivo de grafo.")
    
    
    def seleccionar_objetivo(self):
        if self.grafo:
            
            if self.reiniciar == 1:
            
                # Limpiamos ruta:
                self.limpiar_ruta()
                
                self.reiniciar = 0
            
            # Obtenemos el nodo objetivo
            dialogo = DialogoFinal(self, grafo=self.grafo)
            if dialogo.exec() == QDialog.Accepted:
                self.cambiar_color_nodo(self.objetivo, (0, 122, 255))  # Regresar el color del nodo de inicio anterior
                self.objetivo = dialogo.objetivo
                self.statusBar().showMessage(f"Nodo de inicio seleccionado: {self.objetivo}")
                self.info_label.setText(f"Inicio: {self.inicio if self.inicio else 'Ninguno'}  |  Objetivo: {self.objetivo}")
                self.cambiar_color_nodo(self.objetivo, '#c40e56')  # Cambiar el color del nodo objetivo
        else:
            self.statusBar().showMessage("Primero debes abrir un archivo de grafo.")
    
    
    def open_file(self):
        
        # Abrir un diálogo de archivo para seleccionar el archivo JSON
        file, _ = QFileDialog.getOpenFileName(self, "Abrir archivo JSON", "", "JSON Files (*.json)")
        
        # Verificar si se seleccionó un archivo
        if file:
            
            # Cargar el grafo desde el archivo JSON
            self.grafo = Graph.crearGraph(file)
            self.node_list = list(self.grafo.nodes())

            # Crear el grafo en el área de visualización
            self.plot_widget.clear()  # Limpiar el área de visualización
            self.graph_item, self.labels, self.texts, self.node_positions,  self.edges, self.node_sizes, self.node_colors, self.edge_widths = crearGraph(self.grafo)
            self.actualizar_area_grafo( )

            # Actualizar la barra de estado con el nombre del archivo
            nombre_archivo = os.path.basename(file)
            self.statusBar().showMessage(f"Archivo abierto: {nombre_archivo}")


    def descargar_archivo(self):
        
        texto = self.text_edit.toPlainText()
        
        if texto:
            # Abrir un diálogo de archivo para guardar el archivo
            file, _ = QFileDialog.getSaveFileName(self, "Guardar archivo", "", "Text Files (*.txt)")
            
            # Verificar si se seleccionó un archivo
            if file:
                with open(file, "w") as f:
                    f.write(texto)
                self.statusBar().showMessage(f"Archivo guardado: {file}")
    
    
    def mostrar_acerca_de(self):
        pass
    
    
    def pintar_ruta(self, ruta):
        # Cambiar el color de los nodos en la ruta
        for nodo in ruta:
            if nodo in self.node_list:
                index = self.node_list.index(nodo)
                self.node_colors[index] = pg.mkColor('#c40e56')  # Cambiar el color a rojo
                self.graph_item.setData(
                    pos=self.node_positions,
                    adj=self.edges,
                    size=self.node_sizes,
                    symbol='o',
                    pxMode=True,
                    brush=self.node_colors,
                    pen={'color': 'w', 'width': 1},
                    width=self.edge_widths,
                    symbolPen='w'
                )
    
    
    def limpiar_ruta(self):
        
        if self.grafo is not None:
            # Regresar el color de los nodos a su estado original
            for nodo in self.node_list:
                index = self.node_list.index(nodo)
                self.node_colors[index] = pg.mkColor(0, 122, 255)  # Cambiar el color a rojo
                self.graph_item.setData(
                    pos=self.node_positions,
                    adj=self.edges,
                    size=self.node_sizes,
                    symbol='o',
                    pxMode=True,
                    brush=self.node_colors,
                    pen={'color': 'w', 'width': 1},
                    width=self.edge_widths,
                    symbolPen='w'
                )
            
            # Limpiar el cuadro de texto
            self.text_edit.clear()
            self.text_edit.setPlaceholderText("Aquí se mostrará el método paso a paso... Ejecuta el algoritmo para ver los resultados.")
            
            # Limpiar los nodos de inicio y objetivo
            self.inicio = None
            self.objetivo = None
            self.inicio_o_final = 0
            
            # Actualizar la etiqueta de estado
            self.info_label.setText("Inicio: Ninguno  |  Objetivo: Ninguno")
            
            # Limpiar la barra de estado
            self.statusBar().showMessage("Ruta limpiada. Selecciona nuevos nodos de inicio y objetivo.")
            
        
    def ejecutar_uniform_cost_search(self):
        
        if self.grafo is not None:
            # Uniform Cost Search
            camino, costo, paso_paso = Uniform_Cost.uniform_cost_search(self.grafo, self.inicio, self.objetivo)
            
            # Escribir el resultado en el editor de texto
            self.text_edit.clear()
            self.text_edit.append("Resultado del algoritmo Uniform Cost Search:\n")
            self.text_edit.append(f"Inicio: {self.inicio}")
            self.text_edit.append(f"Objetivo: {self.objetivo}")
            
            self.text_edit.append("\nNivel\tCosto\tVisitados\tCamino")
            self.text_edit.append(paso_paso)  
            
            self.text_edit.append(f"\nRuta: {camino}")
            self.text_edit.append(f"\nCosto: {costo}")
            
            self.pintar_ruta(camino)
            
            self.reiniciar = 1


# Ejecutar Uniform Cost Search y mostrar el resultado
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())