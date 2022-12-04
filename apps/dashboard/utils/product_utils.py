from dashboard.models import ProductPackaging, ProductNonPackaging


class LabelProduct:
    def __init__(self, user):
        self.packaging = ProductPackaging.objects.filter(user=user)
        self.non_packaging = ProductNonPackaging.objects.filter(user=user)

    def get_packaging(self):
        return self.packaging

    def get_non_packaging(self):
        return self.non_packaging

    def get_all_products(self):
        return self.get_packaging().union(self.get_non_packaging())

    def get_label(self, products):
        safety = products.filter(label='S')
        warnings = products.filter(label='W')
        danger = products.filter(label='D')
        return safety, warnings, danger

    def get_label_packaging(self):
        return self.get_label(self.get_packaging())

    def get_label_non_packaging(self):
        return self.get_label(self.get_non_packaging())

    def count_label(self, products):
        safety, warning, danger = self.get_label(products)
        return safety.count(), warning.count(), danger.count()

    def count_label_packaging(self):
        return self.count_label(self.get_packaging())

    def count_label_non_packaging(self):
        return self.count_label(self.get_non_packaging())

    def get_lastest_products(self):
        return self.get_all_products().order_by('-date_added')[:10]


if __name__ == '__main__':
    label = LabelProduct()
    print(label.get_label_packaging())
    print(label.get_label_non_packaging())
    print(label.count_label_packaging())
    print(label.count_label_non_packaging())

