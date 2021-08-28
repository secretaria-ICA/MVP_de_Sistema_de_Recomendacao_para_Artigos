from Recs_class import Recommender
import click


@click.command()
@click.option("--data")
@click.option("--data2")
#class RecSys:

def run(data, data2):

    # instancia recommender
    rec = Recommender()

    print('Carregando arquivos...')
    rec.load_from_csv(data, data2)

    print('treinando o modelo...')
    kNN = rec.fit(metric='cosine')

    print('Gerando as recomendações...')
    recs = rec.make_recs(kNN)

    print('Salvando recomendações no Json...')
    rec.save_recs(recs)

    print('Concluído.')


if __name__ == '__main__':
    run()