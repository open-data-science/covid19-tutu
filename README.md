# covid19-tutu
# TODO

- [ ] Разбиение на транспорт
	- [ ] Добавить рёбра под виды транспорта
	- [ ] Учёт времени в пути
	- [ ] Посчитать константы для видов траспорта
	- [ ] Добавить модель на пересчёт числа заболевших в пути
- [ ] Уточнение модели для города
	- [ ] Подобрать константы recovery rate, contact rate
	- [ ] Разбиение по возрастным группам (?)
- [ ] Покрутить параметры, посмотреть что получится:
	- [ ] Симулировать карантин для отдельных городов (снизить contact rate)
	- [ ] Симулировать фильтрацию по прибытии в город, аэропорт (снизить contact rate)
	- [ ] Удалёнка рёбер (выкинуть часть рейсов)
- [ ] Посмотреть насколько влияет инициализация
	- [ ] Официальная статистика собирается через гузно: насемплировать разных случайных инициализаций
	- [ ] Данные по транспорту шумные: пошатать частоты перемещения в разных направлениях
- [ ] Связь брутфорса с pageRank и eigVec	
- [ ] Число реально заболевших, умерших и здоровых (оценка)
- [ ] Вычислить коэффициент заразности


# notebooks

We take some notebooks from this [repo](https://github.com/DmitrySerg/COVID-19):

- sir_modeling_no_graph.ipynb [source notebook](https://github.com/DmitrySerg/COVID-19/blob/6a7a321ccf23723c890eba8d0ad55b9382d29a5e/models/SIR_estimation.ipynb)
- transport_epidemic_simulation.ipynb [source notebook](https://github.com/DmitrySerg/COVID-19/blob/6a7a321ccf23723c890eba8d0ad55b9382d29a5e/models/COVID-19.ipynb)

We refactor them and restructuring. Also, we create core library and draw library for beautifully our code. Now, we add 
new data from [here](https://github.com/CSSEGISandData) (see bottom).

# Как оно работает сейчас

На каждую итерацию у нас есть два цикла: в первом мы обновляем считаем динамику в городах, в следующем перемещаем между городами людей.  
  
В городе сейчас считается SIR модель. Можно учитывать намного больше разных деталей, вроде возрастных групп, сообществ, случайных факторов, но нужно помнить, что это потребует уточнения и по транспорту (например если добавим возрастные группы в городе, надо будет добавить их и по перемещениям), во-вторых может оказаться, что SIR даст тот же результат, если ей чуть параметры подвинуть.  
  
Между городами перемещение реализовано самым наивным способом. Здесь легко добавить реалистичности не трогая модель города. Однако тоже может оказаться, что тот же результат получится линейным преобразованием от наивного способа, то есть подкруткой скорости транспорта, например.

# Первым делом

Перебрать параметры и посмотреть что на что влияет, а что вовсе не важно. Точные числа мы скорее всего не предскажем, или не сможем проверить, а динамику и зависимости знать важно.

# Описание data

`raw_data.csv` - dates from tutu.ru: flights, trains, buses by april 2019 year. 

`cities.csv` - coordinates and population 

`full_graph.csv` - routes (generated data by `notebook/transport_epidemic_simulation.ipynb`)

`age65.csv` - groups risk 65+ by regions

`cities_infection.csv` - file cities with confirmed and recovered people in Russia by 18.03; 19.03; 20.03 dates.

`CSSEGISandData` - historical data by pandemic [source](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series). Данные обновляются ежедневно

`population.csv` - population by countries [source](https://datahub.io/JohnSnowLabs/population-figures-by-country)

`russia_regions_desease.csv` - Russia disease by province [source-1](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D1%81%D0%BF%D1%80%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5_COVID-19_%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8#cite_note-sptbl5b-60), [source-2](https://rospotrebnadzor.ru/search/index.php?tags=&q=%E2%FB%FF%E2%EB%E5%ED%EE&where=&how=d&from=&to=) 
