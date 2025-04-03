import os
from django.core.management.base import BaseCommand
from django.conf import settings
from movie.models import Movie

class Command(BaseCommand):
    help = "Update movie images from the media folder"

    def handle(self, *args, **options):
        # Ruta de la carpeta donde se encuentran las imágenes
        images_folder = os.path.join(settings.MEDIA_ROOT, 'movie', 'images')
        
        # Verificamos que la carpeta exista
        if not os.path.exists(images_folder):
            self.stderr.write(self.style.ERROR(f"Image folder not found: {images_folder}"))
            return
        
        # Listamos todos los archivos en la carpeta
        available_images = os.listdir(images_folder)
        self.stdout.write(f"Found {len(available_images)} images in folder.")
        
        # Crear un diccionario para buscar imágenes más fácilmente
        image_lookup = {}
        for img in available_images:
            # Extraemos el nombre de la película del nombre del archivo
            # Formato esperado: m_NOMBRE.png
            if img.startswith('m_') and img.endswith('.png'):
                # No reemplazamos espacios, usamos el nombre tal como está
                image_lookup[img] = img
        
        # Contador de películas actualizadas
        updated_count = 0
        
        # Recorremos todas las películas en la base de datos
        movies = Movie.objects.all()
        self.stdout.write(f"Found {len(movies)} movies in database.")
        
        for movie in movies:
            # Probamos con diferentes formatos de nombre:
            # 1. Con espacios: m_Movie Title.png
            # 2. Con guiones bajos: m_Movie_Title.png
            possible_names = [
                f"m_{movie.title}.png",
                f"m_{movie.title.replace(' ', '_')}.png"
            ]
            
            found_image = None
            for name in possible_names:
                if name in image_lookup:
                    found_image = name
                    break
            
            if found_image:
                # Construimos la ruta relativa para almacenar en la base de datos
                relative_path = os.path.join('movie', 'images', found_image)
                
                # Actualizamos el campo de imagen de la película
                movie.image = relative_path
                movie.save()
                
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title} -> {found_image}"))
            else:
                self.stdout.write(self.style.WARNING(f"No matching image found for: {movie.title}"))
                
                # Buscar posibles alternativas para diagnóstico
                alternatives = [img for img in available_images if movie.title.lower() in img.lower()]
                if alternatives:
                    self.stdout.write(f"  Possible alternatives: {', '.join(alternatives[:3])}")
        
        # Mostramos un resumen al finalizar
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} of {len(movies)} movies with images."))