from django.core.management.base import BaseCommand
from movie.models import Movie
import numpy as np
import json

class Command(BaseCommand):
    help = 'Visualize the embedding of each movie in the database'

    def handle(self, *args, **kwargs):
        # Construct the full path to the JSON file
        #Recuerde que la consola está ubicada en la carpeta DjangoProjectBase.
        #El path del archivo movie_descriptions con respecto a DjangoProjectBase sería la carpeta anterior
        json_file_path = 'movie/management/commands/movies.json' 
        
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            movies = json.load(file)
        
        for movie in Movie.objects.all():
            embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
            print(movie.title, embedding_vector[:5])  # Muestra los primeros valores