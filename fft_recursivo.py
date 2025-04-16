# fft_recursivo.py

import numpy as np

def fft(x):
    N = len(x)
    if N <= 1:
        return x
    elif N % 2 != 0:
        raise ValueError("Tamanho da entrada deve ser potência de 2.")

    X_even = fft(x[::2])
    X_odd = fft(x[1::2])
    factor = np.exp(-2j * np.pi * np.arange(N) / N)

    return np.concatenate([X_even + factor[:N // 2] * X_odd,
                           X_even - factor[:N // 2] * X_odd])

if __name__ == "__main__":
    # Exemplo de uso
    x = np.random.random(8)
    X = fft(x)
    print("Sinal:", x)
    print("FFT:", X)