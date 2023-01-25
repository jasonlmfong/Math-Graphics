import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget, QLineEdit, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
#from sympy import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Generator")

        # Create a central widget for the window and set it as the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a Matplotlib figure
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)
        self.is3D = False

        # Create a canvas to display the figure
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        # Create toolbar, passing canvas as first parament, parent (the MainWindow) as second.
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        # Create a text input box for equations
        self.equation_input = QLineEdit(self)
        self.equation_input.setPlaceholderText("Enter the equation")

        # Create a button for plotting
        self.plot_button = QPushButton("Generate Graph", self)
        self.plot_button.clicked.connect(self.generate_graph)
        

        # Create a button for switching between 2D and 3D mode
        self.mode_button = QPushButton("Switch to 3D", self)
        self.mode_button.clicked.connect(self.switch_mode)

        # Add the widgets to the layout
        layout.addWidget(self.mode_button)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.equation_input)
        layout.addWidget(self.plot_button)

        # Show the window
        self.show()

    def generate_graph(self):
        try:
            # Parse the equation entered
            # TODO: add sympy to parse more complex equations
            equation = self.equation_input.text()
            x = np.linspace(-10, 10, 100)
            self.ax.clear()
            # Run this section if in 3D mode
            if self.is3D:
                # TODO: generate empty plot
                if not equation:
                    self.ax.plot_surface()
                else:
                    y = np.linspace(-10, 10, 100)
                    X, Y = np.meshgrid(x, y)
                    Z = np.vectorize(lambda x, y: eval(equation))(X, Y)
                    self.ax.plot_surface(X, Y, Z)
            # Run this section if in 2D mode
            else:
                # TODO: generate empty plot
                if not equation:
                    self.ax.plot()
                else: 
                    y = eval(equation)
                    self.ax.plot(x, y)
            self.canvas.draw()
        except:
            # Show error message if there's any problem with the equation
            self.equation_input.setText("Invalid equation")
    
    def switch_mode(self):
        if self.is3D:
            self.is3D = False
            self.mode_button.setText("Switch to 3D")
            self.ax = self.figure.add_subplot(111)
        else:
            self.is3D = True
            self.mode_button.setText("Switch to 2D")
            self.ax = self.figure.add_subplot(111, projection='3d')
        self.generate_graph()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
