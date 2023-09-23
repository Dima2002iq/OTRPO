from urllib.request import Request, urlopen

request_site = Request("https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0", headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(request_site).read()
print(webpage)
