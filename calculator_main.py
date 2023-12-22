import sys
from PyQt5.QtWidgets import *
import math

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.temp_equation = ""

    def init_ui(self):
        main_layout = QGridLayout()

        ### GridLayout 선언
        layout_results = QGridLayout()
        layout_number = QGridLayout()
        layout_operation = QGridLayout()
        layout_additional_operation = QGridLayout()

        ## 위젯 생성 ##

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        self.results = QLineEdit("")
        self.results.setReadOnly(True)

        ### layout_operation 서브 위젯 생성
        button_backspace = QPushButton("Backspace")
        button_division = QPushButton("/")
        button_multiple = QPushButton("x")
        button_minus = QPushButton("-")
        button_plus = QPushButton("+")
        button_equal = QPushButton("=")

        ### layout_additional_operation 서브 위젯 생성
        button_percent = QPushButton("%")
        button_CE = QPushButton("CE")
        button_C = QPushButton("C")
        button_reverse = QPushButton("1/x")
        button_square = QPushButton("x^2")
        button_root = QPushButton("√x")

        ## 위젯 추가 ##

        ### layout_additional_operation 위젯 추가
        layout_results.addWidget(self.results)

        ### layout_additional_operation 위젯 추가
        layout_additional_operation.addWidget(button_percent, 0, 0)
        layout_additional_operation.addWidget(button_CE, 0, 1)
        layout_additional_operation.addWidget(button_C, 0, 2)
        layout_additional_operation.addWidget(button_reverse, 1, 0)
        layout_additional_operation.addWidget(button_square, 1, 1)
        layout_additional_operation.addWidget(button_root, 1, 2)

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_backspace, 1, 0)
        layout_operation.addWidget(button_division, 2, 0)
        layout_operation.addWidget(button_multiple, 3, 0)
        layout_operation.addWidget(button_minus, 4, 0)
        layout_operation.addWidget(button_plus, 5, 0)
        layout_operation.addWidget(button_equal, 6, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_results, 0, 0, 1, 4)
        main_layout.addLayout(layout_additional_operation, 1, 0, 2, 3)
        main_layout.addLayout(layout_number, 3, 0, 4, 3)
        main_layout.addLayout(layout_operation, 1, 3, 6, 1)

        ## 시그널 설정 ##

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_multiple.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        button_percent.clicked.connect(self.button_percent_clicked)
        button_CE.clicked.connect(self.button_clear_entry_clicked)
        button_C.clicked.connect(self.button_clear_clicked)
        button_reverse.clicked.connect(self.button_reverse_clicked)
        button_square.clicked.connect(self.button_square_clicked)
        button_root.clicked.connect(self.button_root_clicked)


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
                layout_number.addWidget(number_button_dict[number], 2 - x, y)
            elif number==0:
                layout_number.addWidget(number_button_dict[number], 3, 1)

        ### 소숫점 버튼과 +/- 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_change_sign = QPushButton("+/-")
        button_change_sign.clicked.connect(lambda state: self.button_change_sign_clicked())
        layout_number.addWidget(button_change_sign, 3, 0)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################

    def number_button_clicked(self, num):
        self.temp_equation += str(num)
        equation = self.results.text()
        equation += str(num)
        self.results.setText(equation)

    def button_change_sign_clicked(self):
        last_number = ""
        for char in reversed(self.temp_equation):
            if char.isdigit() or char == '.' or (char == '-' and last_number):
                last_number = char + last_number
            else:
                break

        if last_number:
            if last_number.startswith("-"):
                changed_number = last_number[1:]
            else:
                changed_number = "-" + last_number

            self.temp_equation = self.temp_equation[::-1].replace(last_number[::-1], changed_number[::-1], 1)[::-1]
            self.results.setText(changed_number)

    def button_operation_clicked(self, operation):
        self.temp_equation += operation
        self.results.setText("")

    def button_backspace_clicked(self):
        equation = self.results.text()
        equation = equation[:-1]

        # self.temp_equation의 마지막 문자가 숫자일 경우에만 제거(연산자일 경우 삭제하지 않음.)
        if self.temp_equation and self.temp_equation[-1].isdigit():
            self.temp_equation = self.temp_equation[:-1]

        self.results.setText(equation)

    def button_equal_clicked(self):
        equation = self.temp_equation
        solution = eval(equation)
        self.results.setText(str(solution))
        self.temp_equation = str(solution)

    def button_clear_clicked(self):
        self.results.setText("")
        self.temp_equation = ""

    def button_clear_entry_clicked(self):
        current_display = self.results.text()  # 현재 디스플레이에 표시된 숫자를 가져옵니다.

        # self.temp_equation에서 현재 디스플레이에 표시된 숫자를 찾아 제거합니다.
        if self.temp_equation.endswith(current_display):
            self.temp_equation = self.temp_equation[:-len(current_display)]

        self.results.setText("")  # 현재 디스플레이를 지웁니다.

    def button_percent_clicked(self):
        equation = float(self.results.text())
        equation = equation * 0.01
        self.results.setText(str(equation))

    def button_reverse_clicked(self):
        equation = float(self.results.text())

        if math.isfinite(1 / equation):
            self.results.setText(str(1/equation))
        else:
            self.results.setText("0으로 나눌 수 없습니다.")
            return None

    def button_square_clicked(self):
        equation = eval(self.results.text())
        equation = equation * equation
        self.results.setText(str(equation))

    def button_root_clicked(self):
        equation = self.results.text()
        try:
            equation = math.sqrt(eval(equation))
            self.results.setText(str(equation))
        except ValueError:
            self.results.setText("루트안에 음수가 들어갈 수 없습니다.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
