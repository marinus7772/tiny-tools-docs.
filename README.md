# tiny-tools-docs.
# Attendance Tool

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

---

## Описание

**Attendance Tool** — это утилита командной строки для работы с данными посещаемости студентов. Программа позволяет генерировать тестовые данные, рассчитывать статистику, отмечать посещаемость и экспортировать отчеты.

Инструмент разработан в рамках курсовой работы на тему **«Разработка веб-приложения для учета посещаемости студентов»**.

### Основные возможности

- **Генерация тестовых данных** — создание JSON-файлов с группами и студентами
- **Расчет статистики** — подсчет процента посещаемости
- **Отметка посещаемости** — простановка статусов для студентов
- **Поиск студентов** — быстрый поиск по имени
- **Экспорт данных** — выгрузка в CSV формат
- **Форматированный вывод** — таблицы, JSON, текстовый формат

---

## Требования

| Компонент | Требование |
|-----------|------------|
| **Python** | версия 3.8 или выше |
| **Операционная система** | Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.15+ |

---

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/marinus7772/tiny-tools-docs.git
cd tiny-tools-docs

# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python cli.py generate --group "ПКС-21" --students 25 --output group_pks21.json

✅ Сгенерированы данные для группы 'ПКС-21' с 25 студентами
📁 Данные сохранены в файл: group_pks21.json

python cli.py stats --input group_pks21.json --format table

==================================================
📊 СТАТИСТИКА ПОСЕЩАЕМОСТИ
==================================================
Группа: ПКС-21
Всего студентов: 25
Всего отметок: 0
--------------------------------------------------
✅ Присутствовало: 0 (0.0%)
❌ Отсутствовало: 0 (0.0%)
==================================================


