# MVP de Sistema de Recomendação para Artigos

#### Aluno: [Thiago Tadeu Dos Santos Gavioli](https://github.com/thiagogavioli)
#### Orientadora: [Manoela Kohler](https://github.com/manoelakohler).

---

Trabalho apresentado ao curso [BI MASTER](https://ica.puc-rio.ai/bi-master) como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão".


- [Jupyter notebook com a construção do trabalho](RecSys_notebook.ipynb) 
- [Classe que processa e gera as recomendações](Recs_class.py )
- [Funções utilizadas na Classe que gera as recomendações](recommender_functions.py)
- [Arquivo PY 'Main' que processa a classe que gera as recomandações - via banco de dados SQlite](main_bd.py)
- [Banco de dados SQlite com as tabelas que contém a descrição dos artigos e interação usuário-artigo](ibm_articles.db)
- [Arquivo .bat que inicia a classe, gera e salva em Json as recomendações - via banco de dados SQlite](run_bd.bat)
- [(Opcional) CSV com a descrição de cada artigo e demais informações](articles_community.csv)
- [(Opcional) CSV com a interação usuário-artigo](user-item-interactions.csv)
- [(Opcional) Arquivo PY 'Main' que processa a Classe que gera as recomendações - via arquivos CSV](main.py)
- [(Opcional) Arquivo .bat que inicia a classe, gera e salva em Json as recomendações - via arquivo csv](run_csv.bat)


### Resumo

O trabalho apresentado consiste em um MVP de um sistema de recomendação de artigos baseado em filtragem colaborativa, assim como seu deploy para que possa rodar
em .bat. 
Os dados são carregados de um banco de dados SQlite (também contém código opcional que carrega dos arquivos CSV), tratados e então modelados utilizando o 
algoritmo KNN (k-nearest neighbors). Dado um artigo escolhido, retorna-se os similares. Esse processo é feito para todos os artigos da base, e os similares 
armazenados e exportados em um json.

### Abstract

This work consists of a MVP (minimum viable product) recommendation system based on colaborative filtering, such as its deploy to run by a .bat file. 
The data is loaded from a SQlite database (there is also an optional version loading from CSV files), cleaned and pre-processed and then the modeling step
is done through KNN algorithm. For an article the algorithm returns the similars. This process is done for every articles in the database, and the similar are
saved to a Json file. 

---

Matrícula: 191.671.052

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós Graduação *Business Intelligence Master*
