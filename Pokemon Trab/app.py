from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas as rotas

# Função para mapear tipo de personalidade para uma lista de Pokémon
def get_pokemon_by_personality(personality_type):
    personality_to_pokemon = {
        "Extroversão": {
            "pokemon": ["pikachu", "charmander", "squirtle"],
            "explanation": "Você é extrovertido e energético, assim como os Pokémon elétricos e cheios de vitalidade."
        },
        "Neuroticismo": {
            "pokemon": ["psyduck", "cubone", "jigglypuff"],
            "explanation": "Você pode ser um pouco mais emocional e sensível, como esses Pokémon que também têm suas próprias lutas emocionais."
        },
        # Adicione explicações para outros tipos de personalidade aqui
    }

    result = personality_to_pokemon.get(personality_type)
    if result:
        chosen_pokemon = random.choice(result["pokemon"])
        explanation = result["explanation"]
    else:
        # Se o tipo de personalidade não estiver mapeado, escolhemos Pikachu como padrão
        chosen_pokemon = "pikachu"
        explanation = "Não temos uma correspondência específica para o seu tipo de personalidade, então escolhemos Pikachu para você!"

    return chosen_pokemon, explanation

def get_pokemon(data):
    name = data.get('name')
    birthdate = data.get('birthdate')
    personality_type = data.get('personality_type')

    pokemon_name, explanation = get_pokemon_by_personality(personality_type)

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    pokemon_data = response.json()

    image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']

    return jsonify({
        'user': {
            'name': name,
            'birthdate': birthdate,
            'personality_type': personality_type
        },
        'pokemon': {
            'name': pokemon_data['name'],
            'type': pokemon_data['types'][0]['type']['name'],
            'abilities': [ability['ability']['name'] for ability in pokemon_data['abilities']],
            'base_experience': pokemon_data['base_experience'],
            'image_url': image_url
        },
        'explanation': explanation
    })

# Rota para processar os dados do formulário
@app.route('/get_pokemon', methods=['POST'])
def get_pokemon_route():
    data = request.json
    return get_pokemon(data)

if __name__ == '__main__':
    app.run(debug=True)
