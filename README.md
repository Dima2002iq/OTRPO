# Открытые технологии разработки программного обеспечения

Шушарин Дмитрий Владимирович, ОТРПО-П-МОиАИС-20.01-1

## Запуск проекта

### С получением веб-приложения с [Dockerhub](https://hub.docker.com/r/dmitryshusharin/otrpo)
```shell
docker compose --env-file .env.docker up -d
```

### Со сборкой веб-приложения
```shell
docker compose --env-file .env.docker up -d --build
```