from models import Usuario
from storage import Storage

storage = Storage()

usuario = Usuario("Gabriel")
treino = usuario.adicionar_treino("2026-05-21")
treino.adicionar_tentativa("V1", True)
treino.adicionar_tentativa("V2", True)
treino.adicionar_tentativa("V3", False)

print(f"Score: {usuario.calcular_score_total()}")
print(f"Altura: {usuario.obter_altura_montanha():.1f}%")

storage.salvar_usuario(usuario)
print("Usuário salvo!")

usuario_carregado = storage.carregar_usuario("Gabriel")
print(f"Usuário carregado: {usuario_carregado.nome}")
print(f"Treinos: {len(usuario_carregado.treinos)}")