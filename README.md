# JonyaTooL

JonyaTooL - это утилита для работы с Discord аккаунтами, включающая проверку токенов, спам сообщений, проверку привязанных карт и сортировку токенов.

## Установка

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/JonyaCode/JonyaTooL
    cd JonyaTooL
    ```

2. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Конфигурация

Отредактируйте файл `config.yaml`, чтобы настроить утилиту под свои нужды:

```yaml
settings:
  use_proxies: true
  num_threads: 100
  chrome_version: "122"
  iproyal_log: "login"
  iproyal_pass: "password"
  iproyal_country: "us"
  proxy_source: "file" # file or generate
  delay_between_tasks: 1 
  spam_threads: 10
  billing_threads: 10
  ```

## Файлы данных

### `data/tokens.txt`
Файл с токенами для проверки. Токены могут быть в формате `token` или `email:pass:token`.

### `data/proxy.txt`
Файл с прокси для использования при проверках.

### `data/billing/`
Папка для хранения результатов проверки привязанных карт:
- `valid.txt` - токены с привязанными картами.
- `invalid.txt` - токены без привязанных карт.

### `data/checker/`
Папка для хранения результатов проверки токенов:
- `valid.txt` - валидные токены.
- `invalid.txt` - невалидные токены.

### `spamer/`
Папка для файлов спамера:
- `tokens.txt` - токены для спама.
- `used_tokens.txt` - использованные токены.
- `message.txt` - сообщение для отправки.

## Структура проекта

```
JonyaTooL/
├── core/
│   ├── billing_checker.py
│   ├── config_loader.py
│   ├── proxy_manager.py
│   ├── spammer.py
│   ├── token_checker.py
│   ├── token_loader.py
│   ├── token_manager.py
│   └── date_sorter.py
├── data/
│   ├── tokens.txt
│   ├── proxy.txt
│   ├── billing/
│   │   ├── valid.txt
│   │   └── invalid.txt
│   ├── checker/
│   │   ├── valid.txt
│   │   └── invalid.txt
├── spamer/
│   ├── tokens.txt
│   ├── used_tokens.txt
│   └── message.txt
├── config.yaml
├── main.py
└── requirements.txt
```

## Использование

Запустите основной скрипт:

```bash
python main.py
```

### Меню

Выберите нужное действие из меню:

- `Check Tokens`
- `Sort Tokens by Date`
- `Spam Messages`
- `Check Cards`
- `Exit`

### Check Tokens

Эта функция проверяет валидность токенов. Токены загружаются из файла `data/tokens.txt`.

1. Убедитесь, что файл `data/tokens.txt` существует и содержит токены в формате:
    ```
    token
    email:pass:token
    ```

2. Запустите программу и выберите `Check Tokens`.

Результаты будут сохранены в:

- `data/checker/valid.txt`
- `data/checker/invalid.txt`

### Sort Tokens by Date

Эта функция сортирует токены по дате их создания. Токены загружаются из файла `data/tokens.txt`.

1. Убедитесь, что файл `data/tokens.txt` существует и содержит токены в формате:
    ```
    token
    email:pass:token
    ```

2. Запустите программу и выберите `Sort Tokens by Date`.

Результаты будут сохранены в указанное место после сортировки.

### Spam Messages

Эта функция отправляет сообщения во все доступные лички и чаты.

1. Убедитесь, что файлы в папке `spamer` существуют:
    - `spamer/tokens.txt` - Токены для спама.
    - `spamer/message.txt` - Сообщение для отправки.

2. Запустите программу и выберите `Spam Messages`.

Отправленные сообщения будут записаны в `spamer/used_tokens.txt`.

### Check Cards

Эта функция проверяет наличие привязанных карт к аккаунтам.

1. Убедитесь, что файл `data/tokens.txt` существует и содержит токены в формате:
    ```
    token
    email:pass:token
    ```

2. Запустите программу и выберите `Check Cards`.

Результаты будут сохранены в:

- `data/billing/valid.txt`
- `data/billing/invalid.txt`

### Exit

Эта функция завершает работу программы.

## Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для подробностей.
