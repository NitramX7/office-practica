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
    QHBoxLayout,
    QDockWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit



)
from PySide6.QtGui import QAction, QIcon, Qt, QKeySequence, QTextCursor, QTextDocument, QTextCharFormat, QFont
import os
import sys
import speech_recognition as sr


class Ventana (QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0f0; color: #000000; }
            QTextEdit { background-color: white; color: #000000; border: 1px solid #ccc; border-radius: 4px; }
            QMenuBar, QMenu, QToolBar, QStatusBar { background-color: #eaeaea; color: #000000; }
            QToolButton, QLabel, QAction, QMenu::item { color: #000000; }
            QPushButton { background-color: #f5f5f5; color: black; border: 1px solid #ccc; border-radius: 4px; padding: 4px; }
            QPushButton:hover { background-color: #ddd; }
            QDockWidget, QToolBar, QStatusBar { border: 1px solid #ccc; }
            QDockWidget::title { background-color: #eaeaea; color: #000000; padding: 4px; border-bottom: 1px solid #ccc; }
        """)

        base_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "imagenes")

        icon_nuevo = QIcon(os.path.join(base_dir, "nuevo.png"))
        icon_abrir = QIcon(os.path.join(base_dir, "abrir.png"))
        icon_guardar = QIcon(os.path.join(base_dir, "guardar.png"))
        icon_salir = QIcon(os.path.join(base_dir, "salir.png"))
        icon_deshacer = QIcon(os.path.join(base_dir, "deshacer.png"))
        icon_rehacer = QIcon(os.path.join(base_dir, "rehacer.png"))
        icon_copiar = QIcon(os.path.join(base_dir, "copiar.png"))
        icon_cortar = QIcon(os.path.join(base_dir, "cortar.png"))
        icon_pegar = QIcon(os.path.join(base_dir, "pegar.png"))
        icon_panel_buscar = QIcon(os.path.join(base_dir, "buscar.png"))
        icon_reemplazar = QIcon(os.path.join(base_dir, "reemplazar.png"))
        icon_voz = QIcon(os.path.join(base_dir, "voz.png"))

        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(
            __file__), "imagenes/iconoApp.ico")))

        self.texto = QTextEdit()
        self.setCentralWidget(self.texto)
        self.ultimaBusqueda = ""

        self.barraTarea = QToolBar()
        self.addToolBar(self.barraTarea)
        self.barraTarea.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.barraEstado = QStatusBar()
        self.setStatusBar(self.barraEstado)

        # Derecha: operaciones (fijo)
        self.operaciones = QLabel("")
        rightBox = QWidget()
        rightLay = QHBoxLayout(rightBox)
        rightLay.setContentsMargins(0, 0, 0, 0)
        rightLay.addWidget(self.operaciones)

        self.buscarOpciones = QDockWidget("Buscar")
        self.buscarOpciones.setAllowedAreas(Qt.RightDockWidgetArea)
        self.reemplazarOpciones = QDockWidget("Reemplazar")
        self.reemplazarOpciones.setAllowedAreas(Qt.RightDockWidgetArea)

        self.buscarPanel = QLineEdit()
        self.buscarPanel.setPlaceholderText("Texto a buscar")
        self.buscarPanel.textChanged.connect(self.actualizaBusqueda)

        # self.btnBuscar = QPushButton("Buscar una palabra")
        # self.btnBuscar.clicked.connect(self.buscar)
        self.btnBuscarTodas = QPushButton("Buscar todas las palabras")
        self.btnBuscarTodas.clicked.connect(self.buscarTodas)
        self.btnSiguiente = QPushButton("Siguiente")
        self.btnSiguiente.clicked.connect(self.siguientePalabra)
        self.btnAnterior = QPushButton("Anterior")
        self.btnAnterior.clicked.connect(self.anteriorPalabra)

        self.contenedorBuscar = QWidget()

        self.buscarOpciones.setWidget(self.contenedorBuscar)

        self.layout = QVBoxLayout(self.contenedorBuscar)
        self.layout.addWidget(QLabel("Buscar:"))
        self.layout.addWidget(self.buscarPanel)

        navBox = QWidget()
        navLay = QHBoxLayout(navBox)
        navLay.setContentsMargins(0, 0, 0, 0)
        navLay.addWidget(self.btnAnterior)
        navLay.addWidget(self.btnSiguiente)
        self.layout.addWidget(navBox)
        # self.layout.addWidget(self.btnBuscar)
        self.layout.addWidget(self.btnBuscarTodas)

        self.addDockWidget(Qt.RightDockWidgetArea, self.buscarOpciones)
        self.buscarOpciones.hide()

        self.busquedaPanel = QLineEdit()
        self.busquedaPanel.setPlaceholderText("Texto a buscar")
        self.inpReemplazar = QLineEdit()
        self.inpReemplazar.setPlaceholderText("Reemplazar por")

        self.btnReemplazar = QPushButton("Reemplazar siguiente")
        self.btnReemplazar.clicked.connect(self.reemplazarSiguiente)
        self.btnReemplazarTodos = QPushButton("Reemplazar todos")
        self.btnReemplazarTodos.clicked.connect(self.reemplazarTodos)

        contenedorReemplazar = QWidget()
        layRe = QVBoxLayout(contenedorReemplazar)
        layRe.addWidget(QLabel("Buscar:"))
        layRe.addWidget(self.busquedaPanel)
        layRe.addWidget(QLabel("Reemplazar por:"))
        layRe.addWidget(self.inpReemplazar)
        layRe.addWidget(self.btnReemplazar)
        layRe.addWidget(self.btnReemplazarTodos)

        self.reemplazarOpciones.setWidget(contenedorReemplazar)
        self.addDockWidget(Qt.RightDockWidgetArea, self.reemplazarOpciones)
        self.reemplazarOpciones.hide()

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

        # Modo oscuro (estado y acción)
        self._modo_oscuro = False
        self.accionModoOscuro = QAction("Modo oscuro", self)
        self.accionModoOscuro.triggered.connect(self.toggle_modo_oscuro)

        self.accionNuevo = QAction("Nuevo", self)
        self.accionNuevo.setShortcut(QKeySequence("Ctrl+N"))
        self.accionNuevo.triggered.connect(self.nuevo)
        self.accionNuevo.setIcon(icon_nuevo)

        self.accionAbrir = QAction("Abrir")
        self.accionAbrir.setShortcut(QKeySequence("Ctrl+O"))
        self.accionAbrir.triggered.connect(self.abrir)
        self.accionAbrir.setIcon(icon_abrir)

        self.accionGuardar = QAction("Guardar")
        self.accionGuardar.setShortcut(QKeySequence("Ctrl+S"))
        self.accionGuardar.triggered.connect(self.guardar)
        self.accionGuardar.setIcon(icon_guardar)

        self.accionSalir = QAction("Salir")
        self.accionSalir.setShortcut(QKeySequence("Ctrl+Q"))
        self.accionSalir.triggered.connect(self.salir)
        self.accionSalir.setIcon(icon_salir)

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
        self.accionDeshacer.setIcon(icon_deshacer)

        self.accionRehacer = QAction("Rehacer", self)
        self.accionRehacer.setShortcut(QKeySequence("Ctrl+Y"))
        self.accionRehacer.triggered.connect(self.rehacer)
        self.accionRehacer.setIcon(icon_rehacer)

        self.accionCopiar = QAction("Copiar", self)
        self.accionCopiar.setShortcut(QKeySequence("Ctrl+C"))
        self.accionCopiar.triggered.connect(self.copiar)
        self.accionCopiar.setIcon(icon_copiar)

        self.accionCortar = QAction("Cortar", self)
        self.accionCortar.setShortcut(QKeySequence("Ctrl+X"))
        self.accionCortar.triggered.connect(self.cortar)
        self.accionCortar.setIcon(icon_cortar)

        self.accionPegar = QAction("Pegar", self)
        self.accionPegar.setShortcut(QKeySequence("Ctrl+V"))
        self.accionPegar.triggered.connect(self.pegar)
        self.accionPegar.setIcon(icon_pegar)

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

        self.accionFuente = QAction("Cambiar fuente", self)
        self.accionFuente.triggered.connect(self.cambiarFuente)

        # MENU DE ESTILO
        menuEstilo.addActions([
            self.accionColorFondo,
            self.accionColorFuente,
            self.accionFuente,
            self.accionModoOscuro

        ])

        self.texto.textChanged.connect(self.actualizar_contador)

        self.accionBuscar = QAction("Buscar", self)
        self.accionBuscar.setShortcut(QKeySequence("Ctrl+F"))
        self.accionBuscar.triggered.connect(self.buscar)

        self.accionBuscarTodas = QAction("Buscar todas", self)
        self.accionBuscarTodas.triggered.connect(self.buscarTodas)

        self.accionReemplazar = QAction("Reemplazar", self)
        self.accionReemplazar.setShortcut(QKeySequence("Ctrl+R"))
        self.accionReemplazar.triggered.connect(self.reemplazar)

        self.accionPanelBuscar = QAction("Mostrar panel de busqueda")
        self.accionPanelBuscar.triggered.connect(self.mostrarPanelBuscar)
        self.accionPanelBuscar.setIcon(icon_panel_buscar)

        self.accionPanelReemplazar = QAction(
            "Mostrar panel de reemplazo", self)
        self.accionPanelReemplazar.triggered.connect(
            self.mostrarPanelReemplazar)
        self.accionPanelReemplazar.setIcon(icon_reemplazar)

        self.accionDictarVoz = QAction("Dictar por voz", self)
        self.accionDictarVoz.triggered.connect(self.dictar_por_voz)
        self.accionDictarVoz.setIcon(icon_voz)

        # Acciones de navegación (atajos)
        self.accionSiguiente = QAction("Siguiente coincidencia", self)
        self.accionSiguiente.setShortcut(QKeySequence("F3"))
        self.accionSiguiente.triggered.connect(self.siguientePalabra)
        self.addAction(self.accionSiguiente)

        self.accionAnterior = QAction("Anterior coincidencia", self)
        self.accionAnterior.setShortcut(QKeySequence("Shift+F3"))
        self.accionAnterior.triggered.connect(self.anteriorPalabra)
        self.addAction(self.accionAnterior)

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
            self.accionPanelBuscar,
            self.accionPanelReemplazar,
            self.accionReemplazar,
            self.accionDictarVoz

        ])

    def nuevo(self):
        self.texto.clear()
        self.operaciones.setText("Nuevo documento 🆕")
        self.barraEstado.showMessage("Documento nuevo creado", 3000)

    def reconocer_voz(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                recognizer.pause_threshold = 1.2
                recognizer.non_speaking_duration = 0.6
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""
        except Exception:
            return None

        try:
            texto = recognizer.recognize_google(audio, language="es-ES")
            return texto.strip()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""

    def dictar_por_voz(self):
        texto = self.reconocer_voz()
        self.procesar_texto_de_voz(texto)

    def procesar_texto_de_voz(self, texto):
        if texto is None:
            self.operaciones.setText("No se pudo procesar la voz")
            self.barraEstado.showMessage("Error al reconocer la voz", 2000)
            return
        if not texto:
            self.operaciones.setText("No se escucho nada")
            self.barraEstado.showMessage("No se detecto audio", 2000)
            return

        comando = texto.lower().strip()

        if "negrita" in comando:
            self._toggle_negrita()
            self.operaciones.setText("Formato: negrita")
            self.barraEstado.showMessage("Negrita activada/desactivada", 2000)
            return

        if "cursiva" in comando:
            self._toggle_cursiva()
            self.operaciones.setText("Formato: cursiva")
            self.barraEstado.showMessage("Cursiva activada/desactivada", 2000)
            return

        if "subrayado" in comando:
            self._toggle_subrayado()
            self.operaciones.setText("Formato: subrayado")
            self.barraEstado.showMessage("Subrayado activado/desactivado", 2000)
            return

        if "guardar" in comando and "archivo" in comando:
            self.operaciones.setText("Guardando por voz")
            self.guardar()
            return

        if "nuevo" in comando and "documento" in comando:
            self.operaciones.setText("Nuevo documento por voz")
            self.nuevo()
            return

        cursor = self.texto.textCursor()
        cursor.insertText(texto + " ")
        self.texto.setTextCursor(cursor)
        self.operaciones.setText("Texto dictado insertado")
        self.barraEstado.showMessage("Dictado insertado en el documento", 2000)

    def _toggle_negrita(self):
        cursor = self.texto.textCursor()
        fmt = cursor.charFormat()
        nuevo_peso = QFont.Normal if fmt.fontWeight() == QFont.Bold else QFont.Bold
        fmt.setFontWeight(nuevo_peso)
        cursor.mergeCharFormat(fmt)
        self.texto.mergeCurrentCharFormat(fmt)

    def _toggle_cursiva(self):
        cursor = self.texto.textCursor()
        fmt = cursor.charFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        cursor.mergeCharFormat(fmt)
        self.texto.mergeCurrentCharFormat(fmt)

    def _toggle_subrayado(self):
        cursor = self.texto.textCursor()
        fmt = cursor.charFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        cursor.mergeCharFormat(fmt)
        self.texto.mergeCurrentCharFormat(fmt)

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

    def guardar(self):

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
        # Guardar y reflejar término en panel
        self.ultimaBusqueda = palabra
        if hasattr(self, 'busquedaPanelPanel'):
            self.busquedaPanel.setText(palabra)

    def reemplazar(self):
        # Reemplazar (dialog) - hace un reemplazo del siguiente encontrado
        palabra, ok = QInputDialog.getText(
            self, "Reemplazar", "Palabra a buscar:")
        if not ok or not palabra:
            return
        nueva, ok2 = QInputDialog.getText(
            self, "Reemplazar", "Reemplazar por:")
        if not ok2:
            return

        # Intenta desde la posición actual; si no, desde el inicio
        if not self.texto.find(palabra):
            self.texto.moveCursor(QTextCursor.MoveOperation.Start)
            if not self.texto.find(palabra):
                self.operaciones.setText(f"No encontrado ❌ '{palabra}'")
                self.barraEstado.showMessage(
                    f"'{palabra}' no encontrado", 3000)
                return
        cursor = self.texto.textCursor()
        cursor.insertText(nueva)
        self.texto.setTextCursor(cursor)
        self.operaciones.setText("Reemplazado ✅")
        self.barraEstado.showMessage(f"'{palabra}' → '{nueva}'", 3000)

    def cambiar_color_fondo(self):
        color = QColorDialog.getColor(
            parent=self, title="Elegir color de fondo")
        if not color.isValid():
            QMessageBox.information(
                self, "Color no válido", "Selecciona un color válido.")
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

    def cambiarFuente(self):
        ok, fuente = QFontDialog.getFont(parent=self)
        if not ok:
            return

        cursor = QTextCursor()

        # if not cursor.hasSelection():
        #     cursor.select(QTextCursor.Document)
        #     self.texto.setTextCursor(cursor)

        fmt = QTextCharFormat()
        fmt.setFont(fuente)

        self.texto.setCurrentCharFormat(fmt)
        self.operaciones.setText("Fuente cambiada 🖌️")
        # self.barraEstado.showMessage(f"Fuente: {fuente.name()}", 3000)

        cursor.clearSelection()

    def buscarTodas(self):
        palabra = self._obtenerPalabraBusqueda()
        if not palabra:
            self.texto.setExtraSelections([])
            self.operaciones.setText("Introduce el texto a buscar")
            self.barraEstado.showMessage("Introduce el texto a buscar", 2000)
            return

        doc = self.texto.document()
        selecciones = []
        contador = 0
        pos = 0

        highlight_bg = self.texto.palette().highlight()
        highlight_fg = self.texto.palette().highlightedText()

        while True:
            cursor = doc.find(palabra, pos)
            if cursor.isNull():
                break

            sel = QTextEdit.ExtraSelection()
            sel.cursor = cursor
            sel.format.setBackground(highlight_bg)
            sel.format.setForeground(highlight_fg)
            selecciones.append(sel)

            pos = cursor.selectionEnd()
            contador += 1

        self.texto.setExtraSelections(selecciones)

        if contador == 0:
            self.operaciones.setText(f"No encontrado ❌ '{palabra}'")
            self.barraEstado.showMessage(
                f"No hubo coincidencias de '{palabra}'", 3000)
        else:
            self.operaciones.setText(
                f"Coincidencias seleccionadas: {contador} 🔎")
            self.barraEstado.showMessage(
                f"Seleccionadas {contador} ocurrencias de '{palabra}'", 3000
            )

        self.ultimaBusqueda = palabra
        if hasattr(self, 'busquedaPanel'):
            self.busquedaPanel.setText(palabra)

    def mostrarPanelBuscar(self):
        if (self.buscarOpciones.isVisible()):
            self.buscarOpciones.hide()
        else:
            self.buscarOpciones.show()

    def mostrarPanelReemplazar(self):
        if self.reemplazarOpciones.isVisible():
            self.reemplazarOpciones.hide()
        else:
            self.reemplazarOpciones.show()

    def reemplazarSiguiente(self):
        palabra = self.busquedaPanel.text()
        nueva = self.inpReemplazar.text()
        if not palabra:
            self.barraEstado.showMessage("Introduce el texto a buscar", 2000)
            return

        if not self.texto.find(palabra):
            self.texto.moveCursor(QTextCursor.MoveOperation.Start)
            if not self.texto.find(palabra):
                self.operaciones.setText(f"No encontrado ❌ '{palabra}'")
                self.barraEstado.showMessage(
                    f"'{palabra}' no encontrado", 3000)
                return

        cursor = self.texto.textCursor()
        cursor.insertText(nueva)
        self.texto.setTextCursor(cursor)
        self.operaciones.setText("Reemplazado ✅")
        self.barraEstado.showMessage(f"'{palabra}' → '{nueva}'", 3000)

    def reemplazarTodos(self):
        palabra = self.busquedaPanel.text()
        nueva = self.inpReemplazar.text()
        if not palabra:
            self.barraEstado.showMessage("Introduce el texto a buscar", 2000)
            return

        self.texto.moveCursor(QTextCursor.MoveOperation.Start)
        contador = 0
        while self.texto.find(palabra):
            cursor = self.texto.textCursor()
            cursor.insertText(nueva)
            self.texto.setTextCursor(cursor)

            contador += 1

        if contador == 0:
            self.operaciones.setText(f"No encontrado ❌ '{palabra}'")
            self.barraEstado.showMessage(
                f"No hubo coincidencias de '{palabra}'", 3000)
        else:
            self.operaciones.setText(f"Reemplazos realizados: {contador} ✅")
            self.barraEstado.showMessage(
                f"Se reemplazaron {contador} ocurrencias de '{palabra}'", 3000)

    def actualizaBusqueda(self, texto: str):

        if not texto:
            self.texto.setExtraSelections([])
            return
        self.ultimaBusqueda = texto
        self._resaltarCoincidencias(texto)

    def _obtenerPalabraBusqueda(self):

        palabra = self.buscarPanel.text().strip()
        if palabra:
            return palabra

    def siguientePalabra(self):
        palabra = self._obtenerPalabraBusqueda()
        if not palabra:
            self.barraEstado.showMessage("Introduce el texto a buscar", 2000)
            return
        if not self.texto.find(palabra):

            self.texto.moveCursor(QTextCursor.MoveOperation.Start)
            if not self.texto.find(palabra):
                self.operaciones.setText(f"No encontrado ? '{palabra}'")
                self.barraEstado.showMessage(
                    f"'{palabra}' no encontrado", 3000)
                return
        self.ultimaBusqueda = palabra

    def anteriorPalabra(self):
        palabra = self._obtenerPalabraBusqueda()
        if not palabra:
            self.barraEstado.showMessage("Introduce el texto a buscar", 2000)
            return
        if not self.texto.find(palabra, QTextDocument.FindBackward):

            self.texto.moveCursor(QTextCursor.MoveOperation.End)
            if not self.texto.find(palabra, QTextDocument.FindBackward):
                self.operaciones.setText(f"No encontrado ? '{palabra}'")
                self.barraEstado.showMessage(
                    f"'{palabra}' no encontrado", 3000)
                return
        self.ultimaBusqueda = palabra

    # def _resaltarCoincidencias(self, palabra):

    #     if not palabra:
    #         self.texto.setExtraSelections([])
    #         return 0

    #     original = self.texto.textCursor()
    #     self.texto.moveCursor(QTextCursor.Start)

    #     selecciones = []
    #     contador = 0
    #     while self.texto.find(palabra):
    #         cursor = self.texto.textCursor()
    #         sel = QTextEdit.ExtraSelection()
    #         sel.cursor = cursor

    #         contador += 1

    #     self.texto.setExtraSelections(selecciones)
    #     self.texto.setTextCursor(original)
    #     return contador

    def toggle_modo_oscuro(self):
        if getattr(self, "_modo_oscuro", False):
            # 🔆 VOLVER A MODO CLARO
            self.setStyleSheet("""
                QMainWindow { background-color: #f0f0f0; color: #000000; }
                QTextEdit { background-color: white; color: #000000; border: 1px solid #ccc; border-radius: 4px; }
                QMenuBar, QMenu, QToolBar, QStatusBar { background-color: #eaeaea; color: #000000; }
                QToolButton, QLabel, QAction, QMenu::item { color: #000000; }
                QPushButton { background-color: #f5f5f5; color: black; border: 1px solid #ccc; border-radius: 4px; padding: 4px; }
                QPushButton:hover { background-color: #ddd; }
                QDockWidget, QToolBar, QStatusBar { border: 1px solid #ccc; }
                QDockWidget::title { background-color: #eaeaea; color: #000000; padding: 4px; border-bottom: 1px solid #ccc; }
            """)
            self._modo_oscuro = False
            self.operaciones.setText("Modo claro ☀️")
            self.barraEstado.showMessage("Modo claro activado", 2000)

        else:
            # 🌙 ACTIVAR MODO OSCURO
            self.setStyleSheet("""
                QMainWindow { background-color: #2b2b2b; color: #f0f0f0; }
                QTextEdit { background-color: #3b3b3b; color: #f0f0f0; border: 1px solid #555; border-radius: 4px; }
                QMenuBar, QMenu, QToolBar, QStatusBar { background-color: #2b2b2b; color: #f0f0f0; }
                QPushButton { background-color: #555; color: white; border-radius: 4px; padding: 4px; }
                QPushButton:hover { background-color: #777; }
                QDockWidget, QToolBar, QStatusBar { border: 1px solid #444; }
                QDockWidget::title { background-color: #333; color: #f0f0f0; padding: 4px; border-bottom: 1px solid #555; }
            """)
            self._modo_oscuro = True
            self.operaciones.setText("Modo oscuro 🌙")
            self.barraEstado.showMessage("Modo oscuro activado", 2000)


app = QApplication()

ventana = Ventana()
ventana.show()

app.exec()
