def rec_soma_esqdir(k,n, A):
    """"
    Soma recursivamente, da esquerda para direita, 
    k termos termos de uma lista A de n termos.   
    """
    if k > n:
        s = 0
    else:
        s = rec_soma_esqdir(k+1,n,A) + A[k]
    return s