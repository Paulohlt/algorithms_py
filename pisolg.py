def pisolg(N):
    """
    Retorna o piso do logaritmo na base 2
    """
    n = 1
    i = 0
    if N <= 0:
            raise Exception("Value has to be positive")
    while n <= N/2: 
        n = n*2
        i += 1
    return i
