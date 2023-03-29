# Poetry Wall
# Excerpt example with OpenAI ChatGPT 
# Roni Bandini, Buenos Aires, March 2023

import openai

# Define OpenAI API key 
openai.api_key = ""

# Set up the model and prompt
model_engine = "text-davinci-003" 

prompt = "Resumir en una oración de 5 palabras: La señorita del abanico va por el puente del fresco río. Los caballeros con sus levitas, miran el puente sin barandillas. La señorita del abanico y los volantes, busca marido. Los caballeros están casados, con altas rubias de idioma blanco. Los grillos cantan por el Oeste. La señorita va por lo verde. Los grillos cantan bajo las flores. Los caballeros, van por el Norte. La señorita del abanico va por el puente del fresco río."

# Generate a response
completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

response = completion.choices[0].text
print(response)
