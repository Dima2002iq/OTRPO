import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from urllib.request import Request, urlopen
import json

from django.urls import reverse

from .models import Event


def page(request, num=0):
    request_site = Request(f"https://pokeapi.co/api/v2/pokemon?offset={num * 5}&limit=5",
                           headers={"User-Agent": "Mozilla/5.0"})
    webpage = json.loads(urlopen(request_site).read())

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
    pokemon_pc = get_pokemon_info(random.randint(1, get_pokemon_count()))
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
    request_site = Request(f"https://pokeapi.co/api/v2/pokemon?offset=0&limit={get_pokemon_count()}",
                           headers={"User-Agent": "Mozilla/5.0"})
    webpage = json.loads(urlopen(request_site).read())
    context = {
        "pokemons": webpage,
        "search_text": request.POST.get("search"),
    }
    return render(request, "pokemons/search.html", context)


def get_pokemon_count():
    return json.loads(urlopen(Request("https://pokeapi.co/api/v2/pokemon", headers={"User-Agent": "Mozilla/5.0"}))
                      .read())['count']


def get_pokemon_info(name):
    return json.loads(urlopen(Request(f"https://pokeapi.co/api/v2/pokemon/{name}",
                                      headers={"User-Agent": "Mozilla/5.0"})).read())
