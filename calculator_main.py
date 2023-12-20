import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### GridLayout 선언
        layout_number = QGridLayout()
        layout_operation = QHBoxLayout()
        layout_additional_operation = QFormLayout()

        ## 위젯 생성 ##

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel("Equation: ")
        label_solution = QLabel("Solution: ")
        self.equation = QLineEdit("")
        self.solution = QLineEdit("")

        ### layout_operation 서브 위젯 생성
        button_backspace = QPushButton("Backspace")
        button_division = QPushButton("/")
        button_multiple = QPushButton("x")
        button_minus = QPushButton("-")
        button_plus = QPushButton("+")
        button_equal = QPushButton("=")

        ### layout_additional_operation 서브 위젯 생성
        button_clear = QPushButton("Clear")

        ### layout_additional_operation 위젯 추가
        layout_additional_operation.addRow(label_equation, self.equation)
        layout_additional_operation.addRow(label_solution, self.solution)

        ## 위젯 추가 ##

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_backspace)
        layout_operation.addWidget(button_division)
        layout_operation.addWidget(button_multiple)
        layout_operation.addWidget(button_minus)
        layout_operation.addWidget(button_plus)
        layout_operation.addWidget(button_equal)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_additional_operation)
        main_layout.addLayout(layout_operation)

        # main_layout.addLayout(layout_clear_equal)
        main_layout.addLayout(layout_number)

        ## 시그널 설정 ##

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_multiple.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                layout_number.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 3, 0)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################

    def number_button_clicked(self, num):
        equation = self.equation.text()
        equation += str(num)
        self.equation.setText(equation)

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.solution.setText(str(solution))

    def button_clear_clicked(self):
        self.equation.setText("")
        self.solution.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())