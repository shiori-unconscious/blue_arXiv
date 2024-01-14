# BlueArXiv ArXiv论文推荐平台
## 项目部署
1. 安装依赖
```
pip install -r requirements.txt
```
2. 下载数据集
```
https://www.kaggle.com/datasets/Cornell-University/arxiv
```
3. 建立数据库
```
cd blue_arxiv
./bat.sh
```
4. 导入数据
```
python manage.py loadjson <path-to-jsonfile>
```
5. 运行
```
python manage.py runserver
```