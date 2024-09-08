def rec_soma(n, A):
    """"
    Soma recursivamente n termos de uma lista A,  
    """
    if n == 0:
        s = A[n]
    else:
        s = rec_soma(n-1,A) + A[n]
    return s