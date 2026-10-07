import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QCheckBox, QPushButton,
                             QTreeWidget, QTreeWidgetItem, QMessageBox, QGroupBox)

class SistemaPedidosApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Toma de Pedidos")
        self.resize(450, 600)

        # 1. Opciones y precios fijos directamente en el código
        self.menu_items = {
            "Hamburguesa Clásica": 5.00,
            "Hamburguesa Doble": 7.50,
            "Perro Caliente": 3.00,
            "Papas Fritas Grandes": 2.50,
            "Refresco 600ml": 1.50,
            "Jugo Natural": 2.00,
            "Postre del Día": 3.50
        }

        self.checkboxes = [] # Lista para guardar la referencia a las cajas de selección

        self.init_ui()

    def init_ui(self):
        layout_principal = QVBoxLayout()

        # --- Sección: Nombre del Cliente ---
        layout_cliente = QHBoxLayout()
        label_cliente = QLabel("Nombre de cliente:")
        self.input_cliente = QLineEdit()
        self.input_cliente.setPlaceholderText("Ej. María Pérez")
        layout_cliente.addWidget(label_cliente)
        layout_cliente.addWidget(self.input_cliente)
        layout_principal.addLayout(layout_cliente)

        # --- Sección: Opciones de Pedido (QCheckBox) ---
        grupo_opciones = QGroupBox("Opciones del Menú")
        layout_opciones = QVBoxLayout()

        # Generamos las cajas de selección dinámicamente leyendo el diccionario fijos
        for item, precio in self.menu_items.items():
            cb = QCheckBox(f"{item} (${precio:.2f})")
            cb.setProperty("nombre_item", item)   # Guardamos el nombre internamente en el widget
            cb.setProperty("precio_item", precio) # Guardamos el costo internamente
            self.checkboxes.append(cb)
            layout_opciones.addWidget(cb)

        grupo_opciones.setLayout(layout_opciones)
        layout_principal.addWidget(grupo_opciones)

        # --- Botón de Registro ---
        self.btn_agregar = QPushButton("Registrar Pedido")
        self.btn_agregar.clicked.connect(self.agregar_pedido)
        self.btn_agregar.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;")
        layout_principal.addWidget(self.btn_agregar)

        # --- Sección: Lista de Costos y Opciones (QTreeWidget) ---
        self.arbol_pedidos = QTreeWidget()
        self.arbol_pedidos.setHeaderLabels(["Cliente / Opciones", "Costo ($)"])
        self.arbol_pedidos.setColumnWidth(0, 250)
        layout_principal.addWidget(self.arbol_pedidos)

        self.setLayout(layout_principal)

    def agregar_pedido(self):
        nombre_cliente = self.input_cliente.text().strip()

        # Validaciones básicas
        if not nombre_cliente:
            QMessageBox.warning(self, "Faltan datos", "Por favor, escribe el nombre del cliente o clienta.")
            return

        items_seleccionados = []
        costo_total = 0.0

        # Revisamos qué checkboxes fueron marcados por el usuario
        for cb in self.checkboxes:
            if cb.isChecked():
                nombre = cb.property("nombre_item")
                precio = cb.property("precio_item")
                items_seleccionados.append((nombre, precio))
                costo_total += precio

        if not items_seleccionados:
            QMessageBox.warning(self, "Menú vacío", "Debes seleccionar al menos una opción del menú.")
            return

        # 2. Agregar al QTreeWidget (Lista desplegable)
        # Elemento padre (El cliente y su costo total)
        item_cliente = QTreeWidgetItem(self.arbol_pedidos)
        item_cliente.setText(0, f"👤 {nombre_cliente}")
        item_cliente.setText(1, f"${costo_total:.2f}")
        
        # Le damos un color diferente para resaltarlo visualmente
        fuente_negrita = item_cliente.font(0)
        fuente_negrita.setBold(True)
        item_cliente.setFont(0, fuente_negrita)
        item_cliente.setFont(1, fuente_negrita)

        # Elementos hijos (Las opciones que pidió ese cliente específico)
        for nombre, precio in items_seleccionados:
            item_producto = QTreeWidgetItem(item_cliente)
            item_producto.setText(0, f"   ↳ {nombre}")
            item_producto.setText(1, f"${precio:.2f}")

        # Expandimos la rama para que se vean las opciones al instante
        item_cliente.setExpanded(True)

        # 3. Limpiar la interfaz para el siguiente pedido
        self.input_cliente.clear()
        for cb in self.checkboxes:
            cb.setChecked(False)
        
        self.input_cliente.setFocus() # Devolvemos el cursor a la barra de texto

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SistemaPedidosApp()
    ventana.show()
    sys.exit(app.exec_())