#!/usr/bin/env python

from mrjob.job import MRJob
from mrjob.step import MRStep
import json, os
import datetime as dt
from datetime import date

OS_DIR = os.path.abspath('./') + "/language/"

# ?) Se crea diccionario AFINN para asignar puntuaciones a las palabras
def create_dictionary(dir, scores=True):
    dic = {}
    f = open(dir, "r")
    for line in f:
        word, value = line.split('\t')
        if scores:
            dic[word] = float(value)
        else:
            dic[word] = str(value[:-1])
    return dic


class MRTweets(MRJob):

    # 2B) Verificar el origen del tweet. Si es de EEUU, entonces extrae el estado
    def get_state(self, tweet):
        place = tweet['place']
        if "United States" in place['country']:
            state = (place['full_name'].split(',')[-1]).strip()
            if state in self.states.keys():
                return state
        return None

    # 0) Definicion de pasos para MRJob
    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init(),
                   mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_sort)
        ]
    # 1) Inicialización de diccionarios (palabras y estados)
    def mapper_init(self):
        self.dic = create_dictionary(OS_DIR + "AFINN-111.txt")  # generacion de diccionario de palabras AFINN
        self.states = create_dictionary(OS_DIR + "states_codes.txt", scores=False) # generacion de diccionario con estados de EEUU

    # 2) Suma de las puntuaciones de las palabras de un tweet (si el tweet tiene origen en EEUU)
    def mapper(self, _, line):
        tweet = json.loads(line.strip())    # Que hace esta fucion al pasarle el metodo strip sin argumentos?
        try:
            state, text, sum_tweet = self.get_state(tweet), tweet['text'], 0    # Verificamos si el origen es un estado de EEUU
            if state:
                index_count = 0
                for word in text.lower().split(" "):   # leemos el tweet palabra por palabra y asignamos la puntuación que corresponda (si procede)
                    if word in self.dic:
                        sum_tweet += self.dic[word]
                        index_count += 1
                avg_tweet_score = sum_tweet/index_count # calculamos el score promedio de cada tweet
                yield (state, avg_tweet_score)
        except:
            pass

    # 3) Se ejecuta un reducer por estado que calcula la puntuacion media por estado
    def reducer(self, state, scores):
        sum_scores, n_tweets = 0, 0
        for score in scores:
            sum_scores += score
            n_tweets += 1
        puntuation = (sum_scores / n_tweets)
        #yield self.states[state], (round(puntuation, 2), n_tweets) # devuelve los promedios de puntuaciones por estado
        yield None, (round(puntuation, 2), (self.states[state], n_tweets))  # genera clave valor para que el siguiente reduce calcule el estado con mayor score


    # 4) Step2: reduce que ordena los estados por puntuaciones (de mayor a menor)
    def reducer_sort(self, _, score_state_pairs):
        for state in sorted(score_state_pairs, reverse=True):
            yield state

if __name__ == '__main__':

    tinit = dt.datetime.now().time()

    MRTweets.run()

    tend = dt.datetime.now().time()
    print("tinit: ", tinit, " tend: ", tend) # ". Execution time: ", exec_time)


