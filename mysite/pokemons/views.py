from django.http import HttpResponse
from django.template import loader
from urllib.request import Request, urlopen
import json

def index(request):
    count = json.loads(urlopen(Request("https://pokeapi.co/api/v2/pokemon", headers={"User-Agent": "Mozilla/5.0"})).read())['count']

    request_site = Request(f"https://pokeapi.co/api/v2/pokemon?limit={count}&offset=0", headers={"User-Agent": "Mozilla/5.0"})
    webpage = json.loads(urlopen(request_site).read())
    print(webpage['count'])
    template = loader.get_template("pokemons/index.html")
    context = {
        "pokemons": webpage,
    }
    return HttpResponse(template.render(context, request))
