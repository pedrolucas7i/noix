# Noix CLI IDE

Noix CLI IDE é um editor de código interativo baseado em terminal, que oferece recursos essenciais para edição de código e execução de programas em diversas linguagens. Ele suporta múltiplos arquivos abertos, realce de sintaxe e execução de código diretamente do ambiente de desenvolvimento.

## Funcionalidades

- **Edição de código com realce de sintaxe:** Suporta diversas linguagens de programação como Python, JavaScript, Java, C, C++, Ruby, PHP, Go, Swift, Kotlin, entre outras.
- **Abertura e criação de arquivos:** É possível criar novos arquivos ou abrir arquivos existentes diretamente do terminal.
- **Navegação por arquivos:** Navegue facilmente entre os arquivos abertos utilizando abas.
- **Edição de código:** Edite seu código com comandos de navegação e modificação padrão de editores de texto (setas, backspace, delete, enter).
- **Execução de código:** Execute código Python diretamente no editor.
- **Salvamento de arquivos:** Salve suas alterações com facilidade.
- **Sistema de atalho de teclado:** Utilize atalhos como `Ctrl+S` para salvar, `F2` para executar, e `F4` para abrir novos arquivos.

## Instalação

Para usar a Noix CLI IDE, basta ter o Python 3 instalado em seu sistema. O código não possui dependências externas, além da biblioteca `curses`, que já vem instalada com a maioria das distribuições do Python.

### Passos para execução:

1. **Clone o repositório** (ou baixe o arquivo):

```bash
git clone https://github.com/seu_usuario/noix-cli-ide.git
```

2. **Execute o editor**:

```bash
python3 main.py
```

## Navegação

- **Setas para cima e para baixo:** Navegue entre os arquivos ou entre linhas no editor.
- **Setas para a esquerda e direita:** Mova o cursor horizontalmente na linha.
- **Enter:** Adicione uma nova linha no arquivo.
- **Ctrl+S:** Salve o arquivo atual.
- **F2:** Execute o código Python no arquivo atual.
- **F3:** Salve o arquivo atual.
- **F4:** Abra um novo arquivo existente.
- **F5:** Feche o arquivo atual.
- **Esc:** Feche o editor ou menu.

## Como utilizar

### Abrir um arquivo

- Ao iniciar a Noix CLI IDE, você verá uma lista de arquivos disponíveis no diretório atual. Use as setas para navegar entre os arquivos e pressione `Enter` para abrir o arquivo desejado.

### Criar um novo arquivo

- Pressione `n` para criar um novo arquivo. Digite o nome do arquivo e o editor será iniciado para edição.

### Edição de código

- Navegue pelas linhas e edite o conteúdo do arquivo.
- O realce de sintaxe irá destacar palavras-chave de acordo com a linguagem detectada pelo arquivo.

### Execução de código

- Para executar o código Python, pressione `F2`. O resultado da execução será mostrado na parte superior do terminal.

### Salvar

- Para salvar as alterações, pressione `Ctrl+S` ou `F3`.

### Fechar arquivos

- Para fechar um arquivo, pressione `F5`. Se houver mais de um arquivo aberto, você será levado automaticamente ao próximo arquivo aberto.

## Suporte a Linguagens

A Noix CLI IDE suporta o realce de sintaxe para várias linguagens de programação, incluindo:

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

### Arquivos Suportados

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

## Contribuições

Se você deseja contribuir com melhorias para o Noix CLI IDE, fique à vontade para abrir um pull request ou enviar uma issue no repositório.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Sinta-se à vontade para editar e modificar o Noix CLI IDE conforme suas necessidades!