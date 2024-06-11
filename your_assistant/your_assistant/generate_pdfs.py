import pandas as pd
from fpdf import FPDF
import os

# Leer 20 filas empezando desde la fila 21
current_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_dir, 'dataclean.csv')
# Asegúrate de cambiar esto a la ruta correcta de tu archivo CSV
df = pd.read_csv(file_path, skiprows=range(1, 21), nrows=20)

# Crear una clase para el PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Anime Information', 0, 1, 'C')

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body.encode('latin1', 'ignore').decode('latin1'))
        self.ln()

    def add_anime_info(self, anime_info):
        self.chapter_body(anime_info)

# Función para dividir el dataframe en bloques de n filas
def divide_chunks(df, n):
    for i in range(0, len(df), n):
        yield df.iloc[i:i + n]

# Dividir el dataframe en bloques de datos (por ejemplo, 5 animes por bloque)
chunks = list(divide_chunks(df, 5))

# Crear un PDF por cada bloque de datos
for i, chunk in enumerate(chunks):
    pdf = PDF()
    pdf.add_page()

    for index, row in chunk.iterrows():
        anime_info = (
            f"Anime ID: {row['anime_id']}\n"
            f"Name: {row['Name']}\n"
            f"Rank: {row['Rank']}\n"
            f"Rating: {row['Rating']}\n"
            f"Synopsis: {row['Synopsis']}\n"
            f"Type: {row['Type']}\n"
            f"Genres: {row['Genres']}\n"
            f"Image URL: {row['Image URL']}\n"
            f"Producers: {row['Producers']}\n"
            f"Studios: {row['Studios']}\n"
            f"Episodes: {row['Episodes']}\n"
        )
        pdf.add_anime_info(anime_info)
    
    pdf.output(f'anime_info_{i + 1}.pdf')

print("PDFs creados exitosamente.")