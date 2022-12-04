from datetime import date

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from dashboard.utils.send_notification import ScheduledMail

products = None
class Command(BaseCommand):
    help = 'Kirim email pemberitahuan produk yang akan kadaluarsa hari ini ke semua user'

    def add_arguments(self, parser):
        parser.add_argument('warning', type=str, help='Kirim email pemberitahuan produk yang akan kadaluarsa hari ini ke semua user')

    def handle(self, *args, **options):

        global products
        users = get_user_model().objects.all()
        for user in users:
            mail = ScheduledMail(user)
            label_products = options['warning']
            if label_products == 'warning':
                products = mail.get_warning_products()
            else:
                products = mail.get_expiring_products()
            for product in products:
                mail.send_scheduled_mail(product)

        self.stdout.write(self.style.SUCCESS('Successfully sent email'))
        # today_mail = ScheduledMail.get_today_mail()
        # for mail_message in today_mail:
        # 	mail_message.send_scheduled_mail()
