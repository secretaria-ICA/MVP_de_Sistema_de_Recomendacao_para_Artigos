from Recs_class import Recommender


class RecSys:

    def run():

        # instancia recommender
        rec = Recommender()

        print('Carregando arquivos...')
        rec.load_from_bd('ibm_articles.db')

        print('treinando o modelo...')
        kNN = rec.fit(metric='cosine')

        print('Gerando as recomendações...')
        recs = rec.make_recs(kNN)

        print('Salvando recomendações no Json...')
        rec.save_recs(recs)

        print('Concluído.')


if __name__ == '__main__':
    RecSys.run()
