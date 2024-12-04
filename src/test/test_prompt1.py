from ..promptsManager.prompt1 import Prompt1

prompt = Prompt1()

# comprencion de componentes:
# [["11"], ["1"], [["11"], ["11"], ["1111"]], [["111"]], [[["111"], ["111"], ["1"]]]]
# El array se compone de 5 arrays [a, b, c, d, e]
# El array a contiene un listado de que se debe imprimir en la primera linea. Mirar # Paso 1
# El array b es igual al array a. Mirar # Paso 2
# El array c, se compone de 3 arrays, esto por que la seccion "Analisisi por plataforma" tiene 3 subsecciones. Mirar # Paso 3
# Cada sub array de c, contiene un listado de que se debe imprimir en la sub-seccion "Analisisi por plataforma". Mirar # Paso 3 - Calculos
# El array d, es igual al array c, pero con una sola subseccion. Mirar # Paso 4
# El array e, fue pensado como posibles subsecciones de la seccion Formato de respuesta. Mirar # Paso 5
# Por esa razon, es array e contiene un array que a su vez contiene 3 arrays. Mirar # Paso 5
#
# Los subtitulos se imprimen cuando se detecta que se quiere imprimir una linea del componente.


# res = prompt.createPrompt([["11"], ["1"], [["11"], ["11"], ["1111"]], [["111"]], [[["111"], ["111"], ["1"]]]])

res = prompt.createPrompt([["01"], ["1"], [["10"], ["10"], ["1000"]], [["100"]], [[["110"], ["000"], ["1"]]]])

ruta = "src/test/response.txt"

# Crear y escribir en el archivo
with open(ruta, "w", encoding="utf-8") as archivo:
    archivo.write(res)

exit(0)
