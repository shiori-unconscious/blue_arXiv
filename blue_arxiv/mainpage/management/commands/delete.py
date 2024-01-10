from datetime import datetime
import json
from mainpage.models import Paper, Journal, Category
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import random


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        Journal.objects.all().delete()