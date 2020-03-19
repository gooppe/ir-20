# Methods of Information Retrieval

[![Build Status](https://travis-ci.com/gooppe/ir-20.svg?token=4S4zJiazyUoqSfqTW3Zv&branch=master)](https://travis-ci.com/gooppe/ir-20)

- [Methods of Information Retrieval](#methods-of-information-retrieval)
  - [BooSearch](#boosearch)
    - [Установка](#%d0%a3%d1%81%d1%82%d0%b0%d0%bd%d0%be%d0%b2%d0%ba%d0%b0)
    - [Использование](#%d0%98%d1%81%d0%bf%d0%be%d0%bb%d1%8c%d0%b7%d0%be%d0%b2%d0%b0%d0%bd%d0%b8%d0%b5)
    - [Загрузка данных](#%d0%97%d0%b0%d0%b3%d1%80%d1%83%d0%b7%d0%ba%d0%b0-%d0%b4%d0%b0%d0%bd%d0%bd%d1%8b%d1%85)

## BooSearch

### Установка

Для установки локально:
```bash
pip install git+https://github.com/gooppe/ir-20
```

Можно запустить изолированно в контейнере:
```bash
git clone https://github.com/gooppe/ir-20 && cd ir-20
sudo docker install -t boosearch .
sudo docker run -it --rm -v /path/to/data:/workspace/data boosearch 
```

### Использование

Для построения индекса

```bash
boos index --data news.json --index index.json
```

Для поиска
```
boos search --data news.json --index index.json "машины & самолеты & ~(самокаты|мотоциклы)"
```

Для всех команд работает флаг `--help`, показывающий дополнительные параметры (размер буфера, число выводимых результатов, etc.)


### Загрузка данных

Скачиваем данные из пре-релиза и распаковываем

```bash
curl -LJO https://github.com/gooppe/ir-20/releases/download/v0.0.1-data/news.json.tgz
tar -zxvf news.json.tgz
```