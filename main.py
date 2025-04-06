import subprocess
import curses
import os

def main(stdscr):
	curses.curs_set(0)
	stdscr.clear()
	stdscr.refresh()
	selection = 0
	while True:
		stdscr.clear()
		stdscr.addstr(0, 0, "  " + os.path.basename(os.getcwd()))
		files = get_files()
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
		elif key in [curses.KEY_ENTER, 10, 13]:
			stdscr.addstr(len(files) + 4, 0, f"Selected: {files[selection]}")
			stdscr.getch()
			call_nano(files[selection])
			break

def get_files():
	resultado = subprocess.run(["ls", "-a"], capture_output=True, text=True)

	if resultado.returncode == 0:
	    files = resultado.stdout.strip().split('\n')
	    files = [f for f in files if f not in ('.', '..')]
	    print(files)
	    return files
	else:
	    print("Erro ao executar ls -a")


def call_nano(file):
	subprocess.call(["nano", file])

curses.wrapper(main)