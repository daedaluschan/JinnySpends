from datetime import date

class expense():

    def __init__(self):
        current_date = date.today()
        self.expense_date = current_date


    @property
    def expense_date(self):
        return self._expense_date

    @expense_date.setter
    def expense_date(self, value):
        self._expense_date = value
