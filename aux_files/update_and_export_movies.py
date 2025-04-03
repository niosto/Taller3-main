
import os
import csv
from openai import OpenAI
from django.core.management.base import BaseCommand
from movie.models import Movie
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Update movie descriptions using OpenAI API and export to CSV"

    def handle(self, *args, **kwargs):
        # ✅ Load environment variables
        load_dotenv('../openAI.env')

        # ✅ Initialize OpenAI client
        client = OpenAI(
            api_key=os.environ.get('openai_apikey'),
        )

        # ✅ Helper function to get completion
        def get_completion(prompt, model="gpt-3.5-turbo"):
            messages = [{"role": "user", "content": prompt}]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
            )
            return response.choices[0].message.content.strip()

        # ✅ Instruction for the AI
        instruction = (
            "Vas a actuar como un aficionado del cine que sabe describir de forma clara, "
            "concisa y precisa cualquier película en menos de 200 palabras. La descripción "
            "debe incluir el género de la película y cualquier información adicional que sirva "
            "para crear un sistema de recomendación."
        )

        # ✅ Fetch all movies
        movies = Movie.objects.all()
        self.stdout.write(f"Found {movies.count()} movies")

        # ✅ Prepare CSV file
        output_file = 'updated_movie_descriptions.csv'
        with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Updated Description'])  # Header

            # ✅ Process each movie and write to CSV
            for movie in movies:
                self.stdout.write(f"Processing: {movie.title}")
                try:
                    prompt = (
                        f"{instruction} "
                        f"Vas a actualizar la descripción '{movie.description}' de la película '{movie.title}'."
                    )
                    updated_description = get_completion(prompt)

                    # ✅ Write title and updated description to CSV
                    writer.writerow([movie.title, updated_description])

                    self.stdout.write(self.style.SUCCESS(f"Updated and saved: {movie.title}"))

                except Exception as e:
                    self.stderr.write(f"Failed for {movie.title}: {str(e)}")

        self.stdout.write(self.style.SUCCESS(f"All movie descriptions updated and saved to {output_file}"))
