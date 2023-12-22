ef button_backspace_clicked(self):
        equation = self.results.text()  # 수정: text() 함수 호출
        equation = equation[:-1]

        # self.temp_equation의 마지막 문자가 숫자일 경우에만 제거
        if self.temp_equation and self.temp_equation[-1].isdigit():
            self.temp_equation = self.temp_equation[:-1]

        self.results.se