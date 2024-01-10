from datetime import datetime
import json
from mainpage.models import Paper, Journal, Category
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
import random


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        category = ["cs.HC","cs.AI","cs.CL"]
        obj = Category.objects.filter(name__in=category)
        self.stdout.write('{}'.format(obj))
        # self.stdout.write(self.style.SUCCESS("Updating many-to-many relationships..."))
        
        # for paper_id, category, journal in paper_stuff:
        #     try:
        #         paper = Paper.objects.get(arxiv_id=paper_id)
                
        #         journal_obj = Journal.objects.get(name=journal)
        #         paper.journal.add(journal_obj)
                
        #         category_obj = Category.objects.filter(name__in=category)
        #         paper.categories.add(*category_obj)
                
        #     except Paper.DoesNotExist:
        #         self.stdout.write(self.style.WARNING(f"Paper with arxiv_id={paper_id} does not exist. Skipping..."))
        #     except Exception as e:            
        #         self.stdout.write(self.style.ERROR(f"Error processing paper with arxiv_id={paper_id}: {e}"))
            
        # self.stdout.write(self.style.SUCCESS("Many-to-many relationships updated successfully."))