from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from urllib.request import Request, urlopen
import json


# def index(request):
#     request_site = Request("https://pokeapi.co/api/v2/pokemon", headers={"User-Agent": "Mozilla/5.0"})
#     webpage = json.loads(urlopen(request_site).read())
#     template = loader.get_template("pokemons/index.html")
#     context = {
#         "pokemons": webpage,
#         "next": webpage["next"][webpage["next"].find('?'):],
#     }
#     return HttpResponse(template.render(context, request))

def page(request, num=0):
    request_site = Request(f"https://pokeapi.co/api/v2/pokemon?offset={num * 20}&limit=20",
                           headers={"User-Agent": "Mozilla/5.0"})
    webpage = json.loads(urlopen(request_site).read())
    template = loader.get_template("pokemons/index.html")
    context = {
        "pokemons": webpage,
        "num_next": num + 1,
        "num_prev": num - 1,
    }
    return HttpResponse(template.render(context, request))


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
