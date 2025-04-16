import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def simular_risco_seguro_vida(
    n_clientes: int,
    p_morte: float,
    sum_assegurado: float,
    reservas: float,
    n_sim: int = 10000,
    seed: int = 42
) -> dict:
    """
    Simula os sinistros de uma carteira de seguros de vida e estima o risco de que as reservas 
    da seguradora sejam insuficientes para cobrir os pagamentos dos sinistros.

    Parâmetros:
      - n_clientes     : Número de clientes segurados (por exemplo, 12.000).
      - p_morte        : Probabilidade anual de óbito de cada cliente.
      - sum_assegurado : Valor do seguro (pagamento por sinistro).
      - reservas       : Montante de reservas disponível para cobrir os sinistros.
      - n_sim          : Número de simulações de Monte Carlo.
      - seed           : Semente para reprodutibilidade.

    Retorna um dicionário com:
      - prob_fail   : Probabilidade de as reservas não serem suficientes.
      - claims_sim  : Array com o total de sinistros (valor pago) em cada simulação.
      - media_claims: Média dos sinistros simulados.
      - std_claims  : Desvio padrão dos sinistros.
    """
    np.random.seed(seed)
    
    # Para cada simulação, o número de sinistros (óbitos) é modelado como uma variável
    # binomial: cada um dos n_clientes pode falecer com probabilidade p_morte.
    mortes = np.random.binomial(n=n_clientes, p=p_morte, size=n_sim)
    
    # Valor total dos sinistros em cada simulação
    claims_sim = mortes * sum_assegurado
    
    # A reserva é insuficiente se o total dos sinistros superar o valor das reservas
    falhas = claims_sim > reservas
    prob_fail = np.mean(falhas)
    
    media_claims = np.mean(claims_sim)
    std_claims = np.std(claims_sim, ddof=1)
    
    return {
        "prob_fail": prob_fail,
        "claims_sim": claims_sim,
        "media_claims": media_claims,
        "std_claims": std_claims,
        "n_sim": n_sim
    }

def main():
    # Parâmetros do problema
    n_clientes = 12000             # Carteira de 12.000 clientes
    p_morte = 0.01                 # Probabilidade anual de óbito (1% por cliente)
    sum_assegurado = 100000.0      # Valor do seguro por cliente (R$ 100.000)
    reservas = 12_000_000.0        # Reservas da seguradora (R$ 12.000.000)
    n_sim = 10000                # Número de simulações de Monte Carlo
    
    # Executa a simulação de risco
    resultados = simular_risco_seguro_vida(n_clientes, p_morte, sum_assegurado, reservas, n_sim)
    
    # Exibe os parâmetros da simulação
    df_params = pd.DataFrame({
        "Parâmetro": [
            "Número de Clientes", 
            "Probabilidade de Morte (anual)", 
            "Valor do Seguro (R$)",
            "Reservas (R$)",
            "Simulações"
        ],
        "Valor": [n_clientes, p_morte, sum_assegurado, reservas, n_sim]
    })
    
    print("Parâmetros da Simulação:")
    print(df_params.to_string(index=False))
    print("\nResultados da Simulação:")
    print(f"Probabilidade de Reservas Insuficientes: {resultados['prob_fail']*100:.2f}%")
    print(f"Média dos Sinistros: R$ {resultados['media_claims']:.2f}")
    print(f"Desvio Padrão dos Sinistros: R$ {resultados['std_claims']:.2f}")
    
    # Plot do histograma do valor total dos sinistros simulados
    plt.figure(figsize=(10, 4))
    plt.hist(resultados["claims_sim"], bins=100, color='steelblue', alpha=0.7, density=True)
    plt.axvline(x=reservas, color='red', linestyle='--', label="Reservas Disponíveis")
    plt.title("Distribuição dos Sinistros Totais (12.000 Clientes)")
    plt.xlabel("Total dos Sinistros (R$)")
    plt.ylabel("Densidade")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()
