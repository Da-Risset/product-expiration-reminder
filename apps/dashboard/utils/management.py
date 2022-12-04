import datetime


def get_expiry_date():
    today = datetime.date.today()
    expiry_date = today + datetime.timedelta(days=365)
    return expiry_date


def label_expiry_date(expiry_date):
    today = datetime.date.today()
    delta = expiry_date - today
    if 7 >= delta.days > 0:
        return 'W'
    elif delta.days > 7:
        return 'S'
    else:
        return 'D'


class ExpiryDateManage:
    def __init__(self, name, quality):
        self.name = name
        self.quality = quality
        self.remaining = 0

    def apple(self):

        if self.quality == 'g':
            self.remaining = 30
        elif self.quality == 'b':
            self.remaining = 0
        elif self.quality == 'm':
            self.remaining = 7

        return self.remaining

    def banana(self):

        if self.quality == 'g':
            self.remaining = 3
        elif self.quality == 'b':
            self.remaining = 0
        elif self.quality == 'm':
            self.remaining = 1

        return self.remaining

    def guava(self):
        if self.quality == 'g':
            self.remaining = 3
        elif self.quality == 'b':
            self.remaining = 0
        elif self.quality == 'm':
            self.remaining = 1

        return self.remaining

    def lime(self):
        if self.quality == 'g':
            self.remaining = 30
        elif self.quality == 'b':
            self.remaining = 0
        elif self.quality == 'm':
            self.remaining = 7

        return self.remaining

    def orange(self):
        if self.quality == 'g':
            self.remaining = 30
        elif self.quality == 'b':
            self.remaining = 0
        elif self.quality == 'm':
            self.remaining = 7

        return self.remaining

    def pomegranate(self):
        if self.quality == 'g':
            self.remaining = 60
        elif self.quality == 'b':
            self.remaining = 0
        elif self.quality == 'm':
            self.remaining = 7

        return self.remaining

    def general(self):
        if self.quality == 'g':
            self.remaining = 7
        elif self.quality == 'b':
            self.remaining = 0
        elif self.quality == 'm':
            self.remaining = 1

        return self.remaining

    def get_expiry_date(self):
        today = datetime.date.today()

        if "apel" in self.name:
           self.remaining = self.apple()
        elif "pisang" in self.name:
           self.remaining = self.banana()
        elif "jambu" in self.name:
           self.remaining = self.guava()
        elif "nipis" in self.name:
           self.remaining = self.lime()
        elif "jeruk" in self.name:
           self.remaining = self.orange()
        elif "delima" in self.name:
           self.remaining = self.pomegranate()
        else:
            self.remaining = self.general()

        expiry_date = today + datetime.timedelta(days=self.remaining)
        return expiry_date

    def get_label(self):
        if self.quality == 'g':
            return 'S'
        elif self.quality == 'b':
            return 'D'
        elif self.quality == 'm':
            return 'W'

    def get_expiry_date_label(self):
        return self.get_label(), self.get_expiry_date()
