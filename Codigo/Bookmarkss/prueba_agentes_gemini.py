import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

@tool
def calcular_longitud_texto(texto: str) -> int:
    """Cuenta la cantidad de caracteres que tiene un texto."""
    return len(texto)

tools = [calcular_longitud_texto]

# Configura tu API Key
os.environ["GOOGLE_API_KEY"] = ""

# Inicializar el modelo (Basado en el Transformer Encoder-Decoder [cite: 52])
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-3.1-pro-preview", 
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=30,
    timeout=None,
    max_retries=2,
    )

# Definir el prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil que usa herramientas."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Crear el agente
agent = create_tool_calling_agent(llm_gemini, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Ejecución
agent_executor.invoke({"input": "¿Cuántas letras tiene la palabra 'Transformer'?"})




