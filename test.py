from models import Usuario

# Criar um usuário
usuario = Usuario("Gabriel")

# Adicionar um treino de hoje
treino_hoje = usuario.adicionar_treino("2026-05-21")

# Simular você escalando na academia
treino_hoje.adicionar_tentativa("V0", True)
treino_hoje.adicionar_tentativa("V1", True)
treino_hoje.adicionar_tentativa("V2", False)
treino_hoje.adicionar_tentativa("V3", True)
treino_hoje.adicionar_tentativa("V4", True)

# Ver os resultados
print(f"Score do treino: {treino_hoje.calcular_score_total()}")
print(f"Score total acumulado: {usuario.calcular_score_total()}")
print(f"Altura da montanha: {usuario.obter_altura_montanha():.1f} porcento")