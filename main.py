import subprocess
from prompt_toolkit.shortcuts import radiolist_dialog

def get_files():
	resultado = subprocess.run(["ls", "-a"], capture_output=True, text=True)

	if resultado.returncode == 0:
	    files = resultado.stdout.strip().split('\n')
	    files = [f for f in files if f not in ('.', '..')]
	    print(files)
	    return files
	else:
	    print("Erro ao executar ls -a")


def displayChooseFile(files):
	result = radiolist_dialog(
		title="Choose the file:",
		values=[files]
).run()

displayChooseFile(get_files())
