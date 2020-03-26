**Abstract**

Если вы читаете эту аннотацию, значит вас реально прижало или же вам по доброй воле, самим надо рассчитать Shapley Value Attribution algorithm.
Далее для простоты просто Shapley.

В этой документации мы постараемся максимально детально описать все шаги и методы расчетов Shapley.</br>
Для улучшения вашего понимания мы постараемся все абстрактные термины и сущности подкреплять наглядными иллюстрациями и всевозможными
упрощения для достижения максимального понимания.

По возможносчти мы будем максимально избегать сложных и путанных математических терминов ,чтобы даже те из вас кто не дружит с математикой
смогли сформировать у себя в голове ясную картину происходящего.</br>
Для выпендрежников :rooster: же  ,кто с линейной алгеброй и теорие вероятностей  на "ты" ,мы обязательно прикрепим ссылки на математические работы где вы сможете найти
ответы на все технические и математические подводные камни, с которыми вы столкнетесь при работе с Shapley.

Все вычисления Shapley algorithm построены основываясь на упрощенной версии алгоритма ("упрощенной"-не значит плохо/хуже старичок,
"упрощенной" - значит та же точность ,тот же функционал только быстрее и понятнее). Ссылки на все матриалы по старой доброй традиции ищите в конце
документации.



**Introduction**

`r/zoomertimeforlearning`

Сразу позволим себе оговорится и прояснить для себя и для Вас ,какие задачи/цели не стоят перед этой документаций.
  - Как работает Shapley Algorithm .Мы не ставим перед собой задачи детально донести до читателя все тонкости и нюансы
    устройства работы алгоритма.В конце доки мы обязательно прикрепим ссылки на очень полезные ресурсы благодаря которым ,
    Вы дорогой читатель, сможете погрузится во все математические и технические подробности Shapley Algorithm. Если вы первый
    раз слышите про такой алгоритм, то советуем вам сначала прочитать теоретические доки , понять и ~~простить~~ осмыслить материал,
    и потом уже смело врываться в нашу доку
  - Как устроена теория вероятностей, "почему это выржаение равно вот этому",теория множеств,линейнай алгебра и прочая математическая
    дичь. Наши возможности ограничены , у вас тоже мало времени , и мы это в вас ценим , но попутно описывать весь математический подвал
    у нас просто не хватит сил (+ r/bonusmyfriend ) . В сети огромное колицества литературы и ресурсов которые в случае чего (формула,
    символ, равенство) смогут до вас донести суть всего этого заумного безобразия

Теперь ,к тому чему вы научитесь прочитав эту документаци.

  - Быстро расчитывать аттрибутированные веса для каждого канала
  - Понять аттрибутированный вес каждой позиции (порядковый нормер места в цепях в которых находился канал) внутри каждого канала
  - Проверять ,правильно ли рассчитаны все аттрибутированные веса
  - Как строятся матрицы для быстрых расчетов аттрибуции и где их можно использовать в дальнейшем для решения уже `custom tasks`
  
**Contents**

1.1 Theory Shapley Quick Start
1.2 shapelyLib methods
1.3 How to use shapley

2.1 What is it "Shapley properties" and why we need to check shapleyLib result
2.2 How to use 

2.1 Theory Ordered Shapley Quick start
2.2.shapleyOrderLib methods
2.3 How to use shapleyOrderLib

1.1 Theory Shapley Quick Start




1.2 shapelyLib methods

shapelyLib состоит всего из 10 методов, и в этой главе мы постараемся объяснить, основываясь на какой логике работает каждый из них.
Рассмотрим в какой последовательности их следует применять,какой метод за что отвечает,имеет ли он альтернативу внутри класса а так же какие данные (тип,формат и прочее) следует подавать на вход для каждого из них. 
И конечно же что мы ожидаем получить на выходе у каждогио из этих методов.

![Image alt](https://github.com/toseek01/Instagram/blob/master/illustration/LetsGo_Technik.png)

Итак,имеем следующие методы:
- `__init__`
- `UniqueChainCheck`
- `ChainSplit`
- `ChannelDict`
- `UniqueChannel`
- `ChanneltoID`
- `ZeroMatrix`
- `Vectorization`
- `Calc`
- `DecodeDict`

**__init__**

Здесь хранятся все стратегически важные переменные для внутренних расчетов Shapley и формирования алгебраических сущностей,кодировки каналов,режимы расчетов и тд. Обо всем подробно будет изложено ниже. 

`args`
- data.Аггрегированные данные (pandas) ,строящиеся на основе DMP и/или Google Analytics.Собой эти данные представляют аггрегированные пути пользователей(userID) и соответствующие им конверсии, которые эти пользователи совершили ,перемещаясь по этим цепочкам.
Пример:</br>
a->b->d 10</br>
c->c->d 4</br>
a->a->e 8</br>
b->a->b 3</br>
d->e->b 6</br>

Цепочки могут быть разной длины,содержать сколько угодно каналов ,а также сколько угодно повторяющихся каналов внутри одной цепи.Главное требование к цепочкам, это то ,чтобы все они были *уникальными*.
Конверсии должны иметь тип Int или Float.

- channel_delimiter. Разделитель csv файла ,по дефолту стоит `;`
- loyal. Аргумент loyal является режимом условной лояльности. Проще говоря это сколько контактов с рекламой у пользователей должно было произойти прежде чем они совершили конверсию.Пусть лояльными userID мы будем считать людей кто имел не более N контактов с рекламой, после которых они совершили конверсию. Благодаря этому режиму ,мы можем смотреть как изменятся Shapley values у нелояльной аудитории по отношению к лояльной.Режим имеет только два значения - True и False
- loyal_position. Количество контактов с рекламой для определения лояльной аудитории.Только если loyal==True

`variables`
смотри в shapleyLib.py

**UniqueChainCheck** Проверяет уникальность цепей в *data*. Если будут обнаружены дубликаты, вычисления останавливаются и выдается ошибка

**ChainSplit** Разбивает последовательность каналов (строку) на каналы . Пример: a->b->c => [a,b,c]
**ChannelDict** Словарь для хранения уникального ID для каждого канала
**UniqueChannel** Считает количество уцикальных каналов во всех цепях ,а также создает список этих уникальных каналов
**ChanneltoID** Конвертирует канал(название канала String) в его ID ,которое было создано и хранится в ранее указанном `ChannelDict`
**ZeroMatrix** Cj\\Создает матрицу размером (кол-во цепей Х кол-во уникальных каналов
