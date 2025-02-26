import pandas as pd
import os


def carregar_dados(caminho_arquivo):
    """Carrega o arquivo CSV com os dados das redes sociais."""
    if not os.path.exists(caminho_arquivo):
        print("Arquivo não encontrado.")
        return None

    try:
        df = pd.read_csv(caminho_arquivo)
        print("Arquivo carregado com sucesso!")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None


def calcular_metricas(df):
    """Calcula métricas básicas de engajamento."""
    if df is None:
        return None

    # Verifica se as colunas necessárias existem
    colunas_necessarias = ['Post', 'Curtidas', 'Comentários', 'Compartilhamentos', 'Seguidores']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            print(f"Coluna {coluna} não encontrada no arquivo.")
            return None

    df['Total_Engajamento'] = df['Curtidas'] + df['Comentários'] + df['Compartilhamentos']
    media_engajamento = df['Total_Engajamento'].mean()
    crescimento_seguidores = df['Seguidores'].pct_change().fillna(0) * 100

    return {
        "Média de Engajamento por Post": round(media_engajamento, 2),
        "Crescimento Médio de Seguidores (%)": round(crescimento_seguidores.mean(), 2),
        "Top Post": df.loc[df['Total_Engajamento'].idxmax(), 'Post']
    }


def gerar_relatorio(metricas, caminho_saida):
    """Gera um arquivo CSV com o resumo das métricas."""
    if metricas is None:
        print("Nenhuma métrica calculada para gerar relatório.")
        return

    df_relatorio = pd.DataFrame([metricas])
    df_relatorio.to_csv(caminho_saida, index=False)
    print(f"Relatório salvo em: {caminho_saida}")


if __name__ == "__main__":
    caminho_entrada = "relatorio_redes.csv"  # Nome do arquivo de entrada
    caminho_saida = "relatorio_analise.csv"  # Nome do arquivo de saída

    df = carregar_dados(caminho_entrada)
    metricas = calcular_metricas(df)
    if metricas:
        print("Métricas calculadas:")
        for chave, valor in metricas.items():
            print(f"{chave}: {valor}")
        gerar_relatorio(metricas, caminho_saida)
