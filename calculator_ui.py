# built-in imports
import sys
from collections import OrderedDict
from functools import partial
from pathlib import Path

# third party imports
from PySide6 import QtCore, QtGui, QtWidgets
from sympy import sympify

# custom imports
from client import CalculatorClient


class CalculatorUI(QtWidgets.QMainWindow, CalculatorClient):
    WIN_WIDTH, WIN_HEIGHT = (200, 300)

    def __init__(
        self,
        window_title="Calculator",
        right_align=False,
        reverse_order=False,
        use_server=False,
        server_ip="0.0.0.0",
    ):
        """Class to build the UI for calculating arithmetic strings."""
        super(CalculatorUI, self).__init__(server_ip=server_ip)
        self.right_align = right_align
        self.reverse_order = reverse_order
        self.use_server = use_server
        self.input_string = ""
        self.button_list = []

        self.create_main_window(window_title)
        self.create_menu_bar()
        self.create_layout()
        self.create_connections()

        if self.use_server:
            success = self.connect_to_host()
            if not success:
                self.use_server = False
                print("Using built-in calculator")

    def closeEvent(self, event):
        if self.use_server:
            self.close_connection()
        super(CalculatorUI, self).closeEvent(event)

    # -----------------
    # UI Main Functions
    # -----------------

    def create_main_window(self, title):
        """Sets the main window's dimensions and title."""
        self.setWindowTitle(title)
        self.setMinimumSize(self.WIN_WIDTH, self.WIN_HEIGHT)
        self.main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(1)

    def create_menu_bar(self):
        """Creates the menu bar with layout and theme options."""
        menu_bar = self.menuBar()

        prefs_menu = menu_bar.addMenu("Preferences")
        self.create_menu_action("Right Align", "actn_prefs_alignment", prefs_menu)
        self.create_menu_action("Reverse Order", "actn_prefs_order", prefs_menu)
        self.actn_prefs_alignment.triggered.connect(self.alignment_action_clicked)
        self.actn_prefs_order.triggered.connect(self.order_action_clicked)

        self.theme_list = ["default", "minimal", "pastel", "twilight"]
        theme_menu = menu_bar.addMenu("Theme")
        theme_group = QtGui.QActionGroup(theme_menu)
        for theme in self.theme_list:
            action = self.create_menu_action(
                theme.capitalize(),
                f"actn_theme_{theme}",
                theme_menu,
                group=theme_group,
            )
            action.triggered.connect(partial(self.theme_action_clicked, theme))

    def create_layout(self):
        """
        Creates the main calculator layout.
        Contains the number pad, input, and output fields.
        """
        self.input_lineedit = QtWidgets.QLineEdit()
        self.input_lineedit.setAlignment(QtCore.Qt.AlignRight)
        regex = QtCore.QRegularExpression(
            "^([-+]? ?(\d+|\(\g<1>\))( ?[-+*\/] ?\g<1>)?)$"
        )
        validator = QtGui.QRegularExpressionValidator(regex)
        self.input_lineedit.setValidator(validator)
        self.main_layout.addWidget(self.input_lineedit)

        self.result_lineedit = QtWidgets.QLineEdit()
        self.result_lineedit.setAlignment(QtCore.Qt.AlignRight)
        self.result_lineedit.setReadOnly(True)
        font = self.result_lineedit.font()
        font.setPointSize(30)
        self.result_lineedit.setFont(font)
        self.result_lineedit.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.main_layout.addWidget(self.result_lineedit)

        numpad_layout = self.create_numpad_layout()
        self.main_layout.addLayout(numpad_layout)

    def create_numpad_layout(self):
        """
        Creates the calculator number pad and operator buttons.
        Handles layout modifications depending on alignment and numpad order.
        """
        layout = QtWidgets.QVBoxLayout()

        self.paren_row = QtWidgets.QHBoxLayout()
        self.zero_decimal_row = QtWidgets.QHBoxLayout()
        self.num_row_0 = QtWidgets.QHBoxLayout()
        self.num_row_1 = QtWidgets.QHBoxLayout()
        self.num_row_2 = QtWidgets.QHBoxLayout()

        rows = [
            self.paren_row,
            self.num_row_2,
            self.num_row_1,
            self.num_row_0,
            self.zero_decimal_row,
        ]
        if self.reverse_order:
            rows.reverse()
        for row in rows:
            layout.addLayout(row)

        if self.right_align:
            self.create_ops_buttons(rows)
        self.create_paren_row_buttons()
        self.create_zero_row_buttons()
        self.create_numpad_buttons()
        if not self.right_align:
            self.create_ops_buttons(rows)

        return layout

    def create_connections(self):
        """Creates connections between the buttons and actions."""

        # input
        self.input_lineedit.textChanged.connect(self.input_changed)
        self.input_lineedit.returnPressed.connect(self.eq_button_clicked)

        # numpad buttons
        self.btn_clear.clicked.connect(self.clear_button_clicked)
        for button in self.button_list:
            if button in [self.btn_ops_eq, self.btn_clear]:
                continue
            button.clicked.connect(partial(self.build_input_string, button.text()))
        self.btn_ops_eq.clicked.connect(self.eq_button_clicked)

    # -------------------
    # UI Helper Functions
    # -------------------

    def create_menu_action(
        self,
        text: str,
        var_name: str,
        menu: QtWidgets.QMenu,
        group: QtGui.QActionGroup = None,
        checkable: bool = True,
    ) -> QtGui.QAction:
        """
        Creates a menu action and adds it to the given menu tab and group.

        Args:
            text: text to display on menu action item
            var_name: class variable name to give action
            menu: menu on which to add action item
            group: group in which to add action item
            checkable: bool indicating whether action can be checked

        Returns:
        """
        action = QtGui.QAction(text, menu, checkable=checkable)
        setattr(self, var_name, action)
        menu.addAction(action)
        if group:
            group.addAction(action)
        return action

    def create_button(
        self, text: str, var_name: str, layout: QtWidgets.QLayout
    ) -> None:
        """
        Creates a button and associated variable within the class.

        Args:
            text: text to display on button
            var_name: class variable name to give button
            layout: layout on which to add button
        """
        button = QtWidgets.QPushButton(text)
        button.setMinimumSize(20, 20)
        setattr(self, var_name, button)
        layout.addWidget(button)
        self.button_list.append(button)

    def create_row_with_clear_button(
        self,
        button_info: list[tuple[str, str]],
        layout: QtWidgets.QLayout,
        reverse: bool,
    ) -> None:
        """
        Helper to create a row with the clear ("AC") button on the numpad.
        Handles placement of clear button based on alignment and numpad order.

        Args:
            button_info: list of buttons to create (name, display text)
            layout: layout on which to add button
            reverse: bool indicating whether numpad order is reversed
        """
        clear_button_info = ("clear", "AC")
        if reverse:
            if self.right_align:
                button_info.reverse()
                button_info.append(clear_button_info)
            else:
                button_info.insert(0, clear_button_info)
        buttons = OrderedDict(button_info)
        for key, val in buttons.items():
            self.create_button(val, f"btn_{key}", layout)

    def create_ops_buttons(self, rows: list[QtWidgets.QHBoxLayout]) -> None:
        """
        Helper to create the operation buttons row.

        Args:
            rows: list of numpad rows on which to append each ops button
        """
        ops_symbols = OrderedDict(
            {"div": "/", "mul": "*", "sub": "-", "add": "+", "eq": "="}
        )
        for i, (key, val) in enumerate(ops_symbols.items()):
            self.create_button(val, f"btn_ops_{key}", rows[i])

    def create_paren_row_buttons(self) -> None:
        """
        Creates the parentheses row.
        If numpad is not reversed, also creates the clear button.
        """
        button_info = [("lparen", "("), ("rparen", ")")]
        self.create_row_with_clear_button(
            button_info, self.paren_row, (not self.reverse_order)
        )

    def create_zero_row_buttons(self) -> None:
        """
        Creates the zero/decimal row.
        If numpad is reversed, also creates the clear button.
        """
        button_info = [("0", "0"), ("decimal", ".")]
        self.create_row_with_clear_button(
            button_info, self.zero_decimal_row, self.reverse_order
        )

    def create_numpad_buttons(self) -> None:
        """Creates the numpad digit buttons 1-9."""
        buttons_per_row = 3

        # create a button for each digit
        for i in range(9):
            numpad_row_name = f"num_row_{int(i/buttons_per_row)}"
            self.create_button(
                str(i + 1),  # offset zero-indexing in display text
                f"btn_num_{i}",
                getattr(self, numpad_row_name),
            )

    # -------------------------
    # Connection Main Functions
    # -------------------------

    def input_changed(self):
        """Updates input string based on keyboard input via line edit widget."""
        self.input_string = self.input_lineedit.text()

    def clear_button_clicked(self):
        """Clears the input string and UI."""
        self.clear_input_string()
        if self.result_lineedit.text():
            self.result_lineedit.clear()

    def eq_button_clicked(self):
        """Sends input string to be calculated."""
        if not self.input_string:
            return
        if self.use_server:
            result = self.send_to_server(self.input_string)
        else:
            result = str(float(sympify(self.input_string)))
        self.result_lineedit.setText(result)
        self.input_string = result

    def alignment_action_clicked(self) -> None:
        """Toggles the numpad alignment."""
        self.right_align = not self.right_align
        self.rebuild_widget()

    def order_action_clicked(self) -> None:
        """Toggles the numpad order."""
        self.reverse_order = not self.reverse_order
        self.rebuild_widget()

    def theme_action_clicked(self, theme_name) -> None:
        theme_action = getattr(self, f"actn_theme_{theme_name}")
        checked = theme_action.isChecked()
        qss_file = f"themes/{theme_name}.qss"
        if checked and Path(qss_file).exists():
            qss_file = f"themes/{theme_name}.qss"
            self.set_theme(qss_file)
        else:
            self.clear_theme()

    # ---------------------------
    # Connection Helper Functions
    # ---------------------------

    def build_input_string(self, x):
        """Builds the input string based on numpad input."""
        self.input_string += x
        self.input_lineedit.setText(self.input_string)

    def clear_input_string(self):
        """Clears the input string."""
        self.input_string = ""
        self.input_lineedit.clear()

    def clear_layout(self, layout: QtWidgets.QLayout) -> None:
        """Recursively clears all child layouts and widgets on the given layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())

        self.button_list = []

    def rebuild_widget(self):
        result = self.result_lineedit.text()
        self.clear_layout(self.main_layout)
        self.create_layout()
        self.create_connections()
        self.input_lineedit.setText(self.input_string)
        self.result_lineedit.setText(result)

    def set_theme(self, qss_file) -> None:
        """Sets the style sheet to the given qss file."""
        with open(qss_file, "r") as theme:
            self.setStyleSheet(theme.read())

    def clear_theme(self) -> None:
        """Clears the current style sheet."""
        self.setStyleSheet("")


if __name__ == "__main__":
    # ip = "10.8.9.174"
    ip = "172.18.0.2"
    app = QtWidgets.QApplication(sys.argv)
    calc = CalculatorUI(use_server=True, server_ip=ip)
    calc.show()
    sys.exit(app.exec())