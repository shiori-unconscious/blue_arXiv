import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.pipeline import Pipeline
import nltk
from .models import Paper

try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")


class Recommend:

    def __init__(self, user_model) -> None:
        data = {
            'id': [],
            'text': [],
            'label': []
        }
        self.exclude = []
        cnt1 = 0
        for like in user_model.liked_content.all():
            data['id'].append(like.arxiv_id)
            data['text'].append(like.abstract)
            self.exclude.append(like.arxiv_id)
            data['label'].append(0)
            cnt1 += 1
        
        cnt2 = 0
        for dislike in user_model.disliked_content.all():
            data['id'].append(dislike.arxiv_id)
            data['text'].append(dislike.abstract)
            self.exclude.append(dislike.arxiv_id)
            data['label'].append(1)
            cnt2 += 1
        if cnt1==0 or cnt2==0:
            self.inited = False
            return
        
        data = pd.DataFrame(data).set_index('id')
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words=stopwords.words('english'))),
            ('svm', SVC(kernel='linear'))
        ])
        try:
            self.pipeline.fit(data['text'], data['label'])
        except ValueError as err:
            print(err)
        self.inited = True
        
    def recommend(self):
        if not self.inited:
            papers = Paper.objects.exclude(arxiv_id__in=self.exclude).order_by('?')[:3]
        else:
            papers = Paper.objects.exclude(arxiv_id__in=self.exclude).order_by('?')[:1000]
            papers_texts = [paper.abstract for paper in papers]
            result = self.pipeline.predict(papers_texts)
            papers = [paper for (paper, res) in zip(papers, result) if res==0]
            print(len(papers))
            papers = papers[:3]
        return papers

    def add(self, paper, favi = False):
        self.exclude.append(paper.arxiv_id)
        if favi:
            self.data.loc[paper.arxiv_id] = [paper.abstract, 0]
        else:
            self.data.loc[paper.arxiv_id] = [paper.abstract, 1]

    def remove(self, arxiv_id):
        self.exclude = list(filter(lambda x: x!=arxiv_id, self.exclude))
        self.data.drop(arxiv_id, inplace=True)
