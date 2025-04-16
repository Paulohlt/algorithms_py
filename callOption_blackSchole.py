"""
Simulação por Monte Carlo para precificação de opção de compra (call) europeia
usando o modelo Black-Scholes. Estruturado de forma elegante e completo,
ideal para uso em uma tesouraria de um banco de investimentos.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def precificar_call_europeia_monte_carlo(
    S0: float,          # Preço inicial do ativo subjacente
    K: float,           # Preço de exercício (strike)
    T: float,           # Tempo até o vencimento (em anos)
    r: float,           # Taxa de juros livre de risco (anual)
    sigma: float,       # Volatilidade anual do ativo subjacente
    n_sim: int,         # Número de simulações
    seed: int = 42      # Semente para reprodutibilidade
) -> dict:
    """
    Retorna as métricas de precificação para uma opção de compra (call) europeia,
    estimada via simulação Monte Carlo com o modelo Black-Scholes.
    """
    np.random.seed(seed)
    
    # Gera ruído aleatório ~ N(0,1)
    Z = np.random.normal(0, 1, n_sim)
    
    # Simula o preço do ativo no vencimento (S_T)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    # Calcula o payoff: max(ST - K, 0)
    payoff = np.maximum(ST - K, 0.0)
    
    # Preço da opção (valor presente do payoff médio)
    preco_call = np.exp(-r * T) * np.mean(payoff)
    
    # Estatísticas dos payoffs descontados
    payoff_descontado = np.exp(-r * T) * payoff
    desvio_padrao = np.std(payoff_descontado, ddof=1)
    
    # Intervalo de confiança de 95%
    intervalo_95 = 1.96 * desvio_padrao / np.sqrt(n_sim)
    ic_inferior = preco_call - intervalo_95
    ic_superior = preco_call + intervalo_95
    
    return {
        "preco_call": preco_call,
        "desvio_padrao": desvio_padrao,
        "ic_inferior": ic_inferior,
        "ic_superior": ic_superior,
        "n_sim": n_sim
    }

def main():
    # Parâmetros de mercado e da opção
    S0 = 100.0       # Preço inicial do ativo subjacente
    K = 105.0        # Strike (preço de exercício)
    T = 1.0          # Tempo até o vencimento (1 ano)
    r = 0.05         # Taxa de juros livre de risco (5% ao ano)
    sigma = 0.20     # Volatilidade anual (20%)
    n_sim = 100_000  # Número de simulações de Monte Carlo
    
    # Realiza a simulação
    resultados = precificar_call_europeia_monte_carlo(S0, K, T, r, sigma, n_sim)
    
    # Organiza os resultados em um DataFrame para visualização
    df_stats = pd.DataFrame({
        "Preço Estimado (R$)": [resultados["preco_call"]],
        "Desvio Padrão (R$)": [resultados["desvio_padrao"]],
        "IC 95% Inferior (R$)": [resultados["ic_inferior"]],
        "IC 95% Superior (R$)": [resultados["ic_superior"]],
        "Simulações": [resultados["n_sim"]]
    })
    
    print("Resultados da Simulação Monte Carlo (Call Europeia)\n")
    print(df_stats.to_string(index=False), "\n")
    
    # Para visualização, gera novamente as simulações e plota o histograma dos preços simulados
    np.random.seed(42)
    Z = np.random.normal(0, 1, n_sim)
    ST = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
    
    plt.figure(figsize=(10, 4))
    plt.hist(ST, bins=100, color='steelblue', alpha=0.7, density=True)
    plt.axvline(x=K, color='red', linestyle='--', label='Strike (K)')
    plt.title('Distribuição dos Preços Simulados no Vencimento (S_T)')
    plt.xlabel('Preço no vencimento (S_T)')
    plt.ylabel('Densidade')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    print("Observação: A linha vermelha indica o preço de exercício da opção.")

if __name__ == "__main__":
    main()
