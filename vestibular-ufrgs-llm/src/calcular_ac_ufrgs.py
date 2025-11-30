#!/usr/bin/env python3
"""
Programa para calcular o Argumento de Classificação (AC) no vestibular da UFRGS.

Fórmula do Escore Padronizado: EP = ((EB - MD) / DP) * 100 + 500
Fórmula do AC (média harmônica ponderada): AC = soma_pesos / soma(peso_i / EP_i)
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple


def carregar_json(caminho: Path) -> dict:
    """Carrega um arquivo JSON."""
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)


def calcular_escore_padronizado(escore_bruto: float, media: float, desvio_padrao: float) -> float:
    """
    Calcula o escore padronizado usando a fórmula da UFRGS.
    
    EP = ((EB - MD) / DP) * 100 + 500
    """
    if desvio_padrao == 0:
        return 500.0
    return ((escore_bruto - media) / desvio_padrao) * 100 + 500


def mapear_questoes_por_materia(info: dict) -> Dict[str, List[int]]:
    """
    Mapeia os números das questões para cada matéria baseado na estrutura do vestibular.
    
    Returns:
        Dicionário com matéria como chave e lista de números de questões como valor
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
    
    # Dia 1 - PRIMEIRA_PROVA
    estrutura_dia1 = info['provas_2024']['estrutura_prova']['dia_1']['distribuicao']
    for item in estrutura_dia1:
        questoes_range = item['questoes']
        materia = item['materia'].lower().replace(' ', '_')
        
        # Parse do range (ex: "1-15" -> [1, 2, ..., 15])
        inicio, fim = map(int, questoes_range.split('-'))
        questoes = list(range(inicio, fim + 1))
        
        if materia == 'lingua_portuguesa':
            mapeamento['portugues'].extend(questoes)
        else:
            mapeamento[materia].extend(questoes)
    
    # Dia 2 - SEGUNDA_PROVA
    estrutura_dia2 = info['provas_2024']['estrutura_prova']['dia_2']['distribuicao']
    for item in estrutura_dia2:
        questoes_range = item['questoes']
        materia = item['materia'].lower()
        
        inicio, fim = map(int, questoes_range.split('-'))
        questoes = list(range(inicio, fim + 1))
        
        # Inglês e Espanhol são agrupados como língua estrangeira
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
    
    # Processar PRIMEIRA_PROVA
    primeira_prova = results_llm.get('PRIMEIRA_PROVA', {})
    iguais_p1 = [int(q) for q in primeira_prova.get('iguais', [])]
    
    # Processar SEGUNDA_PROVA
    segunda_prova = results_llm.get('SEGUNDA_PROVA', {})
    iguais_p2 = [int(q) for q in segunda_prova.get('iguais', [])]
    
    # Contar acertos por matéria
    for materia, questoes in mapeamento_questoes.items():
        for q in questoes:
            # Verificar se a questão está no dia 1 ou dia 2
            if any(1 <= num <= 60 for num in questoes if num == q):  # Dia 1
                if q in iguais_p1:
                    acertos[materia] += 1
            else:  # Dia 2
                if q in iguais_p2:
                    acertos[materia] += 1
    
    return acertos


def calcular_total_questoes_por_materia(mapeamento_questoes: Dict[str, List[int]]) -> Dict[str, int]:
    """Calcula o total de questões por matéria."""
    return {materia: len(questoes) for materia, questoes in mapeamento_questoes.items()}


def calcular_ac_para_curso(
    acertos_por_materia: Dict[str, int],
    total_questoes_por_materia: Dict[str, int],
    estatisticas: dict,
    pesos_curso: dict,
    nota_redacao: float = 9.98
) -> Tuple[float, Dict[str, float]]:
    """
    Calcula o Argumento de Classificação para um curso específico.
    
    Returns:
        Tupla com (AC, dicionário de escores padronizados por matéria)
    """
    escores_padronizados = {}
    
    # Calcular escore padronizado para cada matéria
    for materia, acertos in acertos_por_materia.items():
        total = total_questoes_por_materia[materia]
        if total == 0:
            continue
            
        # Escore bruto (número de acertos)
        escore_bruto = acertos
        
        # Pegar estatísticas da matéria
        # Ajustar nome da matéria para o formato do info.json
        materia_stat = materia
        if materia == 'lingua_estrangeira':
            materia_stat = 'ingles'  # Usar inglês como referência
        
        stats = estatisticas.get(materia_stat, {})
        media = stats.get('media', 0)
        desvio = stats.get('desvio_padrao', 1)
        
        # Calcular escore padronizado
        ep = calcular_escore_padronizado(escore_bruto, media, desvio)
        escores_padronizados[materia] = ep
    
    # Adicionar redação ao Português (já convertida em escore padronizado)
    # A redação tem nota de 0 a 10, média ~6.0 e DP ~2.0 (valores típicos)
    ep_redacao = calcular_escore_padronizado(nota_redacao, 6.0, 2.0)
    
    # Combinar Português com Redação (média dos dois escores)
    if 'portugues' in escores_padronizados:
        escores_padronizados['portugues_redacao'] = (
            escores_padronizados['portugues'] + ep_redacao
        ) / 2
    else:
        escores_padronizados['portugues_redacao'] = ep_redacao
    
    # Calcular AC (média harmônica ponderada)
    soma_pesos = 0
    soma_inversos = 0
    
    for materia_peso, peso in pesos_curso.items():
        if materia_peso == 'total':
            continue
            
        ep = escores_padronizados.get(materia_peso, 500)  # 500 é o valor médio
        if ep > 0:
            soma_pesos += peso
            soma_inversos += peso / ep
    
    ac = soma_pesos / soma_inversos if soma_inversos > 0 else 0
    
    return ac, escores_padronizados


def main():
    """Função principal."""
    # Caminhos dos arquivos
    base_path = Path(__file__).parent
    results_path = base_path / "Results.json"
    info_path = base_path / "info.json"
    pesos_path = base_path / "pesos.json"
    
    # Carregar dados
    print("Carregando dados...")
    results = carregar_json(results_path)
    info = carregar_json(info_path)
    pesos_data = carregar_json(pesos_path)
    
    estatisticas = info['provas_2024']['estatisticas']
    
    # Mapear questões por matéria
    mapeamento_questoes = mapear_questoes_por_materia(info)
    total_questoes = calcular_total_questoes_por_materia(mapeamento_questoes)
    
    print("\n" + "=" * 100)
    print("CÁLCULO DO ARGUMENTO DE CLASSIFICAÇÃO (AC) - VESTIBULAR UFRGS 2024")
    print("=" * 100)
    print(f"\nNota da Redação considerada: 9.98")
    print("=" * 100)
    
    # Processar cada LLM
    for llm_nome, llm_dados in results.items():
        print(f"\n{'=' * 100}")
        print(f"LLM: {llm_nome}")
        print(f"{'=' * 100}")
        
        # Contar acertos por matéria
        acertos = contar_acertos_por_materia(llm_dados, mapeamento_questoes)
        
        print("\nDesempenho por Matéria:")
        print("-" * 100)
        for materia, acertos_num in sorted(acertos.items()):
            total = total_questoes[materia]
            percentual = (acertos_num / total * 100) if total > 0 else 0
            print(f"  {materia.replace('_', ' ').title():<25}: {acertos_num:2d}/{total:2d} = {percentual:6.2f}%")
        
        # Calcular AC para cada curso
        print(f"\n{'─' * 100}")
        print("ARGUMENTO DE CLASSIFICAÇÃO POR CURSO:")
        print(f"{'─' * 100}")
        print(f"{'Curso':<35} {'AC':>10}")
        print("-" * 100)
        
        resultados_cursos = []
        for curso, pesos in pesos_data['pesos_provas_por_curso'].items():
            ac, _ = calcular_ac_para_curso(
                acertos,
                total_questoes,
                estatisticas,
                pesos
            )
            resultados_cursos.append((curso, ac))
        
        # Ordenar por AC (decrescente)
        resultados_cursos.sort(key=lambda x: x[1], reverse=True)
        
        for curso, ac in resultados_cursos:
            print(f"{curso:<35} {ac:10.2f}")
        
        print("-" * 100)
        print(f"{'Melhor curso':<35} {resultados_cursos[0][0]}: {resultados_cursos[0][1]:.2f}")
        print(f"{'Pior curso':<35} {resultados_cursos[-1][0]}: {resultados_cursos[-1][1]:.2f}")
    
    print("\n" + "=" * 100)


if __name__ == "__main__":
    main()
