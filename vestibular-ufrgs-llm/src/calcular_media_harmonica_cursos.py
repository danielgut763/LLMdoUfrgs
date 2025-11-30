#!/usr/bin/env python3
"""
Programa para calcular a média harmônica ponderada por curso para cada LLM.

Usa os Escores Padronizados (EP) reais do vestibular UFRGS.
Fórmula da média harmônica ponderada: MH = soma_pesos / soma(peso_i / EP_i)
"""

import json
from pathlib import Path
from typing import Dict, List


def carregar_json(caminho: Path) -> dict:
    """Carrega um arquivo JSON."""
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)


def mapear_questoes_por_materia(info: dict) -> Dict[str, List[int]]:
    """
    Mapeia os números das questões para cada matéria.
    """
    mapeamento = {
        'portugues': [],
        'literatura': [],
        'matematica': [],
        'geografia': [],
        'historia': [],
        'fisica': [],
        'quimica': [],
        'biologia': [],
        'lingua_estrangeira': []
    }
    
    # Dia 1
    estrutura_dia1 = info['provas_2024']['estrutura_prova']['dia_1']['distribuicao']
    for item in estrutura_dia1:
        questoes_range = item['questoes']
        materia = item['materia'].lower().replace(' ', '_')
        
        inicio, fim = map(int, questoes_range.split('-'))
        questoes = list(range(inicio, fim + 1))
        
        if materia == 'lingua_portuguesa':
            mapeamento['portugues'].extend(questoes)
        else:
            mapeamento[materia].extend(questoes)
    
    # Dia 2
    estrutura_dia2 = info['provas_2024']['estrutura_prova']['dia_2']['distribuicao']
    for item in estrutura_dia2:
        questoes_range = item['questoes']
        materia = item['materia'].lower()
        
        inicio, fim = map(int, questoes_range.split('-'))
        questoes = list(range(inicio, fim + 1))
        
        if materia in ['ingles', 'espanhol']:
            mapeamento['lingua_estrangeira'].extend(questoes)
        else:
            mapeamento[materia].extend(questoes)
    
    return mapeamento


def contar_acertos_por_materia(
    results_llm: dict,
    mapeamento_questoes: Dict[str, List[int]]
) -> Dict[str, int]:
    """
    Conta quantas questões a LLM acertou em cada matéria.
    """
    acertos = {materia: 0 for materia in mapeamento_questoes.keys()}
    
    primeira_prova = results_llm.get('PRIMEIRA_PROVA', {})
    iguais_p1 = [int(q) for q in primeira_prova.get('iguais', [])]
    
    segunda_prova = results_llm.get('SEGUNDA_PROVA', {})
    iguais_p2 = [int(q) for q in segunda_prova.get('iguais', [])]
    
    for materia, questoes in mapeamento_questoes.items():
        for q in questoes:
            if q <= 60:  # Dia 1
                if q in iguais_p1:
                    acertos[materia] += 1
            else:  # Dia 2
                if q in iguais_p2:
                    acertos[materia] += 1
    
    return acertos


def obter_ep_por_acertos(estatisticas: dict, materia: str, acertos: int) -> float:
    """
    Obtém o Escore Padronizado (EP) baseado no número de acertos.
    """
    # Ajustar nome da matéria para buscar nas estatísticas
    materia_lookup = materia
    if materia == 'lingua_estrangeira':
        materia_lookup = 'ingles'  # Usar inglês como referência
    
    materia_stats = estatisticas.get(materia_lookup, {})
    escores = materia_stats.get('escores', [])
    
    # Buscar o EP correspondente ao número de acertos
    for item in escores:
        if item['acertos'] == acertos:
            return item['ep']
    
    # Se não encontrar, calcular usando a fórmula
    media = materia_stats.get('media', 0)
    desvio = materia_stats.get('desvio_padrao', 1)
    if desvio > 0:
        return ((acertos - media) / desvio) * 100 + 500
    return 500.0


def calcular_ep_redacao(nota_redacao: float) -> float:
    """
    Calcula o EP da redação.
    Redação tipicamente tem média ~6.0 e desvio padrão ~2.0
    """
    media_redacao = 6.0
    dp_redacao = 2.0
    return ((nota_redacao - media_redacao) / dp_redacao) * 100 + 500


def calcular_eps_por_materia(
    acertos: Dict[str, int],
    estatisticas: dict,
    nota_redacao: float = 9.98
) -> Dict[str, float]:
    """
    Calcula os Escores Padronizados (EP) para cada matéria.
    """
    eps = {}
    
    for materia, acertos_num in acertos.items():
        eps[materia] = obter_ep_por_acertos(estatisticas, materia, acertos_num)
    
    # Calcular EP da redação
    ep_redacao = calcular_ep_redacao(nota_redacao)
    
    # Combinar Português com Redação (média aritmética dos EPs)
    if 'portugues' in eps:
        eps['portugues_redacao'] = (eps['portugues'] + ep_redacao) / 2
    else:
        eps['portugues_redacao'] = ep_redacao
    
    return eps


def calcular_media_harmonica_ponderada(
    eps: Dict[str, float],
    pesos: dict
) -> float:
    """
    Calcula a média harmônica ponderada usando os EPs.
    
    MH = soma_pesos / soma(peso_i / EP_i)
    """
    # Mapeamento de abreviações para nomes completos
    mapeamento_abrev = {
        'POR': 'portugues_redacao',
        'LIT': 'literatura',
        'GEO': 'geografia',
        'HIS': 'historia',
        'BIO': 'biologia',
        'FIS': 'fisica',
        'QUI': 'quimica',
        'MAT': 'matematica',
        'LIN': 'lingua_estrangeira'
    }
    
    soma_pesos = 0
    soma_inversos = 0
    
    for abrev, peso in pesos.items():
        if abrev == 'total':
            continue
        
        materia = mapeamento_abrev.get(abrev)
        if materia is None:
            continue
            
        ep = eps.get(materia, 500)  # 500 é o EP médio
        if ep > 0:
            soma_pesos += peso
            soma_inversos += peso / ep
        else:
            return 0.0
    
    if soma_inversos > 0:
        return soma_pesos / soma_inversos
    return 0.0


def main():
    """Função principal."""
    # Caminhos dos arquivos
    base_path = Path(__file__).parent
    results_path = base_path / "Results.json"
    info_path = base_path / "info.json"
    pesos_path = base_path / "pesos.json"
    
    # Carregar dados
    results = carregar_json(results_path)
    info = carregar_json(info_path)
    pesos_data = carregar_json(pesos_path)
    
    estatisticas = info['provas_2024']['estatisticas']
    pesos_cursos = pesos_data.get('pesos_provas', pesos_data.get('pesos_provas_por_curso', {}))
    
    # Mapear questões
    mapeamento_questoes = mapear_questoes_por_materia(info)
    
    nota_redacao = 9.98
    ep_redacao = calcular_ep_redacao(nota_redacao)
    
    print("=" * 120)
    print("MÉDIA HARMÔNICA PONDERADA POR CURSO - VESTIBULAR UFRGS")
    print("=" * 120)
    print(f"Nota da Redação: {nota_redacao} (EP: {ep_redacao:.2f})")
    print("Usando Escores Padronizados (EP) reais do vestibular UFRGS")
    print("=" * 120)
    
    # Processar cada LLM
    for llm_nome, llm_dados in results.items():
        print(f"\n{llm_nome}")
        print("-" * 120)
        
        # Contar acertos
        acertos = contar_acertos_por_materia(llm_dados, mapeamento_questoes)
        
        # Calcular EPs
        eps = calcular_eps_por_materia(acertos, estatisticas, nota_redacao)
        
        # Mostrar desempenho por matéria com EP
        print("\nDesempenho por Matéria (Acertos -> EP):")
        for materia in sorted(acertos.keys()):
            acertos_num = acertos[materia]
            ep = eps[materia]
            print(f"  {materia.replace('_', ' ').title():<25}: {acertos_num:2d} acertos -> EP: {ep:6.2f}")
        print(f"  {'Portugues + Redacao':<25}: EP combinado: {eps['portugues_redacao']:6.2f}")
        
        # Calcular média harmônica para cada curso
        print(f"\n{'─' * 120}")
        print(f"Média Harmônica Ponderada por Curso (Total de {len(pesos_cursos)} cursos):")
        print(f"{'─' * 120}")
        
        resultados_cursos = []
        for curso, pesos in pesos_cursos.items():
            mh = calcular_media_harmonica_ponderada(eps, pesos)
            resultados_cursos.append((curso, mh))
        
        # Ordenar por média harmônica (decrescente)
        resultados_cursos.sort(key=lambda x: x[1], reverse=True)
        
        # Exibir resultados
        for curso, mh in resultados_cursos:
            print(f"  {curso:<40} {mh:6.2f}")
        
        print("-" * 120)
        print(f"  {'MELHOR:':<40} {resultados_cursos[0][0]}: {resultados_cursos[0][1]:.2f}")
        print(f"  {'PIOR:':<40} {resultados_cursos[-1][0]}: {resultados_cursos[-1][1]:.2f}")
    
    print("\n" + "=" * 120)
    print(f"\nRESUMO COMPARATIVO - TOP 20 CURSOS POR LLM")
    print("=" * 120)
    
    # Criar tabela comparativa
    cursos = list(pesos_cursos.keys())
    
    # Calcular para todas LLMs
    llm_resultados = {}
    for llm_nome, llm_dados in results.items():
        acertos = contar_acertos_por_materia(llm_dados, mapeamento_questoes)
        eps = calcular_eps_por_materia(acertos, estatisticas, nota_redacao)
        
        llm_resultados[llm_nome] = {}
        for curso, pesos in pesos_cursos.items():
            mh = calcular_media_harmonica_ponderada(eps, pesos)
            llm_resultados[llm_nome][curso] = mh
    
    # Exibir top 20 de cada LLM
    for llm_nome in results.keys():
        print(f"\nTOP 20 CURSOS - {llm_nome}:")
        print("-" * 120)
        
        # Ordenar cursos por MH para esta LLM
        cursos_ordenados = sorted(
            [(curso, llm_resultados[llm_nome][curso]) for curso in cursos],
            key=lambda x: x[1],
            reverse=True
        )[:20]
        
        for i, (curso, mh) in enumerate(cursos_ordenados, 1):
            print(f"  {i:2d}. {curso:<45} {mh:6.2f}")
    
    print("\n" + "=" * 120)
    print(f"\nTABELA COMPLETA DE TODOS OS {len(cursos)} CURSOS")
    print("=" * 120)
    print(f"\n{'Curso':<45} ", end="")
    for llm in results.keys():
        print(f"{llm:>10}", end="  ")
    print()
    print("-" * 120)
    
    for curso in sorted(cursos):
        print(f"{curso:<45} ", end="")
        for llm in results.keys():
            mh = llm_resultados[llm][curso]
            print(f"{mh:10.2f}", end="  ")
        print()
    
    print("=" * 120)


if __name__ == "__main__":
    main()
