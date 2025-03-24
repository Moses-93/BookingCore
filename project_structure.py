import os
from pathlib import Path

def should_ignore(name):
    """Визначає, чи потрібно ігнорувати файл/папку"""
    return name.startswith('__') or name.startswith('.')

def print_project_structure(start_path, prefix=""):
    """Рекурсивно виводить структуру директорій з ігноруванням прихованих файлів"""
    try:
        items = sorted(os.listdir(start_path))
    except PermissionError:
        return  # Ігноруємо папки без доступу
    
    # Фільтруємо приховані файли та кеш
    items = [item for item in items if not should_ignore(item)]
    
    for i, item in enumerate(items):
        item_path = os.path.join(start_path, item)
        is_last = i == len(items) - 1
        
        # Визначаємо префікси для відображення
        connector = "└── " if is_last else "├── "
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        # Виводимо поточний елемент
        print(f"{prefix}{connector}{item}{'/' if os.path.isdir(item_path) else ''}")
        
        # Рекурсивно обробляємо піддиректорії
        if os.path.isdir(item_path):
            print_project_structure(item_path, new_prefix)

if __name__ == "__main__":
    project_root = Path.cwd()
    print(f"{project_root.name}/")
    print_project_structure(project_root)