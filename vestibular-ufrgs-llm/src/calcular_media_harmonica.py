#!/usr/bin/env python3
"""
Programa para calcular a média harmônica no vestibular da UFRGS para cada LLM.

A média harmônica é calculada pela fórmula: MH = 2 / (1/P1 + 1/P2)
Onde P1 é a nota da primeira prova e P2 é a nota da segunda prova.
"""

import json
from pathlib import Path


def calcular_media_harmonica(nota1, nota2):
    """
    Calcula a média harmônica entre duas notas.
    
    Args:
        nota1: Nota da primeira prova
        nota2: Nota da segunda prova
        
    Returns:
        float: Média harmônica
    """
    if nota1 == 0 or nota2 == 0:
        return 0.0
    return 2 / (1/nota1 + 1/nota2)


def calcular_acertos(dados_prova):
    """
    Calcula o número de acertos em uma prova.
    
    Args:
        dados_prova: Dicionário com os dados da prova (iguais e diferentes)
        
    Returns:
        int: Número de questões corretas
    """
    return len(dados_prova.get("iguais", []))


def calcular_total_questoes(dados_prova):
    """
    Calcula o total de questões na prova.
    
    Args:
        dados_prova: Dicionário com os dados da prova
        
    Returns:
        int: Total de questões
    """
    acertos = len(dados_prova.get("iguais", []))
    erros = len(dados_prova.get("diferentes", {}))
    return acertos + erros


def main():
    """Função principal do programa."""
    # Caminho para o arquivo results.json
    caminho_arquivo = Path(__file__).parent / "Results.json"
    
    # Carregar dados do arquivo JSON
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo {caminho_arquivo} não encontrado!")
        return
    except json.JSONDecodeError:
        print("Erro: Arquivo JSON inválido!")
        return
    
    print("=" * 80)
    print("CÁLCULO DA MÉDIA HARMÔNICA - VESTIBULAR UFRGS")
    print("=" * 80)
    print()
    
    # Processar cada LLM
    resultados = []
    
    for llm_nome, llm_dados in dados.items():
        # Obter dados das provas
        primeira_prova = llm_dados.get("PRIMEIRA_PROVA", {})
        segunda_prova = llm_dados.get("SEGUNDA_PROVA", {})
        
        # Calcular acertos e totais
        acertos_p1 = calcular_acertos(primeira_prova)
        total_p1 = calcular_total_questoes(primeira_prova)
        nota_p1 = (acertos_p1 / total_p1 * 100) if total_p1 > 0 else 0
        
        acertos_p2 = calcular_acertos(segunda_prova)
        total_p2 = calcular_total_questoes(segunda_prova)
        nota_p2 = (acertos_p2 / total_p2 * 100) if total_p2 > 0 else 0
        
        # Calcular média harmônica
        media_harmonica = calcular_media_harmonica(nota_p1, nota_p2)
        
        # Armazenar resultados
        resultados.append({
            'llm': llm_nome,
            'acertos_p1': acertos_p1,
            'total_p1': total_p1,
            'nota_p1': nota_p1,
            'acertos_p2': acertos_p2,
            'total_p2': total_p2,
            'nota_p2': nota_p2,
            'media_harmonica': media_harmonica
        })
    
    # Ordenar por média harmônica (decrescente)
    resultados.sort(key=lambda x: x['media_harmonica'], reverse=True)
    
    # Exibir resultados
    for i, resultado in enumerate(resultados, 1):
        print(f"{i}. {resultado['llm']}")
        print(f"   {'─' * 70}")
        print(f"   Primeira Prova: {resultado['acertos_p1']:2d}/{resultado['total_p1']:2d} questões corretas = {resultado['nota_p1']:6.2f}%")
        print(f"   Segunda Prova:  {resultado['acertos_p2']:2d}/{resultado['total_p2']:2d} questões corretas = {resultado['nota_p2']:6.2f}%")
        print(f"   Média Harmônica: {resultado['media_harmonica']:.2f}")
        print()
    
    print("=" * 80)
    print()
    
    # Exibir resumo comparativo
    print("RESUMO COMPARATIVO:")
    print("-" * 80)
    print(f"{'LLM':<15} {'Prova 1':<12} {'Prova 2':<12} {'Média Harmônica':<20}")
    print("-" * 80)
    for resultado in resultados:
        print(f"{resultado['llm']:<15} {resultado['nota_p1']:6.2f}%    {resultado['nota_p2']:6.2f}%    {resultado['media_harmonica']:6.2f}")
    print("-" * 80)


if __name__ == "__main__":
    main()
