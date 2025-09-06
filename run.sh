#!/bin/bash

# Скрипт для швидкого запуску додатку

echo "🚀 Запуск Gomin..."

# Перевірка, чи існує віртуальне середовище
if [ ! -d "venv" ]; then
    echo "📦 Створення віртуального середовища..."
    python3 -m venv venv
fi

# Активація віртуального середовища
echo "🔧 Активація віртуального середовища..."
source venv/bin/activate

# Встановлення залежностей
echo "📚 Встановлення залежностей..."
pip install -r requirements.txt

# Запуск додатку
echo "✨ Запуск Flask додатку..."
cd app
python app.py
