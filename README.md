# gFlash v0.3.2 - Fastboot Device Flasher

Professional console utility for flashing Android devices via fastboot protocol with complete protection against dangerous operations.

## Requirements

- Python 3.7+
- libusb (automatically installed via pyusb on Windows)
- PyUSB for USB communication

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Creating Config (gflash-config)

Interactive config creator for JSON configurations:

```bash
python gflash-config.py
python gflash-config.py my_device_config.json
```

The configurator will interactively ask for:
- Device name
- Configuration description
- List of partitions with files (required/optional)
- Partitions to erase
- Whether to reboot after flashing
- Reboot mode

Example:
```
[?] Device name [My Android Device]: Google Pixel 5
[?] Partition name (e.g., boot, system, recovery): boot
[?] Image file path (relative or absolute): boot.img
[?] Is this partition required? [Y/n]: y
[?] SHA256 hash for verification (optional): a1b2c3d4...
```

### Watch Mode (Automatic Device Detection)

Waits for device connection in fastboot mode:

```bash
python gflash.py watch flash_config.json
```

On device connection, asks for confirmation or (in auto mode) starts immediately:

```bash
python gflash.py watch flash_config.json auto
```

Perfect for development with frequent flashing - start and forget:
```bash
gflash.py watch config.json auto    # Runs in background
# Connect phone - automatic flashing!
```

### List Devices
```bash
python gflash.py devices
```

### Get Device Info
```bash
python gflash.py info
```

### Flash Partition
```bash
python gflash.py flash boot.img boot
python gflash.py flash system.img system
python gflash.py flash recovery.img recovery
```

### Erase Partition
```bash
python gflash.py erase system
python gflash.py erase userdata
```

### Reboot
```bash
python gflash.py reboot
python gflash.py reboot bootloader
python gflash.py reboot recovery
```

### Flash All Partitions from Config (Flash-all)
```bash
python gflash.py flash-all flash_config.json
```

The `flash_config.json` contains list of all partitions to flash in the correct order.

### Validate Config without Changes (Dry-run)

```bash
python gflash.py dry-run flash_config.json
```

Dry-run mode checks:
- ✓ All files exist
- ✓ Files have correct size
- ✓ SHA256 hashes match (if specified)
- ✓ Configuration fully ready for flashing
- ✓ **Makes no changes to device**

Perfect to use before flash-all:
```bash
python gflash.py dry-run flash_config.json
python gflash.py flash-all flash_config.json
```

### Backup Partition

Save individual partitions with SHA256 verification:

```bash
python gflash.py backup boot backup_boot.img
python gflash.py backup system backup_system.img
```

### Backup All Partitions from Config

```bash
python gflash.py backup-all flash_config.json ./backups
```

Creates files like `boot.img`, `system.img` etc. in `./backups/` directory with SHA256 hashes in log.

### Version
```bash
python gflash.py version
```

## Flash-all Configuration

gFlash supports flashing multiple partitions from a single JSON config. Example config:

```json
{
  "device_name": "Example Device",
  "description": "Android device flash configuration",
  "version": "1.0",
  "partitions": [
    {
      "name": "boot",
      "file": "boot.img",
      "required": true,
      "description": "Boot partition (kernel + ramdisk)",
      "sha256": "a1b2c3d4e5f6..."
    },
    {
      "name": "system",
      "file": "system.img",
      "required": true,
      "sha256": "f6e5d4c3b2a1..."
    },
    {
      "name": "recovery",
      "file": "recovery.img",
      "required": false
    }
  ],
  "erase_partitions": ["cache", "userdata"],
  "post_flash_reboot": true,
  "reboot_mode": "bootloader"
}
```

### Config Fields:
- `device_name` - device name for reference
- `partitions` - array of partitions to flash
  - `name` - partition name on device
  - `file` - path to image file (relative to config)
  - `required` - if true, flashing error stops entire operation
  - `sha256` - (optional) hash for pre-flash verification
  - `description` - description (optional)
- `erase_partitions` - partitions to erase after flashing
- `post_flash_reboot` - whether to reboot after operation
- `reboot_mode` - reboot mode (bootloader, recovery, etc.)

## Building EXE

```bash
python build.py
```

Executable files will be in `dist/gFlash.exe` and `dist/gFlash-config.exe`

## Supported Devices

Utility supports most Android devices with fastboot:
- Google Pixel (all generations)
- Samsung Galaxy (S10+, S20, S21, etc.)
- OnePlus
- Xiaomi
- Motorola
- HTC
- Sony Xperia
- And other devices with fastboot...

## Notes

- Device must be in fastboot mode (usually: Power Off → Volume Down + Power)
- Windows may require driver installation (ADB/fastboot drivers)
- Bootloader unlock will erase all device data (depends on manufacturer)
- **Always verify file hash before flashing**
- **Don't disconnect device during operation**
- **Use backup-all before flash-all for insurance**

## Backup Functionality (v0.3.2+)

gFlash can save current partition state from device before flashing.

### Workflow for Safe Flashing - Option 1

```bash
# 1. Create config
gflash-config.py device_config.json

# 2. Validate config (dry-run without device contact)
gflash.py dry-run device_config.json

# 3. Save current state (insurance)
gflash.py backup-all device_config.json ./backups

# 4. Flash device
gflash.py flash-all device_config.json
```

### Workflow for Safe Flashing - Option 2

For development with frequent flashing (Watch mode):

```bash
# 1. Create and validate config
gflash-config.py dev_config.json
gflash.py dry-run dev_config.json

# 2. Start watch with auto-flash
gflash.py watch dev_config.json auto

# 3. Turn on phone in fastboot mode - automatic flashing!
# Results in console + gflash.log
```

## Logging

All operations logged to `gflash.log` with timestamps and levels:
- INFO - normal operations
- WARNING - potentially dangerous actions
- ERROR - errors and critical events

Example:
```
2024-01-15 10:30:45,123 [INFO] gFlash v0.3.2 started with command: flash
2024-01-15 10:30:45,234 [INFO] Flash operation started: boot.img -> boot
2024-01-15 10:30:46,456 [INFO] File SHA256: a1b2c3d4e5f6...
2024-01-15 10:30:47,789 [INFO] User confirmed flash operation
```

## Security Features

### Partition Protection
- **Safe partitions list** (SAFE_PARTITIONS) for safe erasing
- **Critical partitions list** (CRITICAL_PARTITIONS) - cannot be erased, require double confirmation for flashing
- **Name validation** - filters special characters and injection attempts

### File Verification
- File existence and type checking
- Size limitation (up to 2GB)
- SHA256 hash before flashing for integrity control
- Mandatory user confirmation before operation

### Error Handling
- Detailed USB error handling (timeout, disconnection)
- Proper resource cleanup on failure
- All operations logged to `gflash.log`

### User Confirmation
- Critical partitions require "DANGER" input
- Unknown partitions require "yes" confirmation
- Unlock requires "unlock" input

## Changelog

### v0.3.2
- ✅ Watch mode for automatic device detection
- ✅ Auto-flash option for flashing on connection
- ✅ Perfect for development with frequent iterations
- ✅ Interactive selection on device detection
- ✅ Device connection/disconnection tracking

### v0.3.1
- ✅ gflash-config - interactive configurator
- ✅ Create JSON configs via CLI without editing
- ✅ Input data validation
- ✅ Configuration preview before saving
- ✅ Support for all config fields

### v0.3.0
- ✅ Dry-run mode for config validation without changes
- ✅ Check all files before flashing
- ✅ SHA256 hash validation in dry-run mode
- ✅ Detailed report of what will be flashed
- ✅ Safe preparation before flash-all
- ✅ Information about total data transfer size

### v0.2.4
- ✅ Backup command for saving partitions from device
- ✅ Backup-all for mass saving from config
- ✅ SHA256 verification during backup
- ✅ SHA256 verification support in config (optional)
- ✅ Detailed progress during backup operations
- ✅ Insurance before flash-all - cache current state

### v0.2.3
- ✅ Flash-all command for multiple partitions from JSON config
- ✅ Support for required and optional partitions
- ✅ Configurable flashing order
- ✅ Automatic partition erasing after flashing
- ✅ Support for relative paths in config
- ✅ Detailed config validation before operation

### v0.2.2
- ✅ Streaming data transfer (4MB chunks) instead of full RAM loading
- ✅ Progress bar for hashing and file sending
- ✅ Improved device response validation
- ✅ Support for large files (up to 2GB) on memory-limited systems
- ✅ More informative output (sizes in MB, operation timing)

### v0.2.1
- ✅ Complete logging to gflash.log
- ✅ Utility versioning
- ✅ Detailed USB error handling
- ✅ SHA256 file integrity check

### v0.2.0
- ✅ Safe and critical partition lists
- ✅ Partition name validation
- ✅ Mandatory confirmations for dangerous operations

## Examples of Dangerous Operations and Protection

### Attempt to Erase Critical Partition
```bash
$ python gflash.py erase bootloader
[ERROR] Partition 'bootloader' is CRITICAL and CANNOT be erased!
```

### Attempt to Flash Critical Partition
```bash
$ python gflash.py flash tz.mbn tz
[WARNING] Partition 'tz' is CRITICAL and protected!
[WARNING] Flashing this partition can brick the device!
Type 'DANGER' to proceed: DANGER
[*] Flashing tz (123456 bytes)
```

## License

g-lab project

## Требования

- Python 3.7+
- libusb (установлена на Windows автоматически через pyusb)
- PyUSB для работы с USB

## Установка

```bash
pip install -r requirements.txt
```

## Использование

### Создание конфига (gflash-config)

Интерактивный конфигуратор для создания JSON конфигов:

```bash
python gflash-config.py
python gflash-config.py my_device_config.json
```

Конфигуратор интерактивно спросит:
- Название устройства
- Описание конфигурации
- Список партиций с файлами (обязательные/опциональные)
- Партиции для стирания
- Нужна ли перезагрузка после прошивки
- Режим перезагрузки

Пример:
```
[?] Device name [My Android Device]: Google Pixel 5
[?] Partition name (e.g., boot, system, recovery): boot
[?] Image file path (relative or absolute): boot.img
[?] Is this partition required? [Y/n]: y
[?] SHA256 hash for verification (optional): a1b2c3d4...
```

### Watch режим (автоматическое обнаружение)

Ждёт подключения устройства в fastboot режиме:

```bash
python gflash.py watch flash_config.json
```

При подключении спросит подтверждение или (в режиме auto) сразу прошьёт:

```bash
python gflash.py watch flash_config.json auto
```

Отлично для разработки при частых прошивках - запустить и забыть:
```bash
gflash.py watch config.json auto    # Работает в фоне
# Подключи телефон - автоматически начнёт прошивку
```

### Список устройств
```bash
python gflash.py devices
```

### Получение информации об устройстве
```bash
python gflash.py info
```

### Прошивка партиции
```bash
python gflash.py flash boot.img boot
python gflash.py flash system.img system
python gflash.py flash recovery.img recovery
```

### Стирание партиции
```bash
python gflash.py erase system
python gflash.py erase userdata
```

### Перезагрузка
```bash
python gflash.py reboot
python gflash.py reboot bootloader
python gflash.py reboot recovery
```

### Прошивка всех партиций из конфига (Flash-all)
```bash
python gflash.py flash-all flash_config.json
```

Конфиг `flash_config.json` содержит список всех партиций для прошивки в нужном порядке.

### Проверка конфига без изменений (Dry-run)
```bash
python gflash.py dry-run flash_config.json
```

Режим Dry-run проверяет:
- ✓ Все файлы существуют
- ✓ Файлы имеют правильный размер
- ✓ SHA256 хэши совпадают (если указаны)
- ✓ Конфигурация полностью готова к прошивке
- ✓ **Не вносит никакие изменения на устройство**

Идеально использовать перед flash-all:
```bash
python gflash.py dry-run flash_config.json
python gflash.py flash-all flash_config.json
```

### Резервная копия партиции
```bash
python gflash.py backup boot backup_boot.img
python gflash.py backup system backup_system.img
```

### Резервная копия всех партиций из конфига
```bash
python gflash.py backup-all flash_config.json ./backups
```

Создаст в папке `./backups` файлы вроде `boot.img`, `system.img` и т.д. с SHA256 хешами в логе.

### Версия
```bash
python gflash.py version
```

## Flash-all конфигурация

gFlash теперь поддерживает прошивку всех партиций из одного JSON конфига. Пример конфига:

```json
{
  "device_name": "Example Device",
  "partitions": [
    {
      "name": "boot",
      "file": "boot.img",
      "required": true,
      "description": "Boot partition",
      "sha256": "a1b2c3d4e5f6..."
    },
    {
      "name": "system",
      "file": "system.img",
      "required": true,
      "sha256": "f6e5d4c3b2a1..."
    },
    {
      "name": "recovery",
      "file": "recovery.img",
      "required": false
    }
  ],
  "erase_partitions": ["cache", "userdata"],
  "post_flash_reboot": true,
  "reboot_mode": "bootloader"
}
```

### Поля конфига:
- `device_name` - название девайса для справки
- `partitions` - массив партиций для прошивки
  - `name` - имя партиции на устройстве
  - `file` - путь к файлу образа (относительно конфига)
  - `required` - если true, ошибка прошивки прерывает всю операцию
  - `sha256` - (опционально) хэш файла для верификации перед прошивкой
  - `description` - описание (опционально)
- `erase_partitions` - партиции для стирания после прошивки
- `post_flash_reboot` - перезагрузить ли устройство после операции
- `reboot_mode` - режим перезагрузки (bootloader, recovery и т.д.)

## Оптимизация v0.2.3

### Потоковая передача данных (Chunked Upload)
- Файлы больше не загружаются полностью в память
- Данные отправляются чанками по 4 МБ
- Поддержка файлов до 2 GB на системах с малым объемом ОЗУ
- Прогресс-бар при хешировании и отправке данных

### Улучшенная валидация ответов
- Проверка размера ответа (не более 4096 байт)
- Детектирование малформированных ответов
- Логирование подозрительных пакетов для отладки

### Детальный прогресс
```
[*] Reading file: boot.img (100.50 MB)
[*] Computing file hash...
[*] Hash progress: 100.0%
[*] File SHA256: a1b2c3d4e5f6...
[*] Sending data to device...
[*] Upload progress: 45.3% (45.6/100.5 MB)
```

## Безопасность v0.2.2

### Защита от опасных операций
- **Белый список партиций** (SAFE_PARTITIONS) для безопасного стирания
- **Чёрный список партиций** (CRITICAL_PARTITIONS) - невозможно стирать, требуют двойного подтверждения для прошивки
- **Валидация имён** - фильтрация спецсимволов и injection-попыток

### Проверка файлов
- Проверка существования и типа файла
- Ограничение размера (до 2GB)
- Подсчёт SHA256 хэша перед прошивкой для контроля целостности
- Обязательное подтверждение пользователем перед операцией

### Обработка ошибок
- Детальная обработка USB-ошибок (timeout, disconnection)
- Корректное закрытие ресурсов при сбое
- Логирование всех операций в `gflash.log`

### Подтверждение пользователя
- Для критических партиций требуется ввод "DANGER"
- Для неизвестных партиций требуется подтверждение "yes"
- Для разблокировки требуется ввод "unlock"

## Логирование

Все операции логируются в файл `gflash.log` с временными метками и уровнями:
- INFO - обычные операции
- WARNING - потенциально опасные действия
- ERROR - ошибки и критические события

Пример:
```
2024-01-15 10:30:45,123 [INFO] gFlash v0.2.1 started with command: flash
2024-01-15 10:30:45,234 [INFO] Flash operation started: boot.img -> boot
2024-01-15 10:30:46,456 [INFO] File SHA256: a1b2c3d4e5f6...
2024-01-15 10:30:47,789 [INFO] User confirmed flash operation
```

## Сборка в exe

```bash
python build.py
```

Исполняемый файл будет в папке `dist/gFlash.exe`

## Поддерживаемые устройства

Утилита поддерживает большинство Android-устройств с fastboot:
- Google Pixel (все поколения)
- Samsung Galaxy (S10+, S20, S21 и т.д.)
- OnePlus
- Xiaomi
- Motorola
- HTC
- Sony Xperia
- И другие устройства с fastboot...

## Примечания

- Устройство должно быть в режиме fastboot (обычно: выключи → Volume Down + Power)
- На Windows может потребоваться установка драйверов (ADB/fastboot drivers)
- Перед разблокировкой бутлоадера устройство скидывает все данные
- **Всегда проверяй хэш файла перед прошивкой**
- **Не выключай устройство во время операции**

## Changelog

### v0.3.2
- ✅ Watch режим для автоматического обнаружения устройства
- ✅ Auto-flash для прошивки при подключении
- ✅ Идеально для разработки при частых итерациях
- ✅ Интерактивный выбор при обнаружении
- ✅ Отслеживание подключения устройства

### v0.3.1
- ✅ gflash-config - интерактивный конфигуратор
- ✅ Создание JSON конфигов через CLI без редактирования
- ✅ Валидация данных при вводе
- ✅ Предпросмотр конфигурации перед сохранением
- ✅ Поддержка всех полей конфига

### v0.3.0
- ✅ Dry-run режим для валидации конфига без изменений
- ✅ Проверка всех файлов перед прошивкой
- ✅ Валидация SHA256 хэшей в dry-run режиме
- ✅ Детальный отчет о том, что будет прошито
- ✅ Безопасная подготовка перед flash-all
- ✅ Информация о общем размере данных для передачи

### v0.2.4
- ✅ Backup команда для сохранения партиций с устройства
- ✅ Backup-all для массового сохранения из конфига
- ✅ SHA256 верификация при backup
- ✅ Поддержка SHA256 верификации в конфиге (опционально)
- ✅ Детальный прогресс при backup операциях
- ✅ Страховка перед flash-all - можно сначала закэшировать текущее состояние
- ✅ Flash-all команда для прошивки нескольких партиций из JSON конфига
- ✅ Поддержка обязательных (required) и опциональных партиций
- ✅ Конфигурируемый порядок прошивки
- ✅ Автоматическое стирание партиций после прошивки
- ✅ Поддержка относительных путей в конфиге
- ✅ Детальная валидация конфига перед операцией

### v0.2.2
- ✅ Потоковая передача данных (4MB chunks) вместо полной загрузки в RAM
- ✅ Прогресс-бар для хеширования и отправки файлов
- ✅ Улучшенная валидация ответов от устройства
- ✅ Поддержка больших файлов (до 2GB) на системах с ограниченной памятью
- ✅ Более информативный вывод (размеры в MB, время операций)

### v0.2.1
- ✅ Полное логирование в gflash.log
- ✅ Версионирование утилиты
- ✅ Детальная обработка USB-ошибок
- ✅ SHA256 проверка целостности файла

### v0.2.0
- ✅ Белые и черные списки партиций
- ✅ Валидация имён партиций
- ✅ Обязательные подтверждения для опасных операций

## Примеры опасных операций и защиты

### Попытка стереть критическую партицию
```bash
$ python gflash.py erase bootloader
[ERROR] Partition 'bootloader' is CRITICAL and CANNOT be erased!
```

### Попытка прошить критическую партицию
```bash
$ python gflash.py flash tz.mbn tz
[WARNING] Partition 'tz' is CRITICAL and protected!
[WARNING] Flashing this partition can brick the device!
Type 'DANGER' to proceed: DANGER
[*] Flashing tz (123456 bytes)
```

## Полный Workflow для безопасной прошивки

### Вариант 1: Одна прошивка с проверкой

```bash
# 1. Создаём конфиг
python gflash-config.py device_config.json

# 2. Проверяем конфиг
python gflash.py dry-run device_config.json

# 3. Сохраняем текущее состояние (страховка)
python gflash.py backup-all device_config.json ./backups

# 4. Прошиваем устройство
python gflash.py flash-all device_config.json
```

### Вариант 2: Разработка с частыми прошивками (Watch mode)

```bash
# 1. Создаём и проверяем конфиг
python gflash-config.py dev_config.json
python gflash.py dry-run dev_config.json

# 2. Запускаем watch с auto-flash
python gflash.py watch dev_config.json auto

# 3. Включаем телефон в fastboot режиме - автоматическая прошивка!
# Результат в консоли + gflash.log
```

## Лицензия

g-lab project
