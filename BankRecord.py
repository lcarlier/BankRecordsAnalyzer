
class BankRecord:
    def __init__(self, bankName, seqNr, accountNumber, date, amount, comment):
        self.accountNumber = accountNumber
        self.seqNr = seqNr
        self.date = date
        self.amount = amount
        self.comment = comment

    def __eq__(self, other):
        return self.seqNr == other.seqNr    and \
               self.date == other.date      and \
               self.amount == other.amount  and \
               self.comment == other.comment

    def __lt__(self, other):
        if self.date == other.date:
            return self.seqNr < other.seqNr
        else:
            return self.date < other.date

    def getIdxData(self, idx):
        if idx == 0:
            return self.accountNumber
        elif idx == 1:
            return self.date.strftime("%d/%m/%y")
        elif idx == 2:
            return self.comment
        elif idx == 3:
            return self.amount
        else:
            return "wrong index: %s"%(idx)

    @staticmethod
    def getIdxHeaderData(idx):
        if idx == 0:
            return "Account Number"
        elif idx == 1:
            return "Date"
        elif idx == 2:
            return "Comment"
        elif idx == 3:
            return "Amount"
        else:
            return "wrong index: %s"%(idx)

    @staticmethod
    def getMaxIdx():
        return 4

    def __str__(self):
        return "'%s' '%s' '%s'"%(self.date, self.comment, self.amount)

    def __repr__(self):
        return self.__str__()