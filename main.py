# std
from time import sleep
# interno
from src.util import *
from src.tipos import *
from src.logger import *
from src.windows import *
from src.navegador import *
from src.planilhas import *

CAMINHO_EXCEL = rf"{ info_stack().caminho }\documentos\DADOS LANÇAMENTOS.xlsx"
SITE_EBS = "https://o2qa.odebrecht.com"
USUARIO = "dclick"
SENHA = "senha123"

def abrir_ordens_de_servico (navegador: Navegador):
    """Abrir a aba das Ordens de Serviço"""
    Logger.informar("Abrindo a aba das Ordens de Serviço")
    # Clicar em 'Ordens de Serviço'
    elemento = navegador.encontrar("css selector", Localizadores.aba_ordens_servico.value)
    assert elemento != None, "Elemento 'Ordens de Serviço' não localizado"
    elemento.click()
    # Aguardar carregar
    elemento = navegador.encontrar("css selector", Localizadores.input_ordem_servico.value)
    assert elemento != None, "Elemento 'Ordem de Serviço' não localizado"
    Logger.informar("Aba 'Ordens de Serviço' aberta")

def abrir_organizacao (navegador: Navegador, organizacao: str):
    """Selecionar a organização informada e clicar em `Ir`"""
    Logger.informar(f"Abrindo a organização '{organizacao}'")
    # Criando o seletor que será manipulado
    elemento = navegador.encontrar("css selector", Localizadores.organizacao.value)
    seletor = navegador.seletor(elemento)
    # Verificar se existe a opção
    opcoes = [ elemento.text.lower() for elemento in seletor.options ]
    assert organizacao.lower() in opcoes, f"Organização '{organizacao}' não encontrada nas opções '{opcoes}'"
    
    # BUG - Não compatível com o IE
    # texto = [ opcao.text for opcao in seletor.options if opcao.text.lower() == organizacao.lower() ][0]
    # seletor.select_by_visible_text(texto)
    
    # Selecionar opção 
    index = [ index for index, opcao in enumerate(seletor.options) if opcao.text.lower() == organizacao.lower() ][0]
    elemento.click()
    for _ in range(index): Windows.atalho(["down"])
    Windows.atalho(["enter"])
    
    # `Ir`
    elemento = navegador.encontrar("css selector", Localizadores.ir.value)
    assert elemento != None, f"Elemento 'Ir' não localizado"
    elemento.click()
    Logger.informar(f"Organização '{organizacao}' aberta")

def abrir_gerenciamento_ativo (navegador: Navegador):
    """Clicar em `AUTOMACAO DCLICK`, `Início` e esperar o refresh"""
    Logger.informar("Abrindo o Gerenciamento de Ativo")
    # aba "AUTOMACAO DCLICK"
    elemento = navegador.encontrar("css selector", Localizadores.navegacao_dclick.value)
    assert elemento != None, "Navegação 'AUTOMACAO DCLICK' não encontrada"
    elemento.click()
    # elemento "Início"
    elemento = navegador.encontrar("css selector", Localizadores.inicio.value)
    assert elemento != None, "Elemento 'Início' não encontrado"
    elemento.click()
    # aguardar a "Organização" carregar
    elemento = navegador.encontrar("css selector", Localizadores.organizacao.value)
    assert elemento != None, "Elemento 'Organização' não encontrado"
    Logger.informar(f"Gerenciamento de Ativo aberto")

def efetuar_login (navegador: Navegador):
    """Efetuar o login no `SITE_EBS` e esperar a página Home carregar"""
    Logger.informar("Efetuando o login")
    navegador.pesquisar(SITE_EBS)
    navegador.aguardar(
        lambda: Localizadores.texto_login.value.lower() in navegador.driver.title.lower(), 
        f"Texto '{ Localizadores.texto_login.value }' não encontrado no título do navegador"
    )
    # usuario
    elemento = navegador.encontrar("css selector", Localizadores.usuario.value)
    assert elemento != None, "Campo do usuario não encontrado"
    elemento.send_keys(USUARIO)
    # senha
    elemento = navegador.encontrar("css selector", Localizadores.senha.value)
    assert elemento != None, "Campo de senha não encontrado"
    elemento.send_keys(SENHA)
    # efetuar login
    elemento = navegador.encontrar("css selector", Localizadores.efetuar_login.value)
    assert elemento != None, "Botão para efetuar login não encontrado"
    elemento.click()
    # aguardar a pagina 'Home' carregar
    navegador.aguardar(
        lambda: Localizadores.texto_home.value.lower() in navegador.titulo.lower(), 
        f"Texto '{ Localizadores.texto_home.value }' não encontrado no título do navegador"
    )
    Logger.informar("Login efetuado e Home Page carregada")

def main():
    """Fluxo principal"""
    dadosLancamentos = parse_dados_lancamentos(CAMINHO_EXCEL)
    print(dadosLancamentos[0])

    try:
        # abrir navegador no modo Internet Explorer
        with Navegador() as navegador:
            # maximizar janela do navegador
            # efetuar login no `SITE_EBS`
            janelaNavegador = Windows.janela_focada()
            janelaNavegador.maximizar()
            efetuar_login(navegador)
            
            # abrir a automação dclick, gerenciamento ativo e aguardar o refresh
            abrir_gerenciamento_ativo(navegador)

            # abrir a organização presente no `dadosLancamentos`
            # abrir as ordens de serviço da organização
            abrir_organizacao(navegador, "ACN") # TODO - Pegar da planilha a organização
            abrir_ordens_de_servico(navegador)

            sleep(5)
    
    except (TimeoutException, TimeoutError) as erro:
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