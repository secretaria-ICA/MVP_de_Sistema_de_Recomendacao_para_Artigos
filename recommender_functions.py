import pandas as pd
import numpy as np
import pickle
import json
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import sys # can use sys to take command line arguments


def email_mapper(df):
    '''
    Função que cria os ids de acordo com o email

    INPUT:
    :param df: dataframe

    OUTPUT:
    :return: email e correspondente id (list)
    '''

    coded_dict = dict()
    cter = 1
    email_encoded = []

    for val in df['email']:
        if val not in coded_dict:
            coded_dict[val] = cter
            cter += 1

        email_encoded.append(coded_dict[val])
    return email_encoded


def map_id(df):
    '''
    Função que mapeia o email de cada usuário a um novo ID  e deleta a coluna "email"

    INPUT:
    :param df: dataframe

    OUTPUT:
    :return: novo dataframe com a coluna de ID criada e coluna email deletada
    '''

    email_encoded = email_mapper(df)
    del df['email']
    df['user_id'] = email_encoded
    return df


def create_X(df):
    """
    Gera uma matriz esparsa utilizando o dataframe com o consumo por usuário.

    INPUT:
        :param: df: pandas dataframe

    OUTPUT:
        X: Matriz esparsa
        user_mapper: dict que mapeia usuário id ao índice do usuário
        user_inv_mapper: dict que mapeia o índice ao id do usuário
        artigo_mapper: dict que mapeia id do artigo ao índice do artigo
        artigo_inv_mapper: dict que mapeia o índice do artigo ao id do artigo
    """

    N = df['user_id'].nunique()
    M = df['article_id'].nunique()

    user_mapper = dict(zip(np.unique(df["user_id"]), list(range(N))))
    artigo_mapper = dict(zip(np.unique(df["article_id"]), list(range(M))))

    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["user_id"])))
    artigo_inv_mapper = dict(zip(list(range(M)), np.unique(df["article_id"])))

    user_index = [user_mapper[i] for i in df['user_id']]
    artigo_index = [artigo_mapper[i] for i in df['article_id']]

    X = csr_matrix((df["frequency"], (artigo_index, user_index)), shape=(M, N))

    return X, user_mapper, artigo_mapper, user_inv_mapper, artigo_inv_mapper


def find_similar_articles(article_id, artigo_mapper, X, artigo_inv_mapper, kNN, k=15, show_distance=False):
    """
    Encontra k-nearest neighbours para um dado article_id.

    INPUT:
        :param article_id: id do artigo de interesse
        :param X: user-item matriz
        :param k: número de artigos similares para devolver
        :param metric: métrica de distância para cálculo no KNN

    OUTPUT:
        lista de k artigos similares
    """
    neighbour_ids = []

    artigo_ind = artigo_mapper[article_id]
    artigo_vec = X[artigo_ind]
    k += 1

    neighbour = kNN.kneighbors(artigo_vec, return_distance=show_distance)
    for i in range(0, k):
        n = neighbour.item(i)
        neighbour_ids.append(artigo_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids