import curses
import subprocess
import os

def get_files():
    resultado = subprocess.run(["ls", "-a"], capture_output=True, text=True)
    if resultado.returncode == 0:
        files = resultado.stdout.strip().split('\n')
        return [f for f in files if f not in ('.', '..')]
    else:
        return []

def call_editor(file_path):
    def run_ide(stdscr):
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()

        try:
            with open(file_path, 'r') as f:
                editor_content = [line.rstrip('\n') for line in f.readlines()]
        except FileNotFoundError:
            editor_content = [""]

        current_line = 0
        current_col = 0
        running = True

        def render_editor():
            nonlocal current_line, current_col, editor_content
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            stdscr.addstr(0, 0, "NOIX IDE CLI - F2: Executar | F3: Salvar | ESC: Sair")

            for i, line in enumerate(editor_content):
                if i < height - 2:
                    stdscr.addstr(i + 1, 0, line)

            if current_line >= len(editor_content):
                current_line = len(editor_content) - 1
            if current_col > len(editor_content[current_line]):
                current_col = len(editor_content[current_line])

            stdscr.move(current_line + 1, current_col)
            stdscr.refresh()

        def run_code():
            nonlocal editor_content
            code = "\n".join(editor_content)
            try:
                result = subprocess.run(['python3', '-c', code], capture_output=True, text=True)
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)

            stdscr.clear()
            stdscr.addstr(0, 0, "Resultado da execução:")
            stdscr.addstr(2, 0, output)
            stdscr.refresh()
            stdscr.getch()

        def save_file():
            with open(file_path, 'w') as f:
                f.write("\n".join(editor_content))
            stdscr.addstr(0, 0, f"Arquivo {file_path} salvo com sucesso!")
            stdscr.refresh()
            stdscr.getch()

        while running:
            render_editor()
            key = stdscr.getch()

            if key == 27:  # ESC
                running = False
            elif key == curses.KEY_DOWN:
                if current_line < len(editor_content) - 1:
                    current_line += 1
                    current_col = min(current_col, len(editor_content[current_line]))
            elif key == curses.KEY_UP:
                if current_line > 0:
                    current_line -= 1
                    current_col = min(current_col, len(editor_content[current_line]))
            elif key == curses.KEY_RIGHT:
                if current_col < len(editor_content[current_line]):
                    current_col += 1
            elif key == curses.KEY_LEFT:
                if current_col > 0:
                    current_col -= 1
            elif key == 10:  # Enter
                editor_content.insert(current_line + 1, "")
                current_line += 1
                current_col = 0
            elif key == 127:  # Backspace
                if current_col > 0:
                    line = editor_content[current_line]
                    editor_content[current_line] = line[:current_col - 1] + line[current_col:]
                    current_col -= 1
            elif key == curses.KEY_DC:  # Delete
                if current_col < len(editor_content[current_line]):
                    line = editor_content[current_line]
                    editor_content[current_line] = line[:current_col] + line[current_col + 1:]
            elif key == 9:  # Tab
                editor_content[current_line] = editor_content[current_line][:current_col] + "    " + editor_content[current_line][current_col:]
                current_col += 4
            elif key == 337:  # F2
                run_code()
            elif key == 338:  # F3
                save_file()
            elif 32 <= key <= 126:  # Printable characters
                line = editor_content[current_line]
                editor_content[current_line] = line[:current_col] + chr(key) + line[current_col:]
                current_col += 1

    curses.wrapper(run_ide)

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    selection = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Selecione um arquivo para editar (ENTER) - ESC para sair")
        files = get_files()
        if not files:
            stdscr.addstr(2, 2, "Nenhum arquivo encontrado.")
            stdscr.refresh()
            stdscr.getch()
            return

        for i, name in enumerate(files):
            if i == selection:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(i + 2, 2, name)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(i + 2, 2, name)

        key = stdscr.getch()

        if key == curses.KEY_UP and selection > 0:
            selection -= 1
        elif key == curses.KEY_DOWN and selection < len(files) - 1:
            selection += 1
        elif key in [10, 13]:  # Enter
            file_path = files[selection]
            call_editor(file_path)
            stdscr.clear()
        elif key == 27:  # ESC
            break

# Inicia o programa
curses.wrapper(main_menu)
