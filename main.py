# std
from time import sleep
# interno
from src.util import *
from src.logger import *
from src.windows import *

def main():
    """Fluxo principal"""
    try:
        pass
    
    except (TimeoutError) as erro:
        Logger.erro(f"Erro de timeout na espera de alguma condição/elemento/janela: { erro }")
        exit(1)
    except AssertionError as erro:
        Logger.erro(f"Erro de validação pré-execução de algum passo no fluxo: { erro }")
        exit(1)
    except Exception as erro:
        Logger.erro(f"Erro inesperado no fluxo: { erro }")
        exit(1)
    
if __name__ == "__main__":
    Logger.informar("### Iniciado execução do fluxo ###")
    main()
    Logger.informar("### Finalizado execução com sucesso ###")