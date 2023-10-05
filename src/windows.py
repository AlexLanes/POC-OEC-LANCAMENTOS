# std
from os import system
from time import sleep, time
from dataclasses import dataclass
from typing import overload, Literal, Callable
# interno
from src.util import *
# externo
import pyautogui as AutoGui
from pygetwindow import Win32Window
from pynput.keyboard import Controller

Teclado = Controller()
AutoGui.FAILSAFE = True
MOUSE = Literal["left", "middle", "right"]
PORCENTAGENS = Literal["0.9", "0.8", "0.7", "0.6", "0.5", "0.4", "0.3", "0.2", "0.1"]
TECLAS = Literal['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']

@dataclass
class Coordenada:
    x: int
    y: int
    comprimento: int
    altura: int

    def __iter__(self):
        """Utilizar com o tuple()"""
        yield self.x
        yield self.y
        yield self.comprimento
        yield self.altura
    
    @overload
    def transformar(self) -> tuple[int, int]:
        """Transformar as cordenadas para a posição (x, y) central horizontalmente e verticalmente"""
    @overload
    def transformar(self, xOffset: float, yOffset: float) -> tuple[int, int]:
        """Transformar as cordenadas para a posição (x, y) de acordo com a porcentagem xOffset e yOffset.\n
        `xOffset` (esquerda, centro, direita) = (0, 0.5, 1)\n
        `yOffset` (topo, centro, baixo) = (0, 0.5, 1)"""
    def transformar(self, xOffset=0.5, yOffset=0.5) -> tuple[int, int]:
        # enforça o range entre 0.0 e 1.0
        xOffset, yOffset = max(0.0, min(1.0, xOffset)), max(0.0, min(1.0, yOffset))
        return ( 
            self.x + int(self.comprimento * xOffset), 
            self.y + int(self.altura * yOffset) 
        )

    def __len__(self):
        return 4

def obter_x_y(coordenada: tuple[int, int] | Coordenada) -> tuple[int|None, int|None]:
    """Obter coordenada (x, y) do item recebido"""
    x = y = None
    if isinstance(coordenada, tuple): 
        x, y = coordenada
    elif isinstance(coordenada, Coordenada):
        x, y = coordenada.transformar()
    return (x, y)

@dataclass
class Janela:
    janela: Win32Window
    def titulo(self) -> str:
        """Titulo da janela"""
        return self.janela.title
    def maximizar(self) -> None:
        """Maximizar janela"""
        self.janela.maximize()
    def maximizado(self) -> bool:
        """Checar se a janela está maximizada"""
        self.janela.isMaximized
    def minimizar(self) -> None:
        """Minimizar janela"""
        self.janela.minimize()
    def minimizado(self) -> bool:
        """Checar se a janela está minimizada"""
        self.janela.isMinimized
    def fechar(self) -> None:
        """Fechar janela"""
        self.janela.close()
    def focado(self) -> bool:
        """Checar se a janela está focada"""
        return self.janela.isActive
    def focar(self) -> None:
        """Focar a janela minimizando e maximizando"""
        if not self.focado():
            self.minimizar()
            self.maximizar()

class Windows:
    @staticmethod
    def procurar_imagem(caminhoImagem: str, porcentagemConfianca: PORCENTAGENS = "0.9", segundosProcura=0, regiao: Coordenada = None, cinza=False) -> Coordenada | None:
        """Procurar imagem na tela com `porcentagemConfianca`% de confiança na procura durante `segundosProcura` segundos na `regiao` da tela informada.\n
        - `segundosProcura` vazio para procurar 1 vez apenas\n
        - `regiao` vazia para procurar na tela inteira
        - `cinza` = True para comparar ambas imagem como grayscale"""
        box = AutoGui.locateOnScreen(
            image=caminhoImagem, 
            minSearchTime=segundosProcura,
            confidence=porcentagemConfianca,
            region=tuple(regiao) if regiao else None,
            grayscale=cinza
        )
        return Coordenada(box.left, box.top, box.width, box.height) if box else None
        
    @staticmethod
    def capturar_imagem(caminhoImagem: str = None, regiao: Coordenada = None, cinza=False) -> None:
        """Realizar uma captura de tela na `regiao` informada da tela e salvar no caminho/nome.formato informado no `caminhoImagem`. \n
        - `caminhoImagem` vazio para não salvar e apenas abrir a imagem capturada\n
        - `regiao` vazia para capturar a tela inteira\n
        - `cinza` = True para transformar a imagem para o formato grayscale"""
        imagem = AutoGui.screenshot(region=tuple(regiao) if regiao else None)
        imagem = imagem.convert("L") if cinza else imagem
        if caminhoImagem: imagem.save(caminhoImagem)
        else: imagem.show()

    @staticmethod
    def titulos_janelas() -> list[str]:
        """Listar os titulos das janelas abertas"""
        return [ titulo for titulo in AutoGui.getAllTitles() if titulo != "" ]

    @staticmethod
    def titulo_janela_focada() -> str:
        """Obter o titulo da janela em foque"""
        return AutoGui.getActiveWindowTitle()
    
    @staticmethod
    def janela_focada() -> Janela:
        """Obter a janela focada"""
        janela: Win32Window = AutoGui.getActiveWindow()
        return Janela(janela)
    
    @staticmethod
    def buscar_janela(titulo: str) -> Janela | None:
        """Obter a primeira janela que possua o `titulo`"""
        janelas: list[Win32Window] = AutoGui.getAllWindows()
        for janela in janelas:
            if normalizar(titulo) in normalizar(janela.title): return Janela(janela)

    @staticmethod
    def aguardar(condicao: Callable[[], bool], mensagemErro: str, timeout=30) -> None | TimeoutError:
        """Repetir a função `condicao` até que retorne `True` ou `TimeoutError` após `timeout` segundos informando a `mensagemErro`"""
        inicio = time()
        while time() - inicio < timeout:
            if condicao(): return
            else: sleep(0.25)
        raise TimeoutError(mensagemErro)

    @staticmethod
    def cmd(comando: str) -> None | Exception:
        """Realizar um comando no `prompt`.
        - Levar em consideração o diretório de execução atual
        - Lança exceção se o comando for inválido"""
        system(comando)
    
    @staticmethod
    def mover_mouse(coordenada: tuple[int, int] | Coordenada) -> None:
        """Mover o mouse até as cordenadas"""
        x, y = obter_x_y(coordenada)
        AutoGui.moveTo(x, y)
    
    @overload
    @staticmethod
    def clicar_mouse() -> None:
        """Clicar com o botão esquerdo do mouse 1 vez na posição atual"""
    @overload
    @staticmethod
    def clicar_mouse(coordenada: Coordenada | tuple[int, int]) -> None:
        """Clicar com o botão esquerdo do mouse 1 vez nas `coordenada`"""
    @overload
    @staticmethod
    def clicar_mouse(coordenada: Coordenada | tuple[int, int], botao: MOUSE, quantidade=1) -> None:
        """Clicar com o botão `botao` do mouse `quantidade` vez(es) nas `coordenada`"""
    def clicar_mouse(coordenada: Coordenada | tuple[int, int] = None, botao="left", quantidade=1) -> None:
        x, y = obter_x_y(coordenada)
        AutoGui.click(x, y, quantidade, 0.25, botao)
    
    @staticmethod
    def scroll_mouse(quantidade: int, direcao: Literal["cima", "baixo"]) -> None:
        """Realizar o scroll `quantidade` vezes no sentido `direcao` na posição atual do mouse"""
        quantidade = min(0, quantidade)
        for _ in range(quantidade): 
            AutoGui.scroll(-1 if direcao == "baixo" else 1)
    
    @staticmethod
    def rgb_mouse() -> tuple[int, int, int]:
        """Obter o RGB da coordenada atual do mouse"""
        return AutoGui.pixel( *AutoGui.position() )
    
    @staticmethod
    def atalho(teclas: list[TECLAS]) -> None:
        """Apertar as teclas sequencialmente e depois soltá-las em ordem reversa"""
        AutoGui.hotkey(teclas, interval=0.25)
    
    @staticmethod
    def digitar(texto: str) -> None:
        """Digitar o texto pressionando cada tecla do texto e soltando em seguida"""
        Teclado.type(texto) 

__all__ = [
    "Janela",
    "Windows",
    "AutoGui",
    "Coordenada"
]
