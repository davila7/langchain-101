from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler                                  
llm = Ollama(base_url="http://localhost:11434", 
             model="llama2", 
             callback_manager = CallbackManager([StreamingStdOutCallbackHandler()]))


llm("You enter a room with 100 assassins and kill one of them. How many assassins are left?")

