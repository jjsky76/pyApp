import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
UIC = uic.loadUiType('gh_calc_new.ui')[0]


class GHCalc(QDialog, UIC):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.text = ''          # number(type:str) after hit button or calculated result
        self.formula = ''       # formula(type:str) for calculation
        self.res = 0            # result value(type:int or float) after calculation
        self.cur = 0            # current value(type:int or float) in text edit
        self.in_op = False      # operation(type:bool) whether in operation( +, -, *, /, = ) or not
        self.last_op = '='      # last operation mode(type:str) +, -, *, /, =

        self.pushButton_0.clicked.connect(lambda: self.btn_clicked('0'))
        self.pushButton_1.clicked.connect(lambda: self.btn_clicked('1'))
        self.pushButton_2.clicked.connect(lambda: self.btn_clicked('2'))
        self.pushButton_3.clicked.connect(lambda: self.btn_clicked('3'))
        self.pushButton_4.clicked.connect(lambda: self.btn_clicked('4'))
        self.pushButton_5.clicked.connect(lambda: self.btn_clicked('5'))
        self.pushButton_6.clicked.connect(lambda: self.btn_clicked('6'))
        self.pushButton_7.clicked.connect(lambda: self.btn_clicked('7'))
        self.pushButton_8.clicked.connect(lambda: self.btn_clicked('8'))
        self.pushButton_9.clicked.connect(lambda: self.btn_clicked('9'))
        self.pushButton_do.clicked.connect(lambda: self.btn_clicked('.'))
        self.pushButton_pl.clicked.connect(lambda: self.btn_clicked('+'))
        self.pushButton_mi.clicked.connect(lambda: self.btn_clicked('-'))
        self.pushButton_mu.clicked.connect(lambda: self.btn_clicked('*'))
        self.pushButton_di.clicked.connect(lambda: self.btn_clicked('/'))
        self.pushButton_ba.clicked.connect(lambda: self.btn_clicked('b'))
        self.pushButton_cl.clicked.connect(lambda: self.btn_clicked('c'))
        self.pushButton_eq.clicked.connect(lambda: self.btn_clicked('='))

    @staticmethod
    def do_calc(op, i, j):
        """
        do_calc         : do calculation for +, - , *, /, =
        op(str)         : '+', '-' , '*', '/', '='
        i(int or float) : previous result
        j(int or float) : current
        """
        if op == '+':
            return i + j
        elif op == '-':
            return i - j
        elif op == '*':
            return i * j
        elif op == '/':
            return i / j
        elif op == '=':
            return i

    def btn_clicked(self, btn):
        """
        btn_clicked : pushButton Event Handler
        btn(str)    : button ( '0' ~ 'c' )
        """
        if '0' <= btn <= '9':
            if self.in_op:
                if self.last_op == '=':
                    self.res = 0
                    self.cur = 0
                    self.formula = ''
                self.text = btn
                self.in_op = False
            else:
                self.text = self.text + btn

            # when starting '0', ignore '0'
            if '.' in self.text:
                self.text = str(float(self.text))
            else:
                self.text = str(int(self.text))
        elif btn == '.':
            if self.in_op:
                if self.last_op == '=':
                    self.res = 0
                    self.cur = 0
                    self.formula = ''
                self.text = '0.'
                self.in_op = False
            else:
                if '.' in self.text:
                    return
                self.text = self.text + btn
        elif btn == 'c':
            self.text = '0'
            self.res = 0
            self.cur = 0
            self.last_op = '='
            self.in_op = False
            self.formula = ''
        elif btn == 'b':
            if self.in_op:
                return

            if len(self.text) > 1:
                self.text = self.text[:-1]
            else:
                self.text = ''
        elif btn == '+' or btn == '-' or btn == '*' or btn == '/':
            if self.in_op and self.last_op != '=':
                self.last_op = btn
                self.formula = self.formula[:-2] + ' ' + btn
                self.lineEdit_fo.setText(self.formula)
                return

            if len(self.text) == 0:
                return

            if '.' in self.text:
                self.cur = float(self.text)
            else:
                self.cur = int(self.text)
            if self.res == 0:
                self.res = self.cur
            else:
                self.res = self.do_calc(self.last_op, self.res, self.cur)
            self.text = str(self.res)

            if self.last_op == '=':
                self.formula = str(self.res) + ' ' + btn
            else:
                self.formula = self.formula + ' ' + str(self.cur) + ' ' + btn
            self.in_op = True
            self.last_op = btn
        elif btn == '=':
            if self.in_op or len(self.text) == 0:
                return

            if '.' in self.text:
                self.cur = float(self.text)
            else:
                self.cur = int(self.text)
            self.res = self.do_calc(self.last_op, self.res, self.cur)
            self.text = str(self.res)
            self.formula = self.formula + ' ' + str(self.cur) + ' ' + btn
            self.in_op = True
            self.last_op = btn

        # Show result & formula
        self.lineEdit_re.setText(self.text)
        self.lineEdit_fo.setText(self.formula)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = GHCalc()
    dlg.show()
    sys.exit(app.exec_())
