import curses
import subprocess
import os
import re

# Expressão regular para identificar palavras-chave do Python
PYTHON_KEYWORDS = r'\b(def|import|for|while|if|else|elif|return|class|try|except|finally|with|as|pass|break|continue|lambda|yield|from|global|nonlocal|assert|del|raise)\b'

def get_files():
    resultado = subprocess.run(["ls", "-a"], capture_output=True, text=True)
    if resultado.returncode == 0:
        files = resultado.stdout.strip().split('\n')
        return [f for f in files if f not in ('.', '..')]
    else:
        return []

def load_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.rstrip('\n') for line in f.readlines()]
    except FileNotFoundError:
        return [""]

def save_file_content(file_path, editor_content):
    with open(file_path, 'w') as f:
        f.write("\n".join(editor_content))

def open_file_selection(stdscr):
    # Menu simples para seleção de arquivo
    selection = 0
    files = get_files()
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Selecione um arquivo para abrir (ENTER) - ESC para cancelar")
        if not files:
            stdscr.addstr(2, 2, "Nenhum arquivo encontrado.")
            stdscr.refresh()
            stdscr.getch()
            return None
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
        elif key in [10, 13]:
            return files[selection]
        elif key == 27:
            return None

def call_editor(initial_file):
    def run_ide(stdscr):
        # Inicialização das cores para realce de sintaxe e barra de abas
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_YELLOW, -1)  # Realce para palavras-chave
        curses.init_pair(2, curses.COLOR_CYAN, -1)    # Destaque para a aba ativa

        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()

        # Lista de arquivos abertos – cada item é um dicionário com o conteúdo, caminho e posição do cursor
        open_files = []
        open_files.append({
            "file_path": initial_file,
            "editor_content": load_file(initial_file),
            "cursor_line": 0,
            "cursor_col": 0
        })
        active_file = 0
        scroll_offset = 0

        def syntax_highlight(line):
            """Divide a linha em segmentos com ou sem realce."""
            segments = []
            last_index = 0
            for match in re.finditer(PYTHON_KEYWORDS, line):
                start, end = match.span()
                if start > last_index:
                    segments.append((line[last_index:start], curses.A_NORMAL))
                segments.append((line[start:end], curses.color_pair(1)))
                last_index = end
            if last_index < len(line):
                segments.append((line[last_index:], curses.A_NORMAL))
            return segments

        def render_tabs():
            stdscr.move(0, 0)
            stdscr.clrtoeol()
            tab_str = ""
            for idx, f in enumerate(open_files):
                name = f["file_path"]
                if idx == active_file:
                    tab_str += f" [{name}] "
                else:
                    tab_str += f"  {name}  "
            stdscr.addstr(0, 0, tab_str, curses.color_pair(2))

        def render_editor():
            nonlocal scroll_offset
            stdscr.clear()
            render_tabs()
            height, width = stdscr.getmaxyx()
            current_file = open_files[active_file]
            editor_content = current_file["editor_content"]
            cursor_line = current_file["cursor_line"]
            cursor_col = current_file["cursor_col"]

            # Barra de status na última linha
            status_bar = ("F2: Executar | F3: Salvar | F4: Abrir arquivo | "
                          "F5: Fechar arquivo | Ctrl+S: Salvar | Ctrl+Q: Sair")
            stdscr.addstr(height - 1, 0, status_bar[:width-1])

            # Renderização das linhas (da linha 1 até a penúltima)
            for i in range(1, height - 1):
                line_index = i - 1 + scroll_offset
                if line_index < len(editor_content):
                    line = editor_content[line_index]
                    x = 0
                    for segment, attr in syntax_highlight(line):
                        try:
                            stdscr.addstr(i, x, segment[:width - x], attr)
                        except curses.error:
                            pass
                        x += len(segment)
            # Ajusta o scroll se o cursor sair da área visível
            if cursor_line < scroll_offset:
                new_scroll = cursor_line
            elif cursor_line >= scroll_offset + height - 2:
                new_scroll = cursor_line - (height - 3)
            else:
                new_scroll = scroll_offset
            scroll_offset = new_scroll

            # Move o cursor para a posição correta na tela
            disp_line = current_file["cursor_line"] - scroll_offset + 1
            disp_col = current_file["cursor_col"]
            stdscr.move(disp_line, disp_col)
            stdscr.refresh()

        def run_code():
            current_file = open_files[active_file]
            code = "\n".join(current_file["editor_content"])
            try:
                result = subprocess.run(['python3', '-c', code], capture_output=True, text=True)
                output = result.stdout + result.stderr
            except Exception as e:
                output = str(e)

            stdscr.clear()
            stdscr.addstr(0, 0, "Resultado da execução (pressione qualquer tecla para voltar):")
            lines = output.splitlines()
            height, width = stdscr.getmaxyx()
            for i, line in enumerate(lines[:height - 2]):
                try:
                    stdscr.addstr(i + 2, 0, line[:width - 1])
                except curses.error:
                    pass
            stdscr.refresh()
            stdscr.getch()

        def save_current_file():
            current_file = open_files[active_file]
            save_file_content(current_file["file_path"], current_file["editor_content"])
            height, width = stdscr.getmaxyx()
            msg = f"Arquivo {current_file['file_path']} salvo com sucesso! Pressione qualquer tecla..."
            stdscr.addstr(height - 1, 0, msg[:width-1])
            stdscr.refresh()
            stdscr.getch()

        running = True
        while running:
            render_editor()
            key = stdscr.getch()
            current_file = open_files[active_file]

            # ESC ou Ctrl+Q para sair
            if key == 27 or key == (ord('q') & 0x1f):
                running = False
            # Ctrl+S para salvar
            elif key == (ord('s') & 0x1f):
                save_current_file()
            elif key == curses.KEY_DOWN:
                if current_file["cursor_line"] < len(current_file["editor_content"]) - 1:
                    current_file["cursor_line"] += 1
                    current_file["cursor_col"] = min(
                        current_file["cursor_col"],
                        len(current_file["editor_content"][current_file["cursor_line"]])
                    )
            elif key == curses.KEY_UP:
                if current_file["cursor_line"] > 0:
                    current_file["cursor_line"] -= 1
                    current_file["cursor_col"] = min(
                        current_file["cursor_col"],
                        len(current_file["editor_content"][current_file["cursor_line"]])
                    )
            elif key == curses.KEY_RIGHT:
                if current_file["cursor_col"] < len(current_file["editor_content"][current_file["cursor_line"]]):
                    current_file["cursor_col"] += 1
            elif key == curses.KEY_LEFT:
                if current_file["cursor_col"] > 0:
                    current_file["cursor_col"] -= 1
            elif key == 10:  # Enter
                line = current_file["editor_content"][current_file["cursor_line"]]
                before = line[:current_file["cursor_col"]]
                after = line[current_file["cursor_col"]:]
                current_file["editor_content"][current_file["cursor_line"]] = before
                current_file["editor_content"].insert(current_file["cursor_line"] + 1, after)
                current_file["cursor_line"] += 1
                current_file["cursor_col"] = 0
            elif key in (8, 127):  # Backspace
                if current_file["cursor_col"] > 0:
                    line = current_file["editor_content"][current_file["cursor_line"]]
                    current_file["editor_content"][current_file["cursor_line"]] = (
                        line[:current_file["cursor_col"] - 1] + line[current_file["cursor_col"]:]
                    )
                    current_file["cursor_col"] -= 1
                elif current_file["cursor_line"] > 0:
                    prev_line = current_file["editor_content"][current_file["cursor_line"] - 1]
                    curr_line_text = current_file["editor_content"].pop(current_file["cursor_line"])
                    current_file["cursor_line"] -= 1
                    current_file["cursor_col"] = len(prev_line)
                    current_file["editor_content"][current_file["cursor_line"]] = prev_line + curr_line_text
            elif key == curses.KEY_DC:  # Delete
                line = current_file["editor_content"][current_file["cursor_line"]]
                if current_file["cursor_col"] < len(line):
                    current_file["editor_content"][current_file["cursor_line"]] = (
                        line[:current_file["cursor_col"]] + line[current_file["cursor_col"]+1:]
                    )
                elif current_file["cursor_line"] < len(current_file["editor_content"]) - 1:
                    current_file["editor_content"][current_file["cursor_line"]] += current_file["editor_content"].pop(current_file["cursor_line"]+1)
            elif key == 9:  # Tab
                line = current_file["editor_content"][current_file["cursor_line"]]
                current_file["editor_content"][current_file["cursor_line"]] = (
                    line[:current_file["cursor_col"]] + "    " + line[current_file["cursor_col"]:]
                )
                current_file["cursor_col"] += 4
            elif key == curses.KEY_F2:
                run_code()
            elif key == curses.KEY_F3:
                save_current_file()
            elif key == curses.KEY_F4:
                # Abre um novo arquivo e adiciona como aba
                new_file = open_file_selection(stdscr)
                if new_file:
                    open_files.append({
                        "file_path": new_file,
                        "editor_content": load_file(new_file),
                        "cursor_line": 0,
                        "cursor_col": 0
                    })
                    active_file = len(open_files) - 1
            elif key == curses.KEY_F5:
                # Fecha a aba atual se houver mais de uma aberta
                if len(open_files) > 1:
                    open_files.pop(active_file)
                    active_file = max(0, active_file - 1)
            elif 32 <= key <= 126:
                line = current_file["editor_content"][current_file["cursor_line"]]
                current_file["editor_content"][current_file["cursor_line"]] = (
                    line[:current_file["cursor_col"]] + chr(key) + line[current_file["cursor_col"]:]
                )
                current_file["cursor_col"] += 1

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
        elif key in [10, 13]:
            file_path = files[selection]
            call_editor(file_path)
            stdscr.clear()
        elif key == 27:
            break

# Inicia o programa
curses.wrapper(main_menu)
