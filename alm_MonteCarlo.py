import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def simular_risco_caixa(
    saldo_inicial: float,
    horizonte: int,
    mu_inflow: float,
    sigma_inflow: float,
    mu_outflow: float,
    sigma_outflow: float,
    n_sim: int = 10000,
    seed: int = 42
) -> dict:
    """
    Executa simulações de fluxo de caixa diário ao longo do horizonte definido,
    gerando cenários aleatórios para os fluxos de entrada e saída.
    
    """
    np.random.seed(seed)
    
    # Simula fluxos diários de entrada e saída para cada simulação
    # As distribuições podem ser ajustadas conforme o comportamento histórico da empresa.
    inflows = np.random.normal(loc=mu_inflow, scale=sigma_inflow, size=(n_sim, horizonte))
    outflows = np.random.normal(loc=mu_outflow, scale=sigma_outflow, size=(n_sim, horizonte))
    
    # O fluxo líquido diário
    fluxo_liquido = inflows - outflows  # positivo se entradas superam saídas
    
    # Calcula o saldo de caixa cumulativo para cada simulação, começando com o saldo_inicial
    saldo_cumulativo = saldo_inicial + np.cumsum(fluxo_liquido, axis=1)
    
    # Saldo mínimo observado durante o horizonte para cada simulação
    saldo_min = np.min(saldo_cumulativo, axis=1)
    
    # Saldo final de cada simulação (ao término do horizonte)
    saldo_final = saldo_cumulativo[:, -1]
    
    # Conta quantas simulações tiveram saldo negativo (falha em cumprir obrigações)
    ocorrencias_shortfall = np.sum(saldo_min < 0)
    prob_shortfall = ocorrencias_shortfall / n_sim
    
    return {
        "prob_shortfall": prob_shortfall,
        "saldo_final": saldo_final,
        "saldo_min": saldo_min,
        "media_saldo_final": np.mean(saldo_final),
        "n_sim": n_sim,
        "horizonte": horizonte
    }

def main():
    # Parâmetros da simulação
    saldo_inicial = 1_000_000.0      # caixa inicial (em R$)
    horizonte = 30                   # horizonte de 30 dias
    mu_inflow = 50_000.0             # média diária de entrada (R$)
    sigma_inflow = 10_000.0          # desvio padrão das entradas (R$)
    mu_outflow = 60_000.0            # média diária de saída (R$)
    sigma_outflow = 15_000.0         # desvio padrão das saídas (R$)
    n_sim = 10000                    # número de simulações
    
    # Executa a simulação
    resultados = simular_risco_caixa(
        saldo_inicial=saldo_inicial,
        horizonte=horizonte,
        mu_inflow=mu_inflow,
        sigma_inflow=sigma_inflow,
        mu_outflow=mu_outflow,
        sigma_outflow=sigma_outflow,
        n_sim=n_sim
    )
    
    # Exibe os resultados estatísticos
    df_stats = pd.DataFrame({
        "Parâmetro": ["Saldo Inicial (R$)", "Horizonte (dias)", "Média de Inflows (R$)", 
                      "Média de Outflows (R$)", "Simulações"],
        "Valor": [saldo_inicial, horizonte, mu_inflow, mu_outflow, n_sim]
    })
    
    print("Parâmetros da Simulação:")
    print(df_stats.to_string(index=False))
    print("\nResultados:")
    print(f"Probabilidade de Shortfall (Saldo Negativo): {resultados['prob_shortfall']*100:.2f}%")
    print(f"Média do Saldo Final: R$ {resultados['media_saldo_final']:.2f}")
    
    # Histograma do saldo final
    plt.figure(figsize=(10, 4))
    plt.hist(resultados["saldo_final"], bins=100, color='darkblue', alpha=0.7, density=True)
    plt.title("Distribuição do Saldo Final após 30 dias")
    plt.xlabel("Saldo Final (R$)")
    plt.ylabel("Densidade")
    plt.axvline(x=saldo_inicial, color='red', linestyle='--', label="Saldo Inicial")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    # Histograma do menor saldo registrado em cada simulação
    plt.figure(figsize=(10, 4))
    plt.hist(resultados["saldo_min"], bins=100, color='indianred', alpha=0.7, density=True)
    plt.title("Distribuição do Saldo Mínimo Durante o Horizonte")
    plt.xlabel("Saldo Mínimo (R$)")
    plt.ylabel("Densidade")
    plt.axvline(x=0, color='black', linestyle='--', label="Zero (Limite de Falta)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()
