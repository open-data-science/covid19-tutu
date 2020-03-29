# Визуализация потоков транспорта и плотности населения
На данных, предоставленных Tutu.ru для сообщества ODS.

Веб-сервер на <a href=https://palletsprojects.com/p/flask/>Flask</a> и обёртка для <a href=https://vasturiano.github.io/globe.gl/>Globe.GL</a>.

# Использование

1. `python .\main.py` - запускает сервер по адресу `http://localhost:8080/`
2. Вызов `http://localhost:8080/fit` - перезаписывает выходной файл `.\templates\OUTPUT.html`

# Альтернатива

Покрутить глобус <a href=https://safronov.kiev.ua/ods/tutu.html>здесь</a>