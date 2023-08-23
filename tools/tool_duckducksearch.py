from dotenv import load_dotenv
from langchain.tools import DuckDuckGoSearchRun

# cargamos openai api key
load_dotenv()

# tools
search = DuckDuckGoSearchRun()

print(search.run("Quién fue el primer presidente de Chile?"))

'''
El 8 de julio de 1826 el Congreso instituyó el título de Presidente de la República y designó en esas funciones a Manuel Blanco Encalada, quien asumió al día siguiente. Tras la renuncia de Ramón Freire gobernó Chile por dos meses. Haz click aquí para más información de Manuel Blanco Encalada. Escuchar. El 8 de julio de 1826 el ... El presidente de la República de Chile es el jefe de Estado y de Gobierno del país, por ende, titular del poder ejecutivo.Como máxima autoridad política de la nación, designa o remueve a los comandantes en jefe de las Fuerzas Armadas. [n 5] El actual mandatario es Gabriel Boric Font, quien asumió el cargo el 11 de marzo de 2022, dando inicio así a su gestión. Mateo de Toro y Zambrano (1727-1811) 18 September 1810 26 February 1811 † President of the First Government Junta. Died in office. — Juan Martínez de Rozas ... Royal Governor of Chile. Chilean victory in the Battle of Chacabuco, Spanish control ends. Patria Nueva (1817-1826) Supreme directors (1817-1826) No. Portrait Name (Birth ... The timeline shows changes, both personal or title, of the head of state and the head of government of the Republic of Chile from 18 September 1810 until today, regardless of whether president, vice-president, supreme director, interim or junta. 19th century. Adams fue el primer presidente en vivir en la Casa Blanca, al mudarse allí el 1 de noviembre de 1800, mientras esta aún estaba en construcción. Thomas Jefferson (1801-1809)
'''