# Academicozudo

Academicozudo é um software desenvolvido em Python e QT para facilitar a realização de funções no sistema acadêmico da FUNCERN.

### Dependências básicas:

- `Python >= 3.4`
- `pip`
- `Qt == 5.6`
- `PyQt == 5.6`


### Como preparar build:

Em primeiro lugar, é necessário realizar as seguintes operações:
- Instalar as dependências de bibliotecas `Python` via `pip`
- Gerar módulos PyQt através do `uic`
- Compilar módulos em linguagem nativa com o `Cython`

Para isso, execute a linha de comando abaixo:

`python setup.py build_ext --inplace`

### Como rodar:

`python main.py`


### Como distribuir:

`pyinstaller.exe --onefile --windowed main.py`

O executável compilado estará disponível na pasta `dist`