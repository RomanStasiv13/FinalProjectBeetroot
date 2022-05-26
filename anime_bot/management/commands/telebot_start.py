from django.core.management import BaseCommand
from telegram.telegrambot import bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot.infinity_polling()
