from datetime import date

class expense():

    def __init__(self):
        current_date = date.today()
        self.expense_date = current_date
        self.expense_cat = ""
        self.expense_item = ""
        self.expense_amt = 0
        self.expense_reg = "Y"
        self.expense_remark = ""

    @property
    def expense_date(self):
        return self._expense_date

    @expense_date.setter
    def expense_date(self, value):
        self._expense_date = value

    @property
    def expense_cat(self):
        return  self._expense_cat

    @expense_cat.setter
    def expense_cat(self, value):
        self._expense_cat = value

    @property
    def expense_item(self):
        return self._expense_item

    @expense_item.setter
    def expense_item(self, value):
        self._expense_item = value

    @property
    def expense_amt(self):
        return self._expense_amt

    @expense_amt.setter
    def expense_amt(self, value):
        self._expense_amt = value

    @property
    def expense_reg(self):
        return self._expense_reg

    @expense_reg.setter
    def expense_reg(self, value):
        self._expense_reg = value

    @property
    def expense_remark(self):
        return self._expense_remark

    @expense_remark.setter
    def expense_remark(self, value):
        self._expense_remark = value

