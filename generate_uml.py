import os
import ast

def obtener_clases_desde_archivo(ruta_archivo):
    clases = []
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        nodo = ast.parse(f.read())
        for elem in nodo.body:
            if isinstance(elem, ast.ClassDef):
                clases.append(elem.name)
    return clases

def generar_puml_para_directorios(directorios, archivo_salida="estructura.puml"):
    contenido = ["@startuml", "skinparam classAttributeIconSize 0"]

    for directorio in directorios:
        for carpeta_raiz, subcarpetas, archivos in os.walk(directorio):
            paquete = carpeta_raiz.replace(os.sep, ".")
            contenido.append(f'package "{paquete}" {{')
            for archivo in archivos:
                if archivo.endswith(".py"):
                    ruta_archivo = os.path.join(carpeta_raiz, archivo)
                    clases = obtener_clases_desde_archivo(ruta_archivo)
                    modulo = archivo[:-3]  # Quitar .py
                    if clases:
                        contenido.append(f'class {modulo} {{')
                        for clase in clases:
                            contenido.append(f'  +{clase}')
                        contenido.append('}')
            contenido.append('}')

    contenido.append("@enduml")

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write("\n".join(contenido))

    print(f"Archivo {archivo_salida} generado.")

if __name__ == "__main__":
    carpetas = [
        "./app/core",
        "./app/forms",
        "./app/models",
        "./app/services",
        "./app/utils",
        "./app/views",
    ]
    generar_puml_para_directorios(carpetas)