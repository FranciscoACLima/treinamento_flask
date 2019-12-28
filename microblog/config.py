import os

chave_secreta = 'chave-super-secreta-voce-nunca-vai-adivinhar'


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or chave_secreta
