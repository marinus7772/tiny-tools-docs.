import argparse
import sys
import os
from datetime import datetime
from .core import AttendanceProcessor
from .utils import export_to_csv, print_table

def main():
    parser = argparse.ArgumentParser(
        prog='attendance-tool',
        description='Утилита для обработки данных посещаемости студентов',
        epilog='Пример: attendance-tool generate --group ПКС-21 --students 25'
    )
    
    # Аргументы для основной команды
    parser.add_argument('-v', '--version', action='version', version='attendance-tool 1.0.0')
    parser.add_argument('--debug', action='store_true', help='Режим отладки')
    
    # Подпарсеры для команд
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда: generate — генерация тестовых данных
    generate_parser = subparsers.add_parser('generate', help='Генерация тестовых данных')
    generate_parser.add_argument('--group', type=str, required=True, help='Название группы')
    generate_parser.add_argument('--students', type=int, default=25, help='Количество студентов (по умолчанию: 25)')
    generate_parser.add_argument('--output', type=str, default='attendance_data.json', help='Файл для сохранения')
    
    # Команда: stats — расчет статистики
    stats_parser = subparsers.add_parser('stats', help='Расчет статистики посещаемости')
    stats_parser.add_argument('--input', type=str, required=True, help='Входной JSON-файл с данными')
    stats_parser.add_argument('--format', choices=['text', 'json', 'table'], default='table', help='Формат вывода')
    
    # Команда: export — экспорт в Excel/CSV
    export_parser = subparsers.add_parser('export', help='Экспорт данных')
    export_parser.add_argument('--input', type=str, required=True, help='Входной JSON-файл')
    export_parser.add_argument('--output', type=str, default='report.csv', help='Выходной файл')
    export_parser.add_argument('--format', choices=['csv', 'xlsx'], default='csv', help='Формат экспорта')
    
    # Команда: mark — отметить посещаемость
    mark_parser = subparsers.add_parser('mark', help='Отметка посещаемости студента')
    mark_parser.add_argument('--data', type=str, required=True, help='JSON-файл с данными')
    mark_parser.add_argument('--student', type=str, required=True, help='Имя студента')
    mark_parser.add_argument('--status', choices=['present', 'absent'], required=True, help='Статус посещаемости')
    mark_parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'), help='Дата (ГГГГ-ММ-ДД)')
    
    # Команда: find — поиск студента
    find_parser = subparsers.add_parser('find', help='Поиск студента')
    find_parser.add_argument('--data', type=str, required=True, help='JSON-файл с данными')
    find_parser.add_argument('--name', type=str, required=True, help='Имя или часть имени для поиска')
    
    args = parser.parse_args()
    
    # Проверка наличия команды
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Настройка режима отладки
    if args.debug:
        print("[DEBUG] Режим отладки включен", file=sys.stderr)
        print(f"[DEBUG] Аргументы: {args}", file=sys.stderr)
    
    # Обработка команд
    processor = AttendanceProcessor()
    
    try:
        if args.command == 'generate':
            data = processor.generate_data(args.group, args.students)
            processor.save_data(data, args.output)
            print(f"Сгенерированы данные для группы '{args.group}' с {args.students} студентами")
            print(f"Данные сохранены в файл: {args.output}")
            
        elif args.command == 'stats':
            data = processor.load_data(args.input)
            stats = processor.calculate_stats(data)
            
            if args.format == 'table':
                print_table(stats)
            elif args.format == 'json':
                import json
                print(json.dumps(stats, indent=2, ensure_ascii=False))
            else:  # text
                print(f"Группа: {stats['group_name']}")
                print(f"Всего студентов: {stats['total_students']}")
                print(f"Всего отметок: {stats['total_marks']}")
                print(f"Присутствий: {stats['total_present']} ({stats['present_percent']}%)")
                print(f"Отсутствий: {stats['total_absent']} ({stats['absent_percent']}%)")
                
        elif args.command == 'export':
            data = processor.load_data(args.input)
            export_to_csv(data, args.output)
            print(f"✅ Данные экспортированы в файл: {args.output}")
            
        elif args.command == 'mark':
            data = processor.load_data(args.data)
            processor.mark_attendance(data, args.student, args.status, args.date)
            processor.save_data(data, args.data)
            print(f"Студент '{args.student}' отмечен как {args.status} за {args.date}")
            
        elif args.command == 'find':
            data = processor.load_data(args.data)
            results = processor.find_student(data, args.name)
            if results:
                print(f"🔍 Найдено студентов: {len(results)}")
                for student in results:
                    print(f"   - {student['name']} (группа: {student['group']})")
            else:
                print(f"Студент с именем '{args.name}' не найден")
                
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
