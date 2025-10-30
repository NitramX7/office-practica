from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QInputDialog,
    QToolBar,
    QMenu,
    QTextEdit,
    QWhatsThis,
    QFileDialog,
    QColorDialog,
    QFontDialog,
    QMessageBox,
    QStatusBar,
    QWidget,
    QLabel,
    QHBoxLayout



)
from PySide6.QtGui import QAction, QIcon, Qt, QKeySequence, QTextCursor, QTextDocument, QTextCharFormat
import os


# class Ventana (QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.texto = QTextEdit()
#         self.setCentralWidget(self.texto)

#         self.barraTarea = QToolBar()
#         self.addToolBar(self.barraTarea)

#         self.barraEstado = QStatusBar()
#         self.setStatusBar(self.barraEstado)

#         # LADO IZQUIERDO
#         self.palabrasContador = QLabel()
#         leftBox = QWidget()
#         leftLay = QHBoxLayout(leftBox)
#         leftLay.setContentsMargins(0, 0, 0, 0)
#         leftLay.setSpacing(8)
#         leftLay.addWidget(self.palabrasContador)

#         # LADO DERECHO
#         self.operaciones = QLabel()

#         rightBox = QWidget()
#         rightLay = QHBoxLayout(rightBox)
#         rightLay.setContentsMargins(0, 0, 0, 0)
#         rightLay.setSpacing(8)
#         rightLay.addWidget(self.operaciones)

#         self.barraEstado.addWidget(rightBox, 1)
#         self.barraEstado.addPermanentWidget(leftBox)

#         # MENU ARCHIVO Y SUS FUNCIONES
#         self.barraMenus = self.menuBar()
#         menuArchivo = self.barraMenus.addMenu("&Archivo")
#         menuEditar = self.barraMenus.addMenu("&Editar")
#         menuEstilo = self.barraMenus.addMenu("&Estilo")

#         self.accionNuevo = QAction("Nuevo", self)
#         self.accionNuevo.setShortcut(QKeySequence("Ctrl+N"))
#         self.accionNuevo.triggered.connect(self.nuevo)

#         self.accionAbrir = QAction("Abrir")
#         self.accionAbrir.setShortcut(QKeySequence("Ctrl+O"))
#         self.accionAbrir.triggered.connect(self.abrir)

#         self.accionGuardar = QAction("Guardar")
#         self.accionGuardar.setShortcut(QKeySequence("Ctrl+S"))
#         self.accionGuardar.triggered.connect(self.guardar)

#         self.accionSalir = QAction("Salir")
#         self.accionSalir.setShortcut(QKeySequence("Ctrl+Q"))
#         self.accionSalir.triggered.connect(self.salir)

#         menuArchivo.addActions([
#             self.accionNuevo,
#             self.accionAbrir,
#             self.accionGuardar,
#             self.accionSalir
#         ])

#         # MENU EDITAR Y SUS FUNCIONES

#         self.accionDeshacer = QAction("Deshacer", self)
#         self.accionDeshacer.setShortcut(QKeySequence("Ctrl+Z"))
#         self.accionDeshacer.triggered.connect(self.deshacer)

#         self.accionRehacer = QAction("Rehacer", self)
#         self.accionRehacer.setShortcut(QKeySequence("Ctrl+Y"))
#         self.accionRehacer.triggered.connect(self.rehacer)

#         self.accionCopiar = QAction("Copiar", self)
#         self.accionCopiar.setShortcut(QKeySequence("Ctrl+C"))
#         self.accionCopiar.triggered.connect(self.copiar)

#         self.accionCortar = QAction("Cortar", self)
#         self.accionCortar.setShortcut(QKeySequence("Ctrl+X"))
#         self.accionCortar.triggered.connect(self.cortar)

#         self.accionPegar = QAction("Pegar", self)
#         self.accionPegar.setShortcut(QKeySequence("Ctrl+V"))
#         self.accionPegar.triggered.connect(self.pegar)

#         menuEditar.addActions([
#             self.accionDeshacer,
#             self.accionRehacer,
#             self.accionCopiar,
#             self.accionCortar,
#             self.accionPegar
#         ])

#         self.accionColorFondo = QAction("Cambiar fondo color", self)
#         self.accionColorFondo.triggered.connect(self.cambiar_color_fondo)

#         self.accionColorFuente = QAction("Cambiar fuente color", self)
#         self.accionColorFuente.triggered.connect(self.cambiar_color_fuente)

#         # MENU DE ESTILO
#         menuEstilo.addActions([
#             self.accionColorFondo,
#             self.accionColorFuente

#         ])

#         self.texto.textChanged.connect(self.actualizar_contador)

#         self.accionBuscar = QAction("Buscar", self)
#         self.accionBuscar.setShortcut(QKeySequence("Ctrl+F"))
#         self.accionBuscar.triggered.connect(self.buscar)

#         self.accionReemplazar = QAction("Reemplazar", self)
#         self.accionReemplazar.setShortcut(QKeySequence("Ctrl+R"))
#         self.accionReemplazar.triggered.connect(self.reemplazar)

#         self.barraTarea.addActions([

#             self.accionNuevo,
#             self.accionAbrir,
#             self.accionGuardar,
#             self.accionSalir,
#             self.accionDeshacer,
#             self.accionRehacer,
#             self.accionCopiar,
#             self.accionCortar,
#             self.accionPegar,
#             self.accionBuscar,
#             self.accionReemplazar

#         ])

#     def nuevo(self):
#         self.texto.clear()

#     def actualizar_contador(self):

#         texto = self.texto.toPlainText()
#         palabras = texto.split()
#         contador = len(palabras)

#         self.palabrasContador.setText(f"Palabras: ${contador}")

#     def abrir(self):

#         ruta, filtro = QFileDialog().getOpenFileName(
#             self, "Abrir archivo", "", "Todos los archivos(*)")
#         if not ruta or not filtro:
#             return

#         with open(ruta, "r", encoding="utf-8") as f:
#             contenido = f.read()
#             self.texto.setText(contenido)

#         self.operaciones.setText("Abierto con exito✅")

#     def guardar(self):

#         ruta, filtro = QFileDialog().getSaveFileName(
#             self, "Guardar archivo", "", "Todos los archivos(*)"
#         )

#         if not ruta or not filtro:
#             return

#         with open(ruta, "w", encoding="utf-8") as f:
#             f.write(self.texto.toPlainText())

#     def salir(self):
#         self.close()

#     def deshacer(self):

#         self.texto.undo()

#     def rehacer(self):
#         self.texto.redo()

#     def copiar(self):

#         self.texto.copy()

#     def cortar(self):
#         self.texto.cut()

#     def pegar(self):

#         self.texto.paste()

#     def buscar(self):

#         self.texto.moveCursor(QTextCursor.MoveOperation.Start)

#         palabra, ok = QInputDialog.getText(
#             self, "Buscar", "Introduce la palabra a buscar:")
#         if not palabra or not ok:
#             return

#         encontrado = self.texto.find(palabra)
#         if not encontrado:
#             self.barraEstado.showMessage(f"'{palabra}' no encontrado")
#         else:
#             self.barraEstado.showMessage(f"Buscando: '{palabra}'")

#     def reemplazar(self):
#         self.texto.moveCursor(QTextCursor.MoveOperation.Start)

#         palabra, ok = QInputDialog.getText(
#             self, "Buscar", "Que palabra quieres reemplazar:")
#         if not palabra or not ok:
#             return

#         palabra2, ok2 = QInputDialog.getText(
#             self, "Cambiar", "Por que palabra quieres reemplazarla:")
#         if not palabra2 or not ok2:
#             return

#         if self.texto.find(palabra):
#             self.texto.textCursor().insertText(palabra2)
#             self.barraEstado.showMessage("Reemplazado 1")
#         else:
#             self.barraEstado.showMessage(f"'{palabra}' no encontrado")
#             self.texto.textCursor().insertText(palabra2)

#     def cambiar_color_fondo(self):
#         color = QColorDialog.getColor(
#             parent=self, title="Elegir color de fondo")
#         if not color.isValid():
#             QMessageBox().information("Color no válido")
#             return
#         self.texto.setStyleSheet(f"background-color: {color.name()};")

#         from PySide6.QtWidgets import (
#             QApplication,
#             QMainWindow,
#             QInputDialog,
#             QToolBar,
#             QMenu,
#             QTextEdit,
#             QWhatsThis,
#             QFileDialog,
#             QColorDialog,
#             QFontDialog,
#             QMessageBox


#         )


class Ventana (QMainWindow):
    def __init__(self):
        super().__init__()

        self.texto = QTextEdit()
        self.setCentralWidget(self.texto)

        self.barraTarea = QToolBar()
        self.addToolBar(self.barraTarea)

        self.barraEstado = QStatusBar()
        self.setStatusBar(self.barraEstado)

        # Derecha: operaciones (fijo)
        self.operaciones = QLabel("")
        rightBox = QWidget()
        rightLay = QHBoxLayout(rightBox)
        rightLay.setContentsMargins(0, 0, 0, 0)
        rightLay.addWidget(self.operaciones)

        # Izquierda: contador (elástico)
        self.palabrasContador = QLabel("Palabras: 0")
        leftBox = QWidget()
        leftLay = QHBoxLayout(leftBox)
        leftLay.setContentsMargins(0, 0, 0, 0)
        leftLay.addWidget(self.palabrasContador)

        # IZQUIERDA (se expande)
        self.barraEstado.addWidget(leftBox, 1)
        self.barraEstado.addPermanentWidget(rightBox)   # DERECHA (fijo)

        # MENU ARCHIVO Y SUS FUNCIONES
        self.barraMenus = self.menuBar()
        menuArchivo = self.barraMenus.addMenu("&Archivo")
        menuEditar = self.barraMenus.addMenu("&Editar")
        menuEstilo = self.barraMenus.addMenu("&Estilo")

        self.accionNuevo = QAction("Nuevo", self)
        self.accionNuevo.setShortcut(QKeySequence("Ctrl+N"))
        self.accionNuevo.triggered.connect(self.nuevo)

        self.accionAbrir = QAction("Abrir")
        self.accionAbrir.setShortcut(QKeySequence("Ctrl+O"))
        self.accionAbrir.triggered.connect(self.abrir)

        self.accionGuardar = QAction("Guardar")
        self.accionGuardar.setShortcut(QKeySequence("Ctrl+S"))
        self.accionGuardar.triggered.connect(self.guardar)

        self.accionSalir = QAction("Salir")
        self.accionSalir.setShortcut(QKeySequence("Ctrl+Q"))
        self.accionSalir.triggered.connect(self.salir)

        menuArchivo.addActions([
            self.accionNuevo,
            self.accionAbrir,
            self.accionGuardar,
            self.accionSalir
        ])

        # MENU EDITAR Y SUS FUNCIONES

        self.accionDeshacer = QAction("Deshacer", self)
        self.accionDeshacer.setShortcut(QKeySequence("Ctrl+Z"))
        self.accionDeshacer.triggered.connect(self.deshacer)

        self.accionRehacer = QAction("Rehacer", self)
        self.accionRehacer.setShortcut(QKeySequence("Ctrl+Y"))
        self.accionRehacer.triggered.connect(self.rehacer)

        self.accionCopiar = QAction("Copiar", self)
        self.accionCopiar.setShortcut(QKeySequence("Ctrl+C"))
        self.accionCopiar.triggered.connect(self.copiar)

        self.accionCortar = QAction("Cortar", self)
        self.accionCortar.setShortcut(QKeySequence("Ctrl+X"))
        self.accionCortar.triggered.connect(self.cortar)

        self.accionPegar = QAction("Pegar", self)
        self.accionPegar.setShortcut(QKeySequence("Ctrl+V"))
        self.accionPegar.triggered.connect(self.pegar)

        menuEditar.addActions([
            self.accionDeshacer,
            self.accionRehacer,
            self.accionCopiar,
            self.accionCortar,
            self.accionPegar
        ])

        self.accionColorFondo = QAction("Cambiar fondo color", self)
        self.accionColorFondo.triggered.connect(self.cambiar_color_fondo)

        self.accionColorFuente = QAction("Cambiar fuente color", self)
        self.accionColorFuente.triggered.connect(self.cambiar_color_fuente)

        # MENU DE ESTILO
        menuEstilo.addActions([
            self.accionColorFondo,
            self.accionColorFuente

        ])

        self.texto.textChanged.connect(self.actualizar_contador)

        self.accionBuscar = QAction("Buscar", self)
        self.accionBuscar.setShortcut(QKeySequence("Ctrl+F"))
        self.accionBuscar.triggered.connect(self.buscar)

        self.accionReemplazar = QAction("Reemplazar", self)
        self.accionReemplazar.setShortcut(QKeySequence("Ctrl+R"))
        self.accionReemplazar.triggered.connect(self.reemplazar)

        self.barraTarea.addActions([

            self.accionNuevo,
            self.accionAbrir,
            self.accionGuardar,
            self.accionSalir,
            self.accionDeshacer,
            self.accionRehacer,
            self.accionCopiar,
            self.accionCortar,
            self.accionPegar,
            self.accionBuscar,
            self.accionReemplazar

        ])

    def nuevo(self):
        self.texto.clear()
        self.operaciones.setText("Nuevo documento 🆕")
        self.barraEstado.showMessage("Documento nuevo creado", 3000)

    def actualizar_contador(self):

        texto = self.texto.toPlainText()
        palabras = texto.split()
        contador = len(palabras)

        self.palabrasContador.setText(f"Palabras: {contador}")

    def abrir(self):

        ruta, filtro = QFileDialog().getOpenFileName(
            self, "Abrir archivo", "", "Todos los archivos(*)")
        if not ruta or not filtro:
            return

        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
            self.texto.setText(contenido)

        self.operaciones.setText("Archivo abierto ✅")
        self.barraEstado.showMessage(
            f"Abriste: {os.path.basename(ruta)}", 3000)

    def guardar(self, flags):

        ruta, filtro = QFileDialog().getSaveFileName(
            self, "Guardar archivo", "", "Todos los archivos(*)"
        )

        if not ruta or not filtro:
            return

        with open(ruta, "w", encoding="utf-8") as f:
            f.write(self.texto.toPlainText())

        self.operaciones.setText("Archivo guardado 💾")
        self.barraEstado.showMessage(
            f"Guardado: {os.path.basename(ruta)}", 3000)

    def salir(self):
        self.operaciones.setText("Saliendo 👋")
        self.barraEstado.showMessage("Cerrando aplicación...", 1500)

        self.close()

    def deshacer(self):

        self.texto.undo()
        self.operaciones.setText("Deshacer ↩️")
        self.barraEstado.showMessage("Acción deshecha", 2000)

    def rehacer(self):
        self.texto.redo()
        self.operaciones.setText("Rehacer ↪️")
        self.barraEstado.showMessage("Acción rehecha", 2000)

    def copiar(self):

        self.texto.copy()
        self.operaciones.setText("Copiado 📋")
        self.barraEstado.showMessage("Texto copiado", 1500)

    def cortar(self):
        self.texto.cut()
        self.operaciones.setText("Cortado ✂️")
        self.barraEstado.showMessage("Texto cortado", 1500)

    def pegar(self):

        self.texto.paste()
        self.operaciones.setText("Cortado ✂️")
        self.barraEstado.showMessage("Texto cortado", 1500)

    def buscar(self):

        self.texto.moveCursor(QTextCursor.MoveOperation.Start)

        palabra, ok = QInputDialog.getText(
            self, "Buscar", "Introduce la palabra a buscar:")
        if not palabra or not ok:
            return

        encontrado = self.texto.find(palabra)
        if not encontrado:
            self.operaciones.setText(f"No encontrado ❌ '{palabra}'")
            self.barraEstado.showMessage(f"'{palabra}' no encontrado", 3000)
        else:
            self.operaciones.setText(f"Buscando 🔎 '{palabra}'")
            self.barraEstado.showMessage(f"Encontrado: '{palabra}'", 3000)

    def reemplazar(self):
        self.texto.moveCursor(QTextCursor.MoveOperation.Start)

        palabra, ok = QInputDialog.getText(
            self, "Buscar", "Que palabra quieres reemplazar:")
        if not palabra or not ok:
            return

        palabra2, ok2 = QInputDialog.getText(
            self, "Cambiar", "Por que palabra quieres reemplazarla:")
        if not palabra2 or not ok2:
            return

        if self.texto.find(palabra):
            self.operaciones.setText("Reemplazado ✅")
            self.barraEstado.showMessage(f"'{palabra}' → '{palabra2}'", 3000)
        else:
            self.operaciones.setText(
                "Insertado ✍️ (no se encontró coincidencia)")
            self.barraEstado.showMessage(
                f"No se encontró '{palabra}', se insertó '{palabra2}'", 3000)

    def cambiar_color_fondo(self):
        color = QColorDialog.getColor(
            parent=self, title="Elegir color de fondo")
        if not color.isValid():
            QMessageBox().information("Color no válido")
            return
        self.texto.setStyleSheet(f"background-color: {color.name()};")
        self.operaciones.setText("Fondo cambiado 🎨")
        self.barraEstado.showMessage(f"Nuevo fondo: {color.name()}", 3000)

    def cambiar_color_fuente(self):
        color = QColorDialog.getColor(
            parent=self, title="Elegir color de fuente")
        if not color.isValid():
            QMessageBox.information(
                self, "Color no válido", "Selecciona un color válido.")
            return

        fmt = QTextCharFormat()
        fmt.setForeground(color)

        cursor = self.texto.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.Document)
            self.texto.setTextCursor(cursor)

        # Aplica el formato a la selección actual (o a todo si no había selección)
        self.texto.mergeCurrentCharFormat(fmt)

        # Opcional: quitar la selección visual tras aplicar el color
        cursor = self.texto.textCursor()
        cursor.clearSelection()
        self.texto.setTextCursor(cursor)
        self.operaciones.setText("Color de fuente cambiado 🖌️")
        self.barraEstado.showMessage(f"Nuevo color: {color.name()}", 3000)


app = QApplication()

ventana = Ventana()
ventana.show()

app.exec()
