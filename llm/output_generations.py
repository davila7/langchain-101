from dotenv import load_dotenv
from langchain import OpenAI
import os

# cargamos openai api key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# cargamos el modelo text-ada-001 con dos respuesta y que seleccione 1
llm = OpenAI(model_name="text-ada-001", n=2, best_of=2)
#print(llm("cómo estás?"))

# muestra la cantidad de tokens
print(llm.get_num_tokens("cómo estás?"))

# creamos una lista de resultados, incluso podemos multiplicar la lista en el mismo parámetro
llm_result = llm.generate(["Dime un chiste", "Dime un poema"]*5)

# cantidad de resultados
print(len(llm_result.generations))

# muestra los resultados
print(llm_result.generations)

# muestra la información que envía el proveedor
print(llm_result.llm_output)