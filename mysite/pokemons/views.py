import random

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import requests

from .models import Event


def page(request, num=0):
    webpage = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={num * 5}&limit=5").json()

    for i in range(len(webpage['results'])):
        webpage['results'][i]['info'] = get_pokemon_info(webpage['results'][i]['name'])

    template = loader.get_template("pokemons/index.html")
    context = {
        "pokemons": webpage,
        "num_next": num + 1,
        "num_prev": num - 1,
    }
    return HttpResponse(template.render(context, request))


def pokemon(request, name):
    info = get_pokemon_info(name)
    context = {
        "pokemon": get_pokemon_info(name),
        "hp": info['stats'][0]['base_stat'],
        "attack": info['stats'][1]['base_stat'],
    }
    return render(request, "pokemons/pokemon.html", context)


def fight(request, name):
    pokemon_id = random.randint(1, get_pokemon_count())
    if pokemon_id > 1017:
        pokemon_id = 10000 + pokemon_id - 1017
    pokemon_pc = get_pokemon_info(pokemon_id)
    pokemon_player = get_pokemon_info(name)
    return render(request, "pokemons/fight.html", {
        "pokemon_pc": pokemon_pc,
        "hp_pc": pokemon_pc['stats'][0]['base_stat'],
        "attack_pc": pokemon_pc['stats'][1]['base_stat'],
        "pokemon_player": pokemon_player,
        "hp_player": pokemon_player['stats'][0]['base_stat'],
        "attack_player": pokemon_player['stats'][1]['base_stat'],
    })


def result(request, name):
    event = Event()
    event.description = request.POST["event"]
    event.save()
    return HttpResponse(f"Event saved: {event.description}")


def search(request):
    webpage = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset=0&limit={get_pokemon_count()}").json()
    context = {
        "pokemons": webpage,
        "search_text": request.POST.get("search"),
    }
    return render(request, "pokemons/search.html", context)


def get_pokemon_count():
    return requests.get("https://pokeapi.co/api/v2/pokemon").json()['count']


def get_pokemon_info(name):
    return requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}").json()
