from datetime import datetime
from typing import List, Optional


class Tentativa:
    def __init__(self, nivel: str, completou: bool):
        self.nivel = nivel
        self.completou = completou
        self.data_hora = datetime.now()

    def calcular_score(self) -> int:
        scores = {
            "V0": 1,
            "V1": 2,
            "V2": 3,
            "V3": 4,
            "V4": 5,
            "V5": 6,
            "V6": 7,
            "V7": 8,
            "V8": 9,
            "V9": 10,
        }
        if self.completou:
            return scores.get(self.nivel, 0)
        else:
            return scores.get(self.nivel, 0) // 2


class Treino:
    def __init__(self, data: str):
        self.data = data
        self.tentativas: List[Tentativa] = []

    def adicionar_tentativa(self, nivel: str, completou: bool):
        tentativa = Tentativa(nivel, completou)
        self.tentativas.append(tentativa)

    def calcular_score_total(self) -> int:
        return sum(t.calcular_score() for t in self.tentativas)


class Expedicao:
    METAS = {
        "facil":       {"pontos": 100,  "nome": "Fácil",       "desbloqueada": True},
        "medio":       {"pontos": 300,  "nome": "Médio",       "desbloqueada": True},
        "dificil":     {"pontos": 500,  "nome": "Difícil",     "desbloqueada": True},
        "impossivel":  {"pontos": 800,  "nome": "Impossível",  "desbloqueada": False},
        "lendario":    {"pontos": 1200, "nome": "Lendário",    "desbloqueada": False},
    }
    LIMITE_DIARIO = 50

    def __init__(self, dificuldade: str, numero: int):
        self.dificuldade = dificuldade
        self.numero = numero
        self.treinos: List[Treino] = []
        self.completada = False
        self.meta_pontos = self.METAS[dificuldade]["pontos"]

    def adicionar_treino(self, data: str) -> Treino:
        treino = Treino(data)
        self.treinos.append(treino)
        return treino

    def calcular_score_total(self) -> int:
        total = 0
        for treino in self.treinos:
            score_dia = treino.calcular_score_total()
            total += min(score_dia, self.LIMITE_DIARIO)
        return total

    def calcular_progresso(self) -> float:
        """Retorna o progresso de 0 a 100%"""
        score = self.calcular_score_total()
        return min((score / self.meta_pontos) * 100, 100.0)

    def verificar_conclusao(self) -> bool:
        """Verifica se a meta foi batida"""
        if self.calcular_score_total() >= self.meta_pontos:
            self.completada = True
        return self.completada


class Usuario:
    def __init__(self, nome: str):
        self.nome = nome
        self.expedicoes: List[Expedicao] = []
        self.niveis_desbloqueados = ["facil", "medio", "dificil"]

    def iniciar_expedicao(self, dificuldade: str) -> Expedicao:
        numero = len(self.expedicoes) + 1
        expedicao = Expedicao(dificuldade, numero)
        self.expedicoes.append(expedicao)
        return expedicao

    def expedicao_atual(self) -> Optional[Expedicao]:
        for exp in reversed(self.expedicoes):
            if not exp.completada:
                return exp
        return None

    def desbloquear_nivel(self, nivel: str):
        if nivel not in self.niveis_desbloqueados:
            self.niveis_desbloqueados.append(nivel)

    def total_expedicoes_completas(self) -> int:
        return sum(1 for exp in self.expedicoes if exp.completada)
