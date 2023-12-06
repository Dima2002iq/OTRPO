import random

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.mail import EmailMessage
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout, authenticate, login

from ftplib import FTP
import requests
import os

from .forms import RegisterForm, LoginForm
from .models import Event
from .token import account_activation_token


def get_pokemons(num):
    webpage = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={num * 5}&limit=5").json()

    for i in range(len(webpage['results'])):
        webpage['results'][i]['info'] = get_pokemon_info(webpage['results'][i]['name'])
    return webpage


def page(request, num=0):
    webpage = get_pokemons(num)
    template = loader.get_template("pokemons/index.html")
    context = {
        "pokemons": webpage,
        "num_next": num + 1,
        "num_prev": num - 1,
    }
    # test
    return HttpResponse(template.render(context, request))


@cache_page(60 * 60)
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
        "pokemon_pc_id": pokemon_id,
        "hp_pc": pokemon_pc['stats'][0]['base_stat'],
        "attack_pc": pokemon_pc['stats'][1]['base_stat'],
        "pokemon_player": pokemon_player,
        "pokemon_player_id": pokemon_player['id'],
        "hp_player": pokemon_player['stats'][0]['base_stat'],
        "attack_player": pokemon_player['stats'][1]['base_stat'],
    })


def result(request, name):
    if request.POST["send_type"] == 'db':
        event = Event()
        event.description = request.POST["event"]
        event.pokemon_player = request.POST["pokemon_player"]
        event.pokemon_pc = request.POST["pokemon_pc"]
        event.pokemon_winner = request.POST["pokemon_winner"]
        event.rounds = request.POST["round"]
        event.user_id = request.user.id
        event.save()
        return HttpResponse(f"Event saved: {event.description}")
    else:
        mail_subject = 'New event happened!'
        message = request.POST["event"]
        to_email = request.POST["email"]

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse(f"Event sent via email.")


def save(request, name):
    if request.method == 'POST':
        pokemon = get_pokemon_info(name)
        data = request.POST.dict()
        markdown = f"# [{name}](https://pokeapi.co/api/v2/pokemon/{name})\n"
        markdown += "## Info\n"
        if "is_pokemon_height" in data.keys():
            markdown += f" * height: {pokemon['height']}\n"
        if "is_pokemon_weight" in data.keys():
            markdown += f" * weight: {pokemon['weight']}\n"
        if "is_pokemon_hp" in data.keys():
            markdown += f" * hp: {pokemon['stats'][0]['base_stat']}\n"
        if "is_pokemon_attack" in data.keys():
            markdown += f" * attack: {pokemon['stats'][1]['base_stat']}\n"
        try:
            ftp = FTP(data["server"])
            ftp.login(data["login"], data["password"])
            if not f"{timezone.now().strftime('%Y%m%d')}" in ftp.nlst():
                ftp.mkd(f"{timezone.now().strftime('%Y%m%d')}")
            ftp.cwd(f"{timezone.now().strftime('%Y%m%d')}")
            with open(f"{pokemon['name']}.md", "w") as file:
                file.write(markdown)
            ftp.storbinary(f"STOR {pokemon['name']}.md", open(f"{pokemon['name']}.md", "rb"))
            ftp.quit()
            os.remove(f"{pokemon['name']}.md")
        except Exception as e:
            return HttpResponse(f"Error: {e}")
        return HttpResponse("File successfully saved!")


def search(request):
    webpage = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset=0&limit={get_pokemon_count()}").json()
    context = {
        "pokemons": webpage,
        "search_text": request.POST.get("search"),
    }
    return render(request, "pokemons/search.html", context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User successfully created!")
        return HttpResponse("Error: user not created!")
    else:
        form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form})


def login_prove(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        input_token = request.POST["input_token"]
        token = request.POST["token"]
        if token == input_token:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Error: wrong token!")


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        token = account_activation_token.make_token(user)
        mail_subject = 'Одноразовый токен для входа'
        message = token
        to_email = user.email

        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        if user is not None:
            return render(request, 'registration/login_prove.html',
                          {'username': username, 'password': password,  'token': token})
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def get_pokemon_count():
    return requests.get("https://pokeapi.co/api/v2/pokemon").json()['count']


def get_pokemon_info(name):
    return requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}").json()
