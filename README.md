
---

# Noix CLI IDE

Noix CLI IDE is a terminal-based interactive code editor that offers essential features for code editing and running programs in various languages. It supports multiple open files, syntax highlighting, and code execution directly from the development environment.

## Features

- **Code editing with syntax highlighting:** Supports several programming languages such as Python, JavaScript, Java, C, C++, Ruby, PHP, Go, Swift, Kotlin, among others.
- **Opening and creating files:** You can create new files or open existing ones directly from the terminal.
- **File navigation:** Easily switch between open files using tabs.
- **Code editing:** Edit your code using standard text editor navigation and modification commands (arrows, backspace, delete, enter).
- **Code execution:** Run Python code directly from the editor.
- **File saving:** Save your changes effortlessly.
- **Keyboard shortcut system:** Use shortcuts like `Ctrl+S` to save, `F2` to run, and `F4` to open new files.

## Installation

To use Noix CLI IDE, all you need is Python 3 installed on your system. The code has no external dependencies other than the `curses` library, which comes pre-installed with most Python distributions.

### Steps to run:

1. **Clone the repository** (or download the file):

```bash
git clone https://github.com/pedrolucas7i/noix.git
```

2. **Run the editor**:

```bash
python3 main.py
```

## Navigation

- **Up and down arrows:** Navigate between files or between lines in the editor.
- **Left and right arrows:** Move the cursor horizontally on the line.
- **Enter:** Add a new line in the file.
- **Ctrl+S:** Save the current file.
- **F2:** Run the Python code in the current file.
- **F3:** Save the current file.
- **F4:** Open an existing file.
- **F5:** Close the current file.
- **Esc:** Exit the editor or menu.

## How to Use

### Open a File

- When you launch Noix CLI IDE, you’ll see a list of available files in the current directory. Use the arrow keys to navigate and press `Enter` to open the desired file.

### Create a New File

- Press `n` to create a new file. Type the file name, and the editor will open for editing.

### Code Editing

- Navigate through the lines and edit the file’s content.
- Syntax highlighting will highlight keywords based on the language detected by the file extension.

### Code Execution

- To run Python code, press `F2`. The execution result will appear at the top of the terminal.

### Saving

- To save changes, press `Ctrl+S` or `F3`.

### Closing Files

- To close a file, press `F5`. If multiple files are open, you’ll be taken to the next open file automatically.

## Language Support

Noix CLI IDE supports syntax highlighting for several programming languages, including:

- Python  
- JavaScript  
- Java  
- C  
- C++  
- Ruby  
- PHP  
- Go  
- Swift  
- Kotlin  
- Scala  
- R  
- Haskell  
- SQL  
- Bash  
- Rust  
- TypeScript  

### Supported File Extensions

- **.py:** Python  
- **.js:** JavaScript  
- **.java:** Java  
- **.c:** C  
- **.cpp:** C++  
- **.rb:** Ruby  
- **.php:** PHP  
- **.pl:** Perl  
- **.go:** Go  
- **.swift:** Swift  
- **.kt:** Kotlin  
- **.scala:** Scala  
- **.r:** R  
- **.hs:** Haskell  
- **.sql:** SQL  
- **.sh:** Bash  
- **.rs:** Rust  
- **.ts:** TypeScript  

## Contributions

If you'd like to contribute improvements to Noix CLI IDE, feel free to open a pull request or submit an issue on the repository.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

Feel free to edit and modify Noix CLI IDE to suit your needs!
