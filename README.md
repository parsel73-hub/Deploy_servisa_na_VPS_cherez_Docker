# Number / Random / Fact API

Python-сервис на FastAPI с эндпоинтами для генерации случайных чисел, фактов и бросков кубиков. Запускается в Docker-контейнере и разворачивается на VPS через Docker Compose.

## Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/` | Приветствие + список эндпоинтов |
| GET | `/health` | Health-check (статус сервиса) |
| GET | `/api/random?min=1&max=100` | Случайное число из диапазона |
| GET | `/api/fact` | Случайный факт |
| GET | `/api/dice?sides=6&count=3` | Бросок кубиков |

## Быстрый старт (локально)

### Запуск через Docker Compose

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

Проверка:

```bash
curl http://localhost:8080/health
# {"status":"ok"}
```

Остановка:

```bash
docker compose -f infra/docker-compose.yml down
```

### Запуск без Docker (Python + uvicorn)

```bash
pip install -r app/requirements.txt
uvicorn --app-dir app main:app --port 8050
```

Проверка:

```bash
curl http://localhost:8050/health
```

---

## Сборка Docker-образа

Сборка образа из корня проекта (одной командой, как требует задание):

```bash
docker build -f infra/Dockerfile -t number-fact-api .
```

Запуск собранного образа:

```bash
docker run -d --name number-fact-api -p 8080:8000 number-fact-api
curl http://localhost:8080/health
docker stop number-fact-api
```

---

## Деплой на VPS reg.ru

### 1. Заказ VPS

1. Зарегистрируйся на [reg.ru](https://www.reg.ru).
2. Перейди в раздел [VPS/VDS-серверы](https://www.reg.ru/vps).
3. Выбери конфигурацию:
   - ОС: **Ubuntu 22.04 LTS** или **24.04 LTS**
   - Минимум: 1 CPU / 1 GB RAM (для FastAPI+Docker достаточно)
4. Оплати из личного кабинета (принимаются карты РФ).
5. Дождись готовности сервера — придёт письмо с IP, логином (`root`) и паролем.

### 2. Настройка сервера

Подключись к серверу по SSH:

```bash
ssh root@<IP_СЕРВЕРА>
```

Обнови систему и установи Docker:

```bash
apt update && apt upgrade -y

# Установка Docker (официальный скрипт)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Проверка
docker --version
docker compose version

# Настрой фаервол
ufw allow 22/tcp
ufw allow 8080/tcp
ufw --force enable
```

### 3. Развёртывание сервиса

Установи Git (если ещё не установлен):

```bash
apt install -y git
```

Клонируй репозиторий:

```bash
git clone https://github.com/<ТВОЙ_ЛОГИН>/Deploy_servisa_na_VPS_cherez_Docker.git
cd Deploy_servisa_na_VPS_cherez_Docker
```

Запусти через Compose:

```bash
docker compose -f infra/docker-compose.yml up -d --build
```

### 4. Проверка работоспособности

```bash
curl http://localhost:8080/health
# {"status":"ok"}
```

Или открой в браузере:

```
http://<IP_СЕРВЕРА>:8080/health
http://<IP_СЕРВЕРА>:8080/api/fact
http://<IP_СЕРВЕРА>:8080/api/random?min=1&max=100
```

### 5. Управление сервисом

Перезапуск:

```bash
docker compose -f infra/docker-compose.yml restart
```

Просмотр логов:

```bash
docker compose -f infra/docker-compose.yml logs -f app
```

Остановка:

```bash
docker compose -f infra/docker-compose.yml down
```

---

## Переменные окружения

Скопируй шаблон в `.env` и при необходимости измени значения:

```bash
cp infra/.env.example infra/.env
```

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `HOST_PORT` | `8080` | Порт на хост-машине |
| `APP_NAME` | `number-fact-api` | Имя приложения |
| `LOG_LEVEL` | `info` | Уровень логирования |

> Файл `.env` **НЕ** попадает в git.

---

## Структура проекта

```
.
├── app/                          # Код сервиса (в git)
│   ├── main.py                   # FastAPI-приложение
│   └── requirements.txt          # Зависимости
├── infra/                        # Инфраструктура (в git)
│   ├── Dockerfile                # Сборка образа
│   ├── .dockerignore             # Исключения для образа
│   ├── docker-compose.yml        # Запуск через Compose
│   └── .env.example              # Шаблон переменных
├── .gitignore                    # Игнорируемые файлы
└── черновики/                    # Игнорируется (не трогаем)
```

---

## Критерии приёмки

- [x] Контейнер собирается одной командой `docker build`
- [x] Сервис запускается через `docker compose up`
- [x] Приложения доступно по публичной ссылке
- [x] README позволяет повторить развёртывание
- [x] Секреты отсутствуют в git
- [x] Нет запуска напрямую через Python на сервере
- [x] Нет ручной установки зависимостей на сервере
