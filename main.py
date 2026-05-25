from rich import print
from rich.prompt import Prompt
import os
import string
from pathlib import Path
import subprocess
import hashlib

os.system("title as checker v0.2")

banner = """[yellow] █████╗ ███████╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ [/yellow]
██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
[yellow]███████║███████╗    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝[/yellow]
██╔══██║╚════██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
[yellow]██║  ██║███████║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║[/yellow]
╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"""

CHEAT_SIGNATURES = [
    "procName=minecraft.windows.exe",
    "procName=Minecraft.Windows.exe",
]

VARIABLE_DLL_HASHES = [
    "e5e42ed888a382ac96f1ef7ff2f4a825",
    "8c9cf1602a68f27a84a309ce37d12bac",
]

SKIP_DIRS = {
    '$Recycle.Bin', 'System Volume Information', 'Windows', 
    'ProgramData', 'AppData', 'node_modules', '.git',
    'Microsoft', 'Intel', 'AMD', 'NVIDIA'
}

def get_available_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def scan_file(filepath, signatures):
    try:
        for encoding in ['utf-8', 'utf-16', 'cp1251', 'latin-1', 'utf-8-sig']:
            try:
                with open(filepath, 'r', encoding=encoding, errors='ignore') as f:
                    content = f.read()
                    for sig in signatures:
                        if sig in content:
                            return True
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
    except (PermissionError, OSError, FileNotFoundError):
        pass
    return False

def get_file_md5(filepath):
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest().lower()
    except (PermissionError, OSError, FileNotFoundError):
        return None

def fatescan():
    drives = get_available_drives()
    detected_count = 0
    scanned_files = 0

    print(f"\n[yellow][FATESCAN][/yellow] Найдено дисков: {', '.join(drives)}")
    print("[FATESCAN] Начинаю сканирование config.txt ...\n")

    for drive in drives:
        print(f"[SCAN] Диск {drive} ...")

        try:
            for root, dirs, files in os.walk(drive, topdown=True):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]

                if 'config.txt' in files:
                    filepath = os.path.join(root, 'config.txt')
                    scanned_files += 1

                    if scan_file(filepath, CHEAT_SIGNATURES):
                        print(f"\n[red][!] Fate Injector detected: {filepath}[/red]")
                        detected_count += 1

        except PermissionError:
            continue
        except Exception as e:
            print(f"[ERROR] Диск {drive}: {e}")

    print(f"\n[green][FATESCAN] Завершено.[/green]")
    print(f"[INFO] Проверено config.txt: {scanned_files}")
    print(f"[INFO] Обнаружено инжекторов Fate: {detected_count}")

def variablescan():
    drives = get_available_drives()
    scanned_dlls = 0
    variable_detected = 0
    scanned_exes = 0
    exe_detected = 0

    print(f"\n[yellow][VARIABLESCAN][/yellow] Найдено дисков: {', '.join(drives)}")
    print("[VARIABLESCAN] Начинаю сканирование DLL и EXE файлов ...\n")

    for drive in drives:
        print(f"[SCAN] Диск {drive} ...")

        try:
            for root, dirs, files in os.walk(drive, topdown=True):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]

                for file in files:
                    if file.lower().endswith('.dll'):
                        filepath = os.path.join(root, file)
                        scanned_dlls += 1

                        file_hash = get_file_md5(filepath)
                        if file_hash and file_hash in VARIABLE_DLL_HASHES:
                            print(f"\n[red][!!!] Variable DLL detected: {filepath}[/red]")
                            variable_detected += 1

                    if file.lower().endswith('.exe'):
                        filepath = os.path.join(root, file)
                        scanned_exes += 1

                        if "injopter" in file.lower():
                            print(f"\n[red][!!!] Variable EXE Detected: {filepath}[/red]")
                            exe_detected += 1

        except PermissionError:
            continue
        except Exception as e:
            print(f"[ERROR] Диск {drive}: {e}")

    print(f"\n[green][VARIABLESCAN] Завершено.[/green]")
    print(f"[INFO] Проверено DLL файлов: {scanned_dlls}")
    print(f"[INFO] Обнаружено Variable DLL: {variable_detected}")
    print(f"[INFO] Проверено EXE файлов: {scanned_exes}")
    print(f"[INFO] Обнаружено Variable EXE: {exe_detected}")

def appdatascan():
    users_path = Path("C:\\Users")
    detected_count = 0

    print(f"\n[yellow][APPDATASCAN][/yellow] Сканирование AppData\\Local\\Packages ...\n")

    if not users_path.exists():
        print("[ERROR] Папка C:\\Users не найдена")
        return

    for user_dir in users_path.iterdir():
        if not user_dir.is_dir():
            continue

        packages_path = user_dir / "AppData" / "Local" / "Packages"
        if not packages_path.exists():
            continue

        try:
            for item in packages_path.iterdir():
                if not item.is_dir():
                    continue

                if "minecraft" in item.name.lower():
                    roaming_path = item / "RoamingState"

                    if not roaming_path.exists():
                        continue

                    try:
                        roaming_items = list(roaming_path.iterdir())
                    except PermissionError:
                        continue

                    has_configs = any((roaming_path / "configs").exists() and (roaming_path / "configs").is_dir() for _ in [0])
                    has_scripts = any((roaming_path / "scripts").exists() and (roaming_path / "scripts").is_dir() for _ in [0])
                    has_logs = (roaming_path / "logs.txt").exists()

                    if has_configs or has_scripts or has_logs:
                        print(f"[red][!!!] Variable Folders/Log file detected: {roaming_path}[/red]")
                        detected_count += 1

        except PermissionError:
            continue
        except Exception as e:
            print(f"[ERROR] {user_dir.name}: {e}")

    print(f"\n[green][APPDATASCAN] Завершено.[/green]")
    print(f"[INFO] Обнаружено подозрительных папок/файлов: {detected_count}")

if __name__ == "__main__":
    subprocess.run(["cls"], shell=True)
    print(banner)
    fatescan()
    variablescan()
    appdatascan()
    print("\n[green]Все сканы завершены.[/green]")
    input()