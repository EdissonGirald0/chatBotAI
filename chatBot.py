# El formato de chat¶
# En este cuaderno, explorará cómo puede utilizar
# el formato de chat para tener conversaciones
# extendidas con chatbots personalizados o especializados
# para tareas o comportamientos específicos.

# Configuración
import panel as pn  # Importar panel como pn para la interfaz gráfica
import os
import openai
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())  # lee el archivo .env local

# establece la clave de la API de OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Función para obtener una respuesta completada a partir de un prompt


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.Completion.create(
        model=model,
        messages=messages,
        temperature=0.5,  # este es el grado de aleatoriedad de la salida del modelo
    )
    return response.choices[0].message['content']

# Función para obtener una respuesta completada a partir de una lista de mensajes


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.5):
    response = openai.Completion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # este es el grado de aleatoriedad de la salida del modelo
    )
    return response.choices[0].message['content']


# Ejemplo 1: Obtener una broma
messages = [
    {'role': 'system', 'content': 'Eres una asistente que habla como Shakespeare.'},
    {'role': 'user', 'content': 'tell me a joke'},
    {'role': 'assistant', 'content': 'Why did the chicken cross the road'},
    {'role': 'user', 'content': 'I don\'t know'}
]

response = get_completion_from_messages(messages, temperature=0.8)
print(response)

# Ejemplo 2: Recordar el nombre del usuario
messages = [
    {'role': 'system', 'content': 'You are friendly chatbot.'},
    {'role': 'user', 'content': 'Hi, my name is Isa'}
]

response = get_completion_from_messages(messages, temperature=0.8)
print(response)

# Ejemplo 3: Saludo inicial y recordar el nombre del usuario
messages = [
    {'role': 'system', 'content': 'You are friendly chatbot.'},
    {'role': 'user', 'content': 'Hi, my name is Isa'},
    {'role': 'assistant', 'content': "Hi Isa! It's nice to meet you. Is there anything I can help you with today?"},
    {'role': 'user', 'content': 'Yes, you can remind me, What is my name?'}
]

response = get_completion_from_messages(messages, temperature=0.8)
print(response)


# Lista para recopilar los paneles a mostrar
panels = []

# Lista para acumular los mensajes del chat
context = [
    {
        'role': 'system',
        'content': """
        You are OrderBot, an automated service to collect orders for a pharmacy. \
        You first greet the customer, then collect the order, \
        and then ask if it's for pickup or delivery. \
        You wait to collect the entire order, then summarize it and check for a final \
        time if the customer wants to add anything else. \
        If it's for delivery, you ask for an address. \
        Finally, you collect the payment. \
        Make sure to clarify all options, extras, and sizes to uniquely \
        identify the item from the menu. \
        You respond in a short, very conversational friendly style. \
        The menu includes: \
        - pure parakeet: 12.95, 10.00, 7.00 \
        - fentanillo parakeet: 10.95, 9.25, 6.50 \
        - anguel parakeet: 11.95, 9.75, 6.75 \
        - trizz: 4.50, 3.50 \
        - crippy: 7.25 \
        Toppings: \
        - extra basuco: 2.00 \
        - cueros: 1.50 \
        - trillador: 3.00 \
        - gotas: 3.50 \
        - tubos: 1.50 \
        - Turra: 1.00 \
        Drinks: \
        - coke: 3.00, 2.00, 1.00 \
        - sprite: 3.00, 2.00, 1.00 \
        - bottled water: 5.00 \
        """
    }
]

# Entrada de texto
inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here...')

# Botón para iniciar la conversación
button_conversation = pn.widgets.Button(name="Chat!")

# Función para recopilar mensajes y mostrarlos en los paneles


def collect_messages(event):
    # Obtener el valor del prompt desde el input
    prompt = inp.value

    # Limpiar el valor del input
    inp.value = ''

    # Agregar el mensaje del usuario al contexto
    context.append({'role': 'user', 'content': prompt})

    # Obtener la respuesta completada del asistente
    response = get_completion_from_messages(context)

    # Agregar el mensaje del asistente al contexto
    context.append({'role': 'assistant', 'content': response})

    # Limpiar los paneles
    panels.clear()

    # Agregar los paneles de visualización de los mensajes al contenedor
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600))
    )
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(
            response, width=600, style={'background-color': '#F6F6F6'}))
    )

    # Actualizar la interfaz gráfica
    dashboard.update()


# Vincular la función collect_messages al botón
button_conversation.on_click(collect_messages)

# Crear el panel de la interfaz gráfica
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(pn.Column(*panels), loading_indicator=True, height=300),
)
# Mostrar el panel en la interfaz
dashboard
