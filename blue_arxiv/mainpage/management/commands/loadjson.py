from datetime import datetime
import json
from mainpage.models import Paper, Journal, Category
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from tqdm import tqdm


class Command(BaseCommand):

    def check_cs(self, tags):
        if tags is None:
            return False
        
        for tag in tags:
            if tag.split('.')[0] == 'cs':
                return True
        return False
    
    def add_arguments(self, parser):
        # 添加名为 path 的命令行参数
        parser.add_argument('path', type=str, help='Path to the JSON file')
        
    def handle(self, *args, **options):
        path = options['path']
        paper_stuff = []
        papers = []
        self.stdout.write(self.style.SUCCESS("Processing JSON file and preparing data..."))
        with open(path, 'r', encoding='utf-8') as data:
            for line in tqdm(data):
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                else:
                    versions = entry.get('versions')
                    timestamp = None
                    if versions is not None and len(versions)>=1:
                        timestamp = versions[-1]['created']
                    category = entry.get('categories').split()
                    if self.check_cs(category):
                        paper_id=entry.get('id')
                        
                        papers.append(
                            Paper(
                                arxiv_id=paper_id,
                                authors=entry.get('authors'),
                                title=entry.get('title'),
                                doi=entry.get('doi'),
                                abstract=entry.get('abstract'),
                                upload_time=timezone.make_aware(datetime.strptime(timestamp if timestamp else "Fri, 23 Aug 1996 09:39:49 GMT", "%a, %d %b %Y %H:%M:%S %Z")),
                            )
                        )
                        
        self.stdout.write(self.style.SUCCESS("Finish Processing JSON file..."))
        # journals = [Journal(name=journal) for journal in journals if journal is not None]
        categories = [Category(name=category) for category in categories if category is not None]
        # 使用数据库事务提高插入效率
        with transaction.atomic():
            # 批量插入
            Paper.objects.bulk_create(papers)
            # Journal.objects.bulk_create(journals)
            Category.objects.bulk_create(categories)
        
        self.stdout.write(self.style.SUCCESS("Data insertion into database is successful."))
        self.stdout.write(self.style.SUCCESS("Updating many-to-many relationships..."))
        
        for paper_id, category in paper_stuff:
            try:
                paper = Paper.objects.get(arxiv_id=paper_id)
                
                # journal_obj = Journal.objects.get(name=journal)
                # paper.journal.add(journal_obj)
                
                category_obj = Category.objects.filter(name__in=category)
                paper.categories.add(*category_obj)
                
            except Paper.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Paper with arxiv_id={paper_id} does not exist. Skipping..."))
            except Exception as e:            
                self.stdout.write(self.style.ERROR(f"Error processing paper with arxiv_id={paper_id}: {e}"))
            
        self.stdout.write(self.style.SUCCESS("Many-to-many relationships updated successfully."))