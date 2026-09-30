import json
import os
from datetime import datetime

ARQUIVO_JSON = 'alunos.json'

# Função 1: Carregar os dados do arquivo JSON para uma lista de dicionários
def carregar_dados():
    """Lê os registros do arquivo JSON se existir."""
    if not os.path.exists(ARQUIVO_JSON):
        return []
    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return []

# Função 2: Salvar os dados na lista de dicionários dentro do JSON
def salvar_dados(lista_alunos):
    """Salva a lista de dicionários no arquivo JSON."""
    try:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(lista_alunos, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False

# Função 3: Definir a situação do aluno com base na nota
def calcular_situacao(nota):
    """Retorna Aprovado, Recuperação ou Reprovado."""
    if nota >= 7.0:
        return "Aprovado"
    elif 5.0 <= nota < 7.0:
        return "Recuperação"
    else:
        return "Reprovado"

# Função 4: Cadastrar um novo aluno com validação try/except e registro de data/hora
def cadastrar_aluno(nome, serie, nota_str):
    """Valida entradas com try/except e adiciona o aluno no JSON com data e hora."""
    try:
        # Tratamento de erro na conversão da nota
        nota = float(nota_str.replace(',', '.'))
        if nota < 0 or nota > 10:
            return False, "A nota deve estar entre 0 e 10!"
        if not nome.strip() or not serie.strip():
            return False, "Preencha todos os campos corretamente!"

        alunos = carregar_dados()
        situacao = calcular_situacao(nota)
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        novo_aluno = {
            "id": len(alunos) + 1 if not alunos else max(a.get("id", 0) for a in alunos) + 1,
            "nome": nome.strip(),
            "serie": serie.strip(),
            "nota": nota,
            "situacao": situacao,
            "data_registro": data_hora
        }

        alunos.append(novo_aluno)
        salvar_dados(alunos)
        return True, "Aluno cadastrado com sucesso!"

    except ValueError:
        return False, "Nota inválida! Insira um número válido (ex: 8.5)."
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"

# Função 5: Excluir um aluno pelo ID ou Nome
def excluir_aluno(aluno_id):
    """Remove um registro da lista e atualiza o arquivo JSON."""
    alunos = carregar_dados()
    novos_alunos = [a for a in alunos if a['id'] != int(aluno_id)]
    if len(novos_alunos) < len(alunos):
        salvar_dados(novos_alunos)
        return True, "Aluno removido com sucesso!"
    return False, "Aluno não encontrado!"

# Função 6: Calcular estatísticas gerais
def calcular_estatisticas():
    """Gera total de alunos, média das notas e contagem por situação."""
    alunos = carregar_dados()
    if not alunos:
        return {"total": 0, "media": 0.0, "aprovados": 0, "recuperacao": 0, "reprovados": 0}

    total = len(alunos)
    soma_notas = sum(a['nota'] for a in alunos)
    media = soma_notas / total

    aprovados = sum(1 for a in alunos if a['situacao'] == "Aprovado")
    recuperacao = sum(1 for a in alunos if a['situacao'] == "Recuperação")
    reprovados = sum(1 for a in alunos if a['situacao'] == "Reprovado")

    return {
        "total": total,
        "media": round(media, 2),
        "aprovados": aprovados,
        "recuperacao": recuperacao,
        "reprovados": reprovados
    }