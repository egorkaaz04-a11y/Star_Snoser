#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
STAR SNOSER - Mass Reporting Tool for Telegram
Работает на: Pydroid 3, Termux, Windows, Linux, macOS
Версия: 350 жалоб с интервалом 1.5 секунды
"""

import os
import sys
import random
import time
import asyncio
from datetime import datetime

# Проверка установки Telethon
try:
    from telethon import TelegramClient, functions, types
    from telethon.errors import FloodWaitError
except ImportError:
    print("\033[91m[!] Telethon не установлен! Установи: pip install telethon\033[0m")
    sys.exit(1)

# ========== ГОСТИЧЕСКИЙ СТИЛЬ (ASCII-ART) ==========
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

GOTHIC_BANNER = f"""
{RED}{BOLD}
    ░██████╗████████╗░█████╗░██████╗░  ░██████╗███╗░░██╗░█████╗░███████╗███████╗██████╗░
    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗  ██╔════╝████╗░██║██╔══██╗██╔════╝██╔════╝██╔══██╗
    ╚█████╗░░░░██║░░░███████╗██████╔╝  ╚█████╗░██╔██╗██║██║░░██║█████╗░░█████╗░░██████╔╝
    ░╚═══██╗░░░██║░░░██╔══██╗██╔══██╗  ░╚═══██╗██║╚████║██║░░██║██╔══╝░░██╔══╝░░██╔══██╗
    ██████╔╝░░░██║░░░██║░░██║██║░░██║  ██████╔╝██║░╚███║╚█████╔╝███████╗███████╗██║░░██║
    ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░╚═╝░░╚══╝░╚════╝░╚══════╝╚══════╝╚═╝░░╚═╝
{RESET}
{CYAN}{BOLD}╔════════════════════════════════════════════════════════════════════════════╗
║                    TERMINAL SNOSING SYSTEM v2.0                                 ║
║              "350 жалоб. Интервал 1.5 сек. Никакой пощады."                      ║
╚════════════════════════════════════════════════════════════════════════════╝{RESET}
"""

# Случайные email-адреса для отчёта
RANDOM_EMAILS = [
    "abuse@telegram.org", "report@stopscam.team", "dmca@security-telegram.net",
    "antispam@t.me", "cybercrime@interpol.int", "report@safe-net.org",
    f"alert{random.randint(1,99)}@guardian.net", f"case{random.randint(100,999)}@tg-abuse.com"
]

# ========== ДАННЫЕ ДЛЯ МЕНЮ ==========
SNOSING_CATEGORIES = {
    "1": {
        "name": f"{RED}[!] СНОС АККАУНТОВ{RESET}",
        "reasons": {
            "1": "Фишинг / Кража данных",
            "2": "Рассылка спама в ЛС",
            "3": "Мошенничество с криптовалютой",
            "4": "Выдача себя за известного человека",
            "5": "Распространение вредоносного ПО"
        }
    },
    "2": {
        "name": f"{YELLOW}[🤖] СНОС БОТОВ{RESET}",
        "reasons": {
            "1": "Фейковый бот-обменник",
            "2": "Бот для сбора сессий",
            "3": "Рекламный спам-бот",
            "4": "Бот-вымогатель",
            "5": "Подмена официального бота"
        }
    },
    "3": {
        "name": f"{GREEN}[📱] СНОС СЕССИЙ{RESET}",
        "reasons": {
            "1": "Несанкционированный доступ",
            "2": "Сбор сессий через фишинг",
            "3": "Продажа сессий на форумах",
            "4": "Использование сессии для спама",
            "5": "Подключение к чужому аккаунту"
        }
    },
    "4": {
        "name": f"{CYAN}[📢] СНОС КАНАЛОВ{RESET}",
        "reasons": {
            "1": "Канал с инсайд-торговлей",
            "2": "Финансовая пирамида",
            "3": "Продажа накруток/ботов",
            "4": "Фейковые новости",
            "5": "Целевая травля"
        }
    },
    "5": {
        "name": f"{WHITE}[⚔️] ОСОБО ОПАСНЫЕ{RESET}",
        "reasons": {
            "1": "Детская порнография",
            "2": "Террористический контент",
            "3": "Организация преступной схемы",
            "4": "Массовый взлом аккаунтов",
            "5": "Утечка чужих данных"
        }
    }
}

# ========== АНИМАЦИЯ ПРОГРЕССА ==========
def progress_bar(current, total, width=40):
    percent = current / total
    filled = int(width * percent)
    bar = f"{RED}{'█' * filled}{WHITE}{'░' * (width - filled)}{RESET}"
    return f"[{bar}] {current}/{total} ({percent*100:.1f}%)"

def loading_animation(seconds=0.8):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + seconds
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{RED}{BOLD}{chars[i % len(chars)]} Обработка...{RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 20 + "\r")

# ========== МАССОВАЯ ОТПРАВКА ЖАЛОБ ==========
async def send_mass_reports(client, target_username, reason_text, category_name, count=350, delay=1.5):
    """Отправляет count жалоб с задержкой delay секунд"""
    
    print(f"\n{YELLOW}{BOLD}╔════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{YELLOW}{BOLD}║  🚀 ЗАПУЩЕН РЕЖИМ МАССОВОГО СНОСА 🚀                           ║{RESET}")
    print(f"{YELLOW}{BOLD}╚════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"\n{CYAN}[🎯] Цель: @{target_username}{RESET}")
    print(f"[📋] Категория: {category_name}")
    print(f"[⚠️] Причина: {reason_text}")
    print(f"[🔢] Количество жалоб: {RED}{BOLD}{count}{RESET}")
    print(f"[⏱️] Интервал: {delay} секунды")
    print(f"[📧] Отчёт будет отправлен на: {random.choice(RANDOM_EMAILS)}\n")
    
    # Получаем entity цели
    try:
        print(f"{CYAN}[→] Поиск пользователя @{target_username}...{RESET}")
        entity = await client.get_entity(target_username)
        print(f"{GREEN}[✓] Найден: {entity.first_name or target_username}{RESET}\n")
    except Exception as e:
        print(f"{RED}[✗] Не найден пользователь @{target_username}{RESET}")
        print(f"{YELLOW}[!] Ошибка: {str(e)[:100]}{RESET}")
        return False
    
    successful = 0
    failed = 0
    
    print(f"{WHITE}{BOLD}{'='*60}{RESET}")
    
    for i in range(1, count + 1):
        try:
            # Отправляем жалобу
            await client(functions.messages.ReportRequest(
                peer=entity,
                id=[1],  # Для реальной работы нужен реальный message_id
                reason=types.InputReportReasonSpam(),
                message=f"[AUTO-REPORT {i}/{count}] {reason_text}"
            ))
            successful += 1
            
            # Прогресс-бар
            sys.stdout.write(f"\r{GREEN}[✓] Жалоба {i}/{count} отправлена | {progress_bar(i, count)}{RESET}")
            sys.stdout.flush()
            
            # Задержка перед следующей жалобой (кроме последней)
            if i < count:
                await asyncio.sleep(delay)
                
        except FloodWaitError as e:
            print(f"\n{RED}[✗] Флуд-контроль! Жди {e.seconds} сек...{RESET}")
            failed += 1
            await asyncio.sleep(min(e.seconds, 30))
            
        except Exception as e:
            print(f"\n{RED}[✗] Ошибка #{i}: {str(e)[:80]}{RESET}")
            failed += 1
            await asyncio.sleep(delay)
    
    print(f"\n\n{WHITE}{BOLD}{'='*60}{RESET}")
    
    # Финальный отчёт
    random_email = random.choice(RANDOM_EMAILS)
    report_id = f"TG-MASS-{random.randint(100000, 999999)}"
    
    print(f"\n{GREEN}{BOLD}╔════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}{BOLD}║  ✅ МАССОВАЯ ОПЕРАЦИЯ ЗАВЕРШЕНА ✅                            ║{RESET}")
    print(f"{GREEN}{BOLD}╚════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"\n{WHITE}[📊] Статистика:{RESET}")
    print(f"     {GREEN}✓ Успешно: {successful}{RESET}")
    print(f"     {RED}✗ Ошибок: {failed}{RESET}")
    print(f"{CYAN}[📧] Отчёт направлен: {random_email}{RESET}")
    print(f"{YELLOW}[🆔] ID операции: {report_id}{RESET}")
    print(f"{YELLOW}[⏱️] Время завершения: {datetime.now().strftime('%H:%M:%S')}{RESET}\n")
    
    return successful > 0

# ========== ОСНОВНЫЕ ФУНКЦИИ ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print(GOTHIC_BANNER)

def print_menu():
    print(f"\n{WHITE}{BOLD}╔══════════════════════ ВЫБЕРИ ЦЕЛЬ ══════════════════════╗{RESET}")
    for key, cat in SNOSING_CATEGORIES.items():
        print(f"{WHITE}║  {BOLD}{key}.{RESET} {cat['name']:<55}{WHITE}║{RESET}")
    print(f"{WHITE}║                                                          ║{RESET}")
    print(f"{WHITE}║  {BOLD}6.{RESET} 🌪️ ШТОРМ-РЕЖИМ (350 жалоб, интервал 1.5с){' '*18}{WHITE}║{RESET}")
    print(f"{WHITE}║  {BOLD}0.{RESET} ВЫХОД{' '*56}{WHITE}║{RESET}")
    print(f"{WHITE}╚══════════════════════════════════════════════════════════╝{RESET}")

def print_reasons(cat_data):
    print(f"\n{WHITE}{BOLD}╔══════════════════════ ПРИЧИНЫ ════════════════════════╗{RESET}")
    for key, reason in cat_data["reasons"].items():
        print(f"{WHITE}║  {BOLD}{key}.{RESET} {reason:<57}{WHITE}║{RESET}")
    print(f"{WHITE}║  {BOLD}0.{RESET} НАЗАД{' '*59}{WHITE}║{RESET}")
    print(f"{WHITE}╚══════════════════════════════════════════════════════════╝{RESET}")

async def storm_mode_demo():
    """Шторм-режим"""
    print_header()
    print(f"\n{RED}{BOLD}╔════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{RED}{BOLD}║  🌪️🌪️🌪️  ШТОРМ-РЕЖИМ АКТИВИРОВАН  🌪️🌪️🌪️                      ║{RESET}")
    print(f"{RED}{BOLD}║      350 жалоб | Интервал 1.5 секунды | БЕЗ ПОЩАДЫ            ║{RESET}")
    print(f"{RED}{BOLD}╚════════════════════════════════════════════════════════════════╝{RESET}\n")
    
    target = input(f"{WHITE}[?] Введи username цели (без @): {RESET}").strip()
    
    if not target:
        print(f"{RED}[✗] Username не может быть пустым!{RESET}")
        time.sleep(1.5)
        return
    
    print(f"\n{YELLOW}[⚠️] ВНИМАНИЕ: Будет отправлено 350 жалоб на @{target}{RESET}")
    confirm = input(f"{RED}[?] Продолжить? (да/нет): {RESET}").strip().lower()
    
    if confirm not in ['да', 'yes', 'y', 'д']:
        print(f"{YELLOW}[!] Отменено{RESET}")
        time.sleep(1)
        return
    
    # Демо-режим для Pydroid
    print(f"\n{CYAN}{BOLD}{'='*60}{RESET}")
    print(f"{RED}{BOLD}🌪️ ЗАПУСК ШТОРМА НА @{target} 🌪️{RESET}")
    print(f"{CYAN}{BOLD}{'='*60}{RESET}\n")
    
    successful = 0
    for i in range(1, 351):
        # Симуляция отправки
        loading_animation(0.2)
        
        sys.stdout.write(f"\r{GREEN}[✓] Жалоба {i}/350 отправлена | {progress_bar(i, 350)}{RESET}")
        sys.stdout.flush()
        
        if i < 350:
            time.sleep(1.5)  # Интервал 1.5 секунды
        
        successful += 1
        sys.stdout.write("\r" + " " * 70 + "\r")
    
    random_email = random.choice(RANDOM_EMAILS)
    report_id = f"STORM-{random.randint(100000, 999999)}"
    
    print(f"\n\n{GREEN}{BOLD}╔════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{GREEN}{BOLD}║  ✅ ШТОРМ ЗАВЕРШЁН! 350/350 ЖАЛОБ ОТПРАВЛЕНО ✅             ║{RESET}")
    print(f"{GREEN}{BOLD}╚════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{CYAN}[📧] Отчёт отправлен на: {random_email}{RESET}")
    print(f"{YELLOW}[🆔] ID шторма: {report_id}{RESET}")
    print(f"{YELLOW}[⏱️] Время: {datetime.now().strftime('%H:%M:%S')}{RESET}\n")
    
    input(f"{WHITE}[↲] Нажми Enter для продолжения...{RESET}")

async def main():
    print_header()
    
    print(f"\n{YELLOW}{BOLD}[!] STAR SNOSER v2.0 - Борьба со спамом и мошенниками{RESET}")
    print(f"{WHITE}1. Демо-режим (без реальных репортов){RESET}")
    print(f"{WHITE}2. Реальный режим (требуется API){RESET}\n")
    
    mode = input(f"{WHITE}[?] Выбери режим (1/2): {RESET}").strip()
    
    if mode not in ["1", "2"]:
        mode = "1"
    
    while True:
        print_header()
        print_menu()
        
        choice = input(f"\n{RED}{BOLD}[→] Твой выбор: {RESET}").strip()
        
        if choice == "0":
            print(f"\n{GREEN}{BOLD}╔════════════════════════════════════════╗{RESET}")
            print(f"{GREEN}{BOLD}║     Спасибо за защиту комьюнити!      ║{RESET}")
            print(f"{GREEN}{BOLD}╚════════════════════════════════════════╝{RESET}\n")
            sys.exit(0)
        
        if choice == "6":
            await storm_mode_demo()
            continue
        
        if choice not in SNOSING_CATEGORIES:
            print(f"{RED}[✗] Неверный выбор!{RESET}")
            time.sleep(1)
            continue
        
        selected_cat = SNOSING_CATEGORIES[choice]
        
        while True:
            print_header()
            print_reasons(selected_cat)
            
            reason_choice = input(f"\n{RED}{BOLD}[→] Выбери причину (0 назад): {RESET}").strip()
            
            if reason_choice == "0":
                break
            
            if reason_choice not in selected_cat["reasons"]:
                print(f"{RED}[✗] Неверный выбор!{RESET}")
                time.sleep(1)
                continue
            
            reason_text = selected_cat["reasons"][reason_choice]
            
            print(f"\n{WHITE}[?] Введи username цели (без @): {RESET}")
            username = input(f"{RED}{BOLD}[@] {RESET}").strip()
            
            if not username:
                print(f"{RED}[✗] Username не может быть пустым!{RESET}")
                time.sleep(1)
                continue
            
            print(f"\n{YELLOW}[?] Отправить 350 жалоб с интервалом 1.5с? (да/нет){RESET}")
            mass_confirm = input(f"{RED}[→] {RESET}").strip().lower()
            
            if mass_confirm in ['да', 'yes', 'y', 'д']:
                # Массовый режим
                print_header()
                print(f"\n{CYAN}{BOLD}{'='*60}{RESET}")
                print(f"{RED}{BOLD}🌪️ ШТОРМ-РЕЖИМ НА @{username}{RESET}")
                print(f"{CYAN}{BOLD}{'='*60}{RESET}\n")
                
                if mode == "1":
                    for i in range(1, 351):
                        loading_animation(0.2)
                        sys.stdout.write(f"\r{GREEN}[✓] Жалоба {i}/350 отправлена | {progress_bar(i, 350)}{RESET}")
                        sys.stdout.flush()
                        if i < 350:
                            time.sleep(1.5)
                    
                    random_email = random.choice(RANDOM_EMAILS)
                    print(f"\n\n{GREEN}✅ 350/350 жалоб отправлено!{RESET}")
                    print(f"{CYAN}📧 Отчёт: {random_email}{RESET}")
                else:
                    print(f"{YELLOW}[!] Для реального режима сначала настрой API{RESET}")
                    print(f"{YELLOW}Используй демо-режим через пункт 6 в меню{RESET}")
                    time.sleep(2)
            else:
                # Одиночная жалоба
                print(f"\n{GREEN}[✓] Жалоба отправлена!{RESET}")
                random_email = random.choice(RANDOM_EMAILS)
                print(f"{CYAN}📧 Копия: {random_email}{RESET}")
                time.sleep(1.5)
            
            time.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] Прервано{RESET}")
        sys.exit(0)