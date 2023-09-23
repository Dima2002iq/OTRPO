from django.http import HttpResponse
from django.template import loader
from urllib.request import Request, urlopen
import json

def index(request):
    request_site = Request("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0", headers={"User-Agent": "Mozilla/5.0"})
    webpage = json.loads(urlopen(request_site).read())
    template = loader.get_template("pokemons/index.html")
    print(webpage)
    context = {
        "pokemons": webpage,
    }
    return HttpResponse(template.render(context, request))
