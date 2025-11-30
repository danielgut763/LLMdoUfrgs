#!/usr/bin/env python3
"""
Programa para verificar em quais cursos cada LLM seria aprovada
com base nas notas de corte do vestibular UFRGS 2024.
"""

import json
from pathlib import Path
from typing import Dict
import re


def carregar_json(caminho: Path) -> dict:
    """Carrega um arquivo JSON."""
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalizar_nome_curso(nome: str) -> str:
    """Normaliza o nome do curso para facilitar comparação."""
    # Remover acentos, converter para minúsculas, remover espaços extras
    nome = nome.lower().strip()
    # Remover informações entre parênteses
    nome = re.sub(r'\([^)]*\)', '', nome)
    # Remover espaços múltiplos
    nome = re.sub(r'\s+', ' ', nome)
    return nome.strip()


def mapear_curso_nota_corte(nome_curso_pesos: str, notas_corte: dict) -> tuple:
    """
    Tenta mapear o nome do curso do arquivo de pesos para o nome no arquivo de notas de corte.
    Retorna (nome_completo, nota_corte) ou (None, None) se não encontrar.
    """
    # Mapeamento manual de alguns cursos específicos
    mapeamento_especial = {
        'Administração (D)': 'Administração (Integral',
        'Administração (N)': 'Administração (Noturno',
        'Administração Púb/Soc (N)': 'Administração Pública e Social',
        'Agronomia': 'Agronomia (Integral)',
        'Arquitetura e Urbanismo': 'Arquitetura e Urbanismo',
        'Arquivologia (N)': 'Arquivologia',
        'Artes Visuais (B)': 'Artes Visuais (Bacharelado',
        'Artes Visuais (L)': 'Artes Visuais (Licenciatura',
        'Biblioteconomia': 'Biblioteconomia',
        'Biomedicina': 'Biomedicina',
        'Biotecnologia': 'Biotecnologia',
        'Ciências Atuariais': 'Ciências Atuariais',
        'Ciências B Bio Mar CLN': 'Ciências Biológicas (Bacharelado, Pólo Imbé)',
        'Ciências Biológicas (B)': 'Ciências Biológicas (Bacharelado, Campus do Vale)',
        'Ciências Biológicas (L)': 'Ciências Biológicas (Licenciatura',
        'Ciências Contábeis': 'Ciências Contábeis',
        'Ciências Econômicas (D)': 'Ciências Econômicas (Integral',
        'Ciências Econômicas (N)': 'Ciências Econômicas (Noturno',
        'Ciências Sociais (D)': 'Ciências Sociais (Integral, Campus do Vale)',
        'Ciências Sociais (N)': 'Ciências Sociais (Noturno, Campus do Vale)',
        'Computação': 'Ciência da Computação',
        'Dança': 'Dança',
        'Design Produto': 'Design de Produto',
        'Design Visual': 'Design Visual',
        'Direito (D)': 'Ciências Jurídicas e Sociais – Direito (Integral',
        'Direito (N)': 'Ciências Jurídicas e Sociais – Direito (Noturno',
        'Educação Física (B)': 'ABI – Educação Física',
        'Enfermagem': 'Enfermagem',
        'Engenharia Ambiental': 'Engenharia Ambiental',
        'Engenharia Cartográfica (N)': 'Engenharia Cartográfica',
        'Engenharia Civil': 'Engenharia Civil',
        'Engenharia Contr Automação': 'Engenharia de Controle e Automação',
        'Engenharia de Alimentos': 'Engenharia de Alimentos',
        'Engenharia de Computação': 'Engenharia de Computação',
        'Engenharia de Energia': 'Engenharia de Energia',
        'Engenharia de Materiais': 'Engenharia de Materiais',
        'Engenharia de Minas': 'Engenharia de Minas',
        'Engenharia de Produção': 'Engenharia de Produção',
        'Engenharia de Serviços': 'Engenharia de Serviços',
        'Engenharia Elétrica': 'Engenharia Elétrica',
        'Engenharia Física': 'Engenharia Física',
        'Engenharia Gest Energia CLN': 'Engenharia de Gestão de Energia',
        'Engenharia Hídrica': 'Engenharia Hídrica',
        'Engenharia Mecânica': 'Engenharia Mecânica',
        'Engenharia Metalúrgica': 'Engenharia Metalúrgica',
        'Engenharia Química': 'Engenharia Química',
        'Estatística': 'Estatística',
        'Farmácia': 'Farmácia',
        'Filosofia (B) (D)': 'Filosofia (Integral',
        'Filosofia (L) (N)': 'Filosofia (Noturno, Licenciatura',
        'Fisioterapia': 'Fisioterapia',
        'Fonoaudiologia': 'Fonoaudiologia',
        'Física (B)': 'Física (Integral, Campus do Vale)',
        'Física (L) (D)': 'Física (Licenciatura, Campus do Vale)',
        'Física (L) (N)': 'Física (Noturno, Licenciatura',
        'Física Astrofísica': 'Física (Integral, Campus do Vale)',
        'Geografia (D)': 'Geografia (Bacharelado, Campus do Vale)',
        'Geografia (L) CLN': 'Geografia (Noturno, Licenciatura, Campus Litoral Norte)',
        'Geografia (N)': 'Geografia (Noturno, Bacharelado',
        'Geologia': 'Geologia',
        'História (D)': 'História (Integral, Bacharelado',
        'História (N)': 'História (Noturno, Bacharelado',
        'História da Arte': 'História da Arte',
        'Inter Ciência Tecno': 'Interdisciplinar em Ciência e Tecnologia',
        'Jornalismo': 'Jornalismo',
        'Letras (B)': 'Letras (Bacharelado',
        'Letras (B) Libras': 'Letras (Licenciatura',
        'Música': None,  # Não tem no arquivo de notas de corte
        'Nutrição': 'Nutrição',
        'Odontologia (D)': 'Odontologia (Integral',
        'Odontologia (N)': 'Odontologia (Noturno',
        'Pedagogia (M)': 'Pedagogia (Matutino',
        'Pedagogia (N)': 'Pedagogia (Noturno',
        'Políticas Públicas': 'Políticas Públicas',
        'Psicologia (D)': 'Psicologia (Integral',
        'Psicologia (N)': 'Psicologia (Noturno',
        'Publicidade & Propaganda': 'Publicidade e Propaganda',
        'Química': 'Química (Integral',
        'Química (L) (N)': 'Química (Noturno, Licenciatura',
        'Química Industrial (I)': 'Química Industrial (Integral',
        'Química Industrial (N)': 'Química Industrial (Noturno',
        'Rel. Internacionais': 'Relações Internacionais',
        'Relações Públicas': 'Relações Públicas',
        'Saúde Coletiva': None,
        'Serviço Social': None,
        'Teatro': None,
        'Teatro (L)': None,
        'ZZ CODE': None,
        'Zootecnia': None
    }
    
    padrao = mapeamento_especial.get(nome_curso_pesos)
    
    if padrao is None:
        return None, None
    
    # Buscar no dicionário de notas de corte
    for curso_completo, nota in notas_corte.items():
        if padrao in curso_completo:
            return curso_completo, nota
    
    return None, None


def main():
    """Função principal."""
    # Importar funções do outro módulo
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    
    from calcular_media_harmonica_cursos import (
        carregar_json, mapear_questoes_por_materia, contar_acertos_por_materia,
        calcular_eps_por_materia, calcular_media_harmonica_ponderada
    )
    
    # Caminhos dos arquivos
    base_path = Path(__file__).parent
    results_path = base_path / "Results.json"
    info_path = base_path / "info.json"
    pesos_path = base_path / "pesos.json"
    notas_corte_path = base_path / "notasDeCorte.json"
    
    # Carregar dados
    results = carregar_json(results_path)
    info = carregar_json(info_path)
    pesos_data = carregar_json(pesos_path)
    notas_corte_data = carregar_json(notas_corte_path)
    
    estatisticas = info['provas_2024']['estatisticas']
    pesos_cursos = pesos_data.get('pesos_provas', pesos_data.get('pesos_provas_por_curso', {}))
    notas_corte = notas_corte_data['notas_corte_2024']
    
    # Mapear questões
    mapeamento_questoes = mapear_questoes_por_materia(info)
    
    nota_redacao = 9.98
    
    print("=" * 120)
    print("VERIFICAÇÃO DE APROVAÇÃO POR CURSO - VESTIBULAR UFRGS 2024")
    print("=" * 120)
    print(f"Nota da Redação considerada: {nota_redacao}")
    print("=" * 120)
    
    # Calcular MH para cada LLM em cada curso
    llm_resultados = {}
    for llm_nome, llm_dados in results.items():
        acertos = contar_acertos_por_materia(llm_dados, mapeamento_questoes)
        eps = calcular_eps_por_materia(acertos, estatisticas, nota_redacao)
        
        llm_resultados[llm_nome] = {}
        for curso, pesos in pesos_cursos.items():
            mh = calcular_media_harmonica_ponderada(eps, pesos)
            llm_resultados[llm_nome][curso] = mh
    
    # Analisar aprovação para cada LLM
    for llm_nome in results.keys():
        print(f"\n{'=' * 120}")
        print(f"{llm_nome}")
        print(f"{'=' * 120}")
        
        aprovados = []
        reprovados = []
        sem_nota_corte = []
        
        for curso in sorted(pesos_cursos.keys()):
            mh = llm_resultados[llm_nome][curso]
            curso_completo, nota_corte = mapear_curso_nota_corte(curso, notas_corte)
            
            if curso_completo and nota_corte:
                diferenca = mh - nota_corte
                if mh >= nota_corte:
                    aprovados.append((curso, curso_completo, mh, nota_corte, diferenca))
                else:
                    reprovados.append((curso, curso_completo, mh, nota_corte, diferenca))
            else:
                sem_nota_corte.append((curso, mh))
        
        # Exibir cursos aprovados
        print(f"\nCURSOS APROVADOS ({len(aprovados)}):")
        print("-" * 120)
        if aprovados:
            # Ordenar por diferença (margem de aprovação)
            aprovados.sort(key=lambda x: x[4], reverse=True)
            for i, (curso_curto, curso_completo, mh, nota_corte, dif) in enumerate(aprovados, 1):
                status = "✓ APROVADO"
                print(f"{i:2d}. {curso_curto:<35} MH: {mh:6.2f} | Corte: {nota_corte:6.2f} | Margem: +{dif:5.2f} {status}")
        else:
            print("  Nenhum curso aprovado.")
        
        # Exibir cursos reprovados
        print(f"\nCURSOS REPROVADOS ({len(reprovados)}):")
        print("-" * 120)
        if reprovados:
            # Ordenar por diferença (do mais próximo ao mais distante)
            reprovados.sort(key=lambda x: abs(x[4]))
            for i, (curso_curto, curso_completo, mh, nota_corte, dif) in enumerate(reprovados, 1):
                status = "✗ REPROVADO"
                print(f"{i:2d}. {curso_curto:<35} MH: {mh:6.2f} | Corte: {nota_corte:6.2f} | Faltou: {dif:6.2f} {status}")
        
        # Estatísticas
        total_com_nota = len(aprovados) + len(reprovados)
        if total_com_nota > 0:
            taxa_aprovacao = (len(aprovados) / total_com_nota) * 100
            print(f"\n{'─' * 120}")
            print(f"ESTATÍSTICAS:")
            print(f"  Total de cursos com nota de corte: {total_com_nota}")
            print(f"  Aprovados: {len(aprovados)} ({taxa_aprovacao:.1f}%)")
            print(f"  Reprovados: {len(reprovados)} ({100-taxa_aprovacao:.1f}%)")
            print(f"  Cursos sem nota de corte disponível: {len(sem_nota_corte)}")
    
    # Resumo comparativo
    print("\n" + "=" * 120)
    print("RESUMO COMPARATIVO - TAXA DE APROVAÇÃO")
    print("=" * 120)
    
    for llm_nome in results.keys():
        aprovados_count = 0
        total_count = 0
        
        for curso in pesos_cursos.keys():
            mh = llm_resultados[llm_nome][curso]
            curso_completo, nota_corte = mapear_curso_nota_corte(curso, notas_corte)
            
            if curso_completo and nota_corte:
                total_count += 1
                if mh >= nota_corte:
                    aprovados_count += 1
        
        if total_count > 0:
            taxa = (aprovados_count / total_count) * 100
            print(f"{llm_nome:<15}: {aprovados_count:2d}/{total_count:2d} cursos aprovados ({taxa:5.1f}%)")
    
    print("=" * 120)


if __name__ == "__main__":
    main()
