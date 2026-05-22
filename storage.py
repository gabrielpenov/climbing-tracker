import json
from models import Usuario, Expedicao, Treino, Tentativa
from typing import Optional


class Storage:
    def __init__(self, arquivo: str = "dados.json"):
        self.arquivo = arquivo

    def salvar_usuario(self, usuario: Usuario) -> None:
        dados = {
            "nome": usuario.nome,
            "niveis_desbloqueados": usuario.niveis_desbloqueados,
            "expedicoes": []
        }

        for exp in usuario.expedicoes:
            exp_dict = {
                "dificuldade": exp.dificuldade,
                "numero": exp.numero,
                "completada": exp.completada,
                "treinos": []
            }

            for treino in exp.treinos:
                treino_dict = {
                    "data": treino.data,
                    "tentativas": []
                }
                for tentativa in treino.tentativas:
                    treino_dict["tentativas"].append({
                        "nivel": tentativa.nivel,
                        "completou": tentativa.completou,
                        "data_hora": tentativa.data_hora.isoformat()
                    })
                exp_dict["treinos"].append(treino_dict)

            dados["expedicoes"].append(exp_dict)

        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def carregar_usuario(self) -> Optional[Usuario]:
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            usuario = Usuario(dados["nome"])
            usuario.niveis_desbloqueados = dados.get("niveis_desbloqueados", ["facil", "medio", "dificil"])

            for exp_dict in dados["expedicoes"]:
                exp = usuario.iniciar_expedicao(exp_dict["dificuldade"])
                exp.completada = exp_dict["completada"]

                for treino_dict in exp_dict["treinos"]:
                    treino = exp.adicionar_treino(treino_dict["data"])
                    for t in treino_dict["tentativas"]:
                        treino.adicionar_tentativa(t["nivel"], t["completou"])

            return usuario

        except FileNotFoundError:
            return None
