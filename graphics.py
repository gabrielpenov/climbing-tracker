import matplotlib.pyplot as plt
from models import Usuario, Expedicao


class Graficos:
    def __init__(self, usuario: Usuario):
        self.usuario = usuario

    def gerar_grafico_niveis(self):
        """Gráfico de barras com vias completadas por nível"""
        niveis = ["V0", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9"]
        contagem = {nivel: 0 for nivel in niveis}

        for expedicao in self.usuario.expedicoes:
            for treino in expedicao.treinos:
                for tentativa in treino.tentativas:
                    if tentativa.completou and tentativa.nivel in contagem:
                        contagem[tentativa.nivel] += 1

        valores = [contagem[n] for n in niveis]

        plt.figure(figsize=(10, 6))
        plt.bar(niveis, valores, color='steelblue')
        plt.xlabel("Nível")
        plt.ylabel("Vias Completadas")
        plt.title(f"Progresso de {self.usuario.nome} — Vias por Nível")
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    def gerar_grafico_score_tempo(self):
        """Gráfico de linha com score acumulado ao longo dos treinos"""
        datas = []
        scores_acumulados = []
        score_total = 0

        for expedicao in self.usuario.expedicoes:
            for treino in expedicao.treinos:
                score_dia = min(treino.calcular_score_total(), Expedicao.LIMITE_DIARIO)
                score_total += score_dia
                datas.append(treino.data)
                scores_acumulados.append(score_total)

        if not datas:
            print("Sem dados suficientes pra gerar o gráfico.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(datas, scores_acumulados, marker='o', linewidth=2, markersize=8, color='green')
        plt.xlabel("Data")
        plt.ylabel("Score Acumulado")
        plt.title(f"Evolução de {self.usuario.nome} ao Longo do Tempo")
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    def gerar_grafico_expedicao_atual(self):
        """Gráfico de progresso da expedição atual"""
        expedicao = self.usuario.expedicao_atual()

        if not expedicao:
            print("Nenhuma expedição ativa.")
            return

        meta = expedicao.meta_pontos
        score = expedicao.calcular_score_total()
        faltante = max(0, meta - score)
        info = Expedicao.METAS[expedicao.dificuldade]

        plt.figure(figsize=(8, 4))
        plt.barh(["Progresso"], [score], color='orange', label=f"Conquistado ({score} pts)")
        plt.barh(["Progresso"], [faltante], left=[score], color='lightgray', label=f"Faltante ({faltante} pts)")
        plt.xlabel("Pontos")
        plt.title(f"Expedição {info['nome']} — Meta: {meta} pontos")
        plt.legend()
        plt.xlim(0, meta * 1.1)
        plt.tight_layout()
        plt.show()
