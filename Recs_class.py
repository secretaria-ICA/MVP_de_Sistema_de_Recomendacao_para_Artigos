import pandas as pd
import numpy as np
import pickle
import json
from sqlalchemy import create_engine
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import psycopg2 as ps
import recommender_functions as rf


class Recommender():
    '''
    Esse sistema de recomendação sugere artigos baseado em similaridades, através do KNN são encontrados os mais
    similares e eles são aramazenados. Dado um artigo escolhido, retorna-se os similares - esse processo é feito
    para todos os artigos da base, e os similares armazenados em um json.
    '''


    def __init__(self):
        '''
        Não temos nenhum atributo necessário para criar a classe.
        '''


    def load_from_bd(self, database_filepath):
        """
        Carrega a base de dados do banco de dados SQLite

        INPUT:
        :param database_filepath: Caminho para o SQLite database

        OUTPUT:
        :return df: Dataframe com interação usuário-conteúdo
        :return df_content: Dataframe com informações dos conteúdos
        """
        table = 'user_interaction'
        table2 = 'content'
        engine = create_engine('sqlite:///{}'.format(database_filepath))
        self.user_item = pd.read_sql(table, engine)
        self.articles = pd.read_sql(table2, engine)


    def load_from_csv(self, user_item_filepath, articles_filepath):
        """
        Carrega a base de dados dos arquivos csv passados

        INPUT:
        :param user_item_filepath: Caminho para o CSV user-item
        :param articles_filepath: Caminho para o CSV articles/content

        OUTPUT:
        :return df: Dataframe com interação usuário-conteúdo
        :return df_content: Dataframe com informações dos conteúdos
        """

        self.user_item = pd.read_csv(user_item_filepath)
        self.articles = pd.read_csv(articles_filepath)
        del self.user_item['Unnamed: 0']
        del self.articles['Unnamed: 0']


    def fit(self, k=15, metric='cosine'):
        '''
        Função que treina o modelo KNN utilizando a base de dados extraída do banco de dados.
        INPUT:
        :param k: número de similares a ser armazenado (int)
        :param metric: métrica utilizada para cálculo dos similares

        OUTPUT:
        :return: retorna o modelo KNN treinado com os mais similares
        '''

        # Insere coluna de frequencia e transforma a coluna 'articla_id' em float
        self.user_item['frequency'] = 1
        self.user_item['article_id'] = self.user_item['article_id'].astype(float)

        # Insere ID e retira email
        self.user_item = rf.map_id(self.user_item)

        # Armazena mais inputs
        self.num_recs = k
        self.metric_model = metric

        # Armazena valores uteis para serem usados no restante da função se necessário
        self.n_users = len(self.user_item['user_id'].unique())
        self.n_articles = len(self.user_item['article_id'].unique())
        self.n_user_item_iter = self.user_item.shape[0]

        self.X, self.user_mapper, self.artigo_mapper, self.user_inv_mapper, self.artigo_inv_mapper = rf.create_X(
            self.user_item)

        k += 1
        kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
        kNN.fit(self.X)

        return kNN


    def make_recs(self, kNN):
        '''
        Função que gera 15 recomendações/similares para cada artigo

        OUTPUT:
        :return: Dicionário com as recomendações geradas (dict)
        '''

        recs = {}

        artigo_mapper = self.artigo_mapper
        X = self.X
        artigo_inv_mapper = self.artigo_inv_mapper

        for id in self.user_item['article_id']:
            recs[id] = rf.find_similar_articles(id, artigo_mapper, X, artigo_inv_mapper, kNN, k=15, show_distance=False)

        return recs


    def save_recs(self, dict, name='recommendation.json'):
        '''
        Função que salva o dicionário gerado com as recomendações em um Json File

        INPUT:
        :param dict: dicionário que se deseja salvar no Json
        :param name: nome que o json salvo terá

        OUTPUT:
        :return json: json file com as recomendações de cada artigo salvas
        '''

        with open(name, 'w') as json_file:
            json.dump(dict, json_file)
