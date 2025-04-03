import os
import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Compare two movies and optionally a prompt using OpenAI embeddings"

    def handle(self, *args, **kwargs):
        # ✅ Load OpenAI API key
        load_dotenv()
        client = OpenAI(api_key=os.environ.get('openai_api_key'))

        # ✅ Change these titles for any movies you want to compare
        movie1 = Movie.objects.get(title="Dante's Inferno")
        movie2 = Movie.objects.get(title="Dante's Inferno")

        def get_embedding(text):
            response = client.embeddings.create(
                input=[text],
                model="text-embedding-3-small"
            )
            return np.array(response.data[0].embedding, dtype=np.float32)

        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

        # ✅ Generate embeddings of both movies
        emb1 = get_embedding(movie1.description)
        emb2 = get_embedding(movie2.description)

        # ✅ Compute similarity between movies
        similarity = cosine_similarity(emb1, emb2)
        self.stdout.write(f"\U0001F3AC Similaridad entre '{movie1.title}' y '{movie2.title}': {similarity:.4f}")

        # ✅ Optional: Compare against a prompt
        prompt = "película de terror psicológico que sigue la historia de un joven escritor atormentado por visiones perturbadoras y pesadillas vívidas. Inspirado en la obra clásica de Dante Alighieri, el protagonista se sumerge en un viaje a través de los nueve círculos del infierno en un intento desesperado por salvar su alma de la condenación eterna. Con una atmósfera oscura y opresiva, la película combina elementos de horror sobrenatural con una narrativa introspectiva que explora los pecados y la redención. Para los amantes del cine de terror que buscan una experiencia inmersiva y perturbadora, ofrece una visión única del infierno y los tormentos internos del protagonista. Con actuaciones intensas y una dirección visualmente impactante, esta película es ideal para aquellos que disfrutan de historias profundas y perturbadoras que desafían los límites de la mente humana. Prepárate para adentrarte en un viaje aterrador a través de la mente del protagonista y descubrir los horrores que acechan en las sombras de su propia alma"
        prompt_emb = get_embedding(prompt)

        sim_prompt_movie1 = cosine_similarity(prompt_emb, emb1)
        sim_prompt_movie2 = cosine_similarity(prompt_emb, emb2)

        self.stdout.write(f"\U0001F4DD Similitud prompt vs '{movie1.title}': {sim_prompt_movie1:.4f}")
        self.stdout.write(f"\U0001F4DD Similitud prompt vs '{movie2.title}': {sim_prompt_movie2:.4f}")