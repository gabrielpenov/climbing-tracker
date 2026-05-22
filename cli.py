from datetime import date
from models import Usuario, Expedicao
from storage import Storage
from graphics import Graficos

storage = Storage()

NIVEIS_BOULDER = ["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"]


def exibir_montanha(progresso: float):
    altura = int(progresso / 10)
    print(f"\n🧗 Montanha: [{('█' * altura).ljust(10, '░')}] {progresso:.1f}%\n")


def escolher_dificuldade(usuario: Usuario) -> str:
    print("\n🏔️  NOVA EXPEDIÇÃO — Qual montanha você quer escalar?\n")
    opcoes = []
    for nivel in usuario.niveis_desbloqueados:
        info = Expedicao.METAS[nivel]
        opcoes.append(nivel)
        print(f"  {len(opcoes)} - {info['nome']} ({info['pontos']} pontos)")
    print()
    while True:
        try:
            escolha = int(input("Escolha: ")) - 1
            if 0 <= escolha < len(opcoes):
                return opcoes[escolha]
            print("Opção inválida.")
        except ValueError:
            print("Digite um número.")


def registrar_treino(usuario: Usuario):
    expedicao = usuario.expedicao_atual()
    if not expedicao:
        print("\nVocê não tem uma expedição ativa!")
        return

    hoje = str(date.today())
    treino = expedicao.adicionar_treino(hoje)

    print(f"\n📋 REGISTRANDO TREINO — {hoje}")
    print("Digite as vias que você fez. Digite 'fim' quando terminar.\n")

    while True:
        print("Níveis: V0 V1 V2 V3 V4 V5 V6 V7 V8 V9")
        nivel = input("Nível tentado (ou 'fim'): ").upper()

        if nivel == "FIM":
            break

        if nivel not in NIVEIS_BOULDER:
            print("Nível inválido.")
            continue

        completou = input(f"Completou o {nivel}? (s/n): ").lower() == "s"
        treino.adicionar_tentativa(nivel, completou)
        print(f"{'✅' if completou else '❌'} {nivel} registrado!\n")

    score_dia = min(treino.calcular_score_total(), Expedicao.LIMITE_DIARIO)
    print(f"\n💪 Treino finalizado! Score do dia: {score_dia} pontos")

    if expedicao.verificar_conclusao():
        print("\n🎉🎉🎉 PARABÉNS! Você chegou ao topo da montanha! 🎉🎉🎉")
        ordem = ["facil", "medio", "dificil", "impossivel", "lendario"]
        idx = ordem.index(expedicao.dificuldade)
        if idx + 1 < len(ordem):
            proximo = ordem[idx + 1]
            usuario.desbloquear_nivel(proximo)
            print(f"🔓 Nível '{Expedicao.METAS[proximo]['nome']}' desbloqueado!")


def ver_progresso(usuario: Usuario):
    expedicao = usuario.expedicao_atual()
    if not expedicao:
        print("\nNenhuma expedição ativa.")
        return

    info = Expedicao.METAS[expedicao.dificuldade]
    score = expedicao.calcular_score_total()
    progresso = expedicao.calcular_progresso()

    print(f"\n📊 PROGRESSO — Expedição {info['nome']}")
    print(f"Meta: {expedicao.meta_pontos} pontos")
    print(f"Score atual: {score} pontos")
    print(f"Faltam: {max(expedicao.meta_pontos - score, 0)} pontos")
    exibir_montanha(progresso)
    print(f"Expedições completas: {usuario.total_expedicoes_completas()}")


def menu_graficos(usuario: Usuario):
    graficos = Graficos(usuario)
    print("\n📈 GRÁFICOS\n")
    print("1 - Vias completadas por nível")
    print("2 - Score acumulado ao longo do tempo")
    print("3 - Progresso da expedição atual")
    print("4 - Voltar")

    opcao = input("\nEscolha: ").strip()

    if opcao == "1":
        graficos.gerar_grafico_niveis()
    elif opcao == "2":
        graficos.gerar_grafico_score_tempo()
    elif opcao == "3":
        graficos.gerar_grafico_expedicao_atual()


def menu_principal(usuario: Usuario):
    while True:
        expedicao = usuario.expedicao_atual()
        print(f"\n⛰️  CLIMBING TRACKER — Olá, {usuario.nome}!")

        if expedicao:
            info = Expedicao.METAS[expedicao.dificuldade]
            progresso = expedicao.calcular_progresso()
            print(f"Expedição atual: {info['nome']} — {progresso:.1f}% completo\n")
        else:
            print("Nenhuma expedição ativa.\n")

        print("1 - Registrar treino de hoje")
        print("2 - Ver progresso")
        print("3 - Ver gráficos")
        print("4 - Nova expedição")
        print("5 - Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            if not expedicao:
                print("\nInicie uma expedição primeiro!")
            else:
                registrar_treino(usuario)
                storage.salvar_usuario(usuario)

        elif opcao == "2":
            ver_progresso(usuario)

        elif opcao == "3":
            menu_graficos(usuario)

        elif opcao == "4":
            if expedicao and not expedicao.completada:
                confirmar = input("\nVocê tem uma expedição em andamento. Abandonar? (s/n): ").lower()
                if confirmar != "s":
                    continue
                expedicao.completada = True
            dificuldade = escolher_dificuldade(usuario)
            usuario.iniciar_expedicao(dificuldade)
            storage.salvar_usuario(usuario)
            print("\n🚀 Nova expedição iniciada! Boa sorte!")

        elif opcao == "5":
            print("\nAté a próxima, escalador! 🧗\n")
            break

        else:
            print("Opção inválida.")


def main():
    print("⛰️  BEM VINDO AO CLIMBING TRACKER!")
    usuario = storage.carregar_usuario()

    if usuario:
        print(f"\nBem vindo de volta, {usuario.nome}!")
    else:
        print("\nPrimeiro acesso! Como você se chama?")
        nome = input("Nome: ").strip()
        usuario = Usuario(nome)
        print(f"\nOlá, {nome}! Vamos começar sua primeira expedição.")
        dificuldade = escolher_dificuldade(usuario)
        usuario.iniciar_expedicao(dificuldade)
        storage.salvar_usuario(usuario)
        print("\n🚀 Expedição iniciada! Boa sorte na montanha!")

    menu_principal(usuario)


if __name__ == "__main__":
    main()
