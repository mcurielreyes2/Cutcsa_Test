import pdfplumber

# Ruta al archivo PDF
pdf_path = "K9W.pdf"  # Cambia esta ruta por la del PDF que quieres procesar

# Variable para almacenar todo el contenido
all_content = ""

# Abrimos el PDF y procesamos cada página
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        # Extraer texto de la página
        page_text = page.extract_text()
        if page_text:
            all_content += f"\n--- Texto de la Página {page_num} ---\n{page_text}\n"

        # Extraer tablas de la página
        tables = page.extract_tables()
        if tables:
            for table_num, table in enumerate(tables, start=1):
                all_content += f"\n--- Tabla {table_num} de la Página {page_num} ---\n"
                for row in table:
                    row_text = " | ".join(
                        cell if cell else "" for cell in row)  # Unir celdas de cada fila con un separador
                    all_content += row_text + "\n"

# Guardar el contenido en un archivo de texto
with open("contenido_pdf_con_tablas.txt", "w", encoding="utf-8") as file:
    file.write(all_content)

print("Extracción completada. Revisa el archivo 'contenido_pdf_con_tablas.txt'.")
