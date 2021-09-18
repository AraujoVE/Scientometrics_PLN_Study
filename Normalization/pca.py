import numpy as np
from numpy.core.fromnumeric import amin


# needless formula, once we have np.cov
'''
def covariance(array):
    array = array - np.mean(array,axis=0)
    return np.dot(np.transpose(array),array)/(np.shape(array)[0] - 1)
'''

#Ex.: Array 5x3, onde cada linha é uma sample e cada coluna um measurement 
#PCA


def pca(array,newDim=2):
    stArray = (array - np.mean(array,axis=0)) / np.std(array,axis=0) # Standardization (5,3)
    covArray = np.cov(stArray,rowvar=False) # Covariance Matrix (3,3)
    eigVal, eigVec = np.linalg.eig(covArray) # Eigenvalues (3) and Eigenvectors (3,3)
    eigVec = eigVec[:,eigVal.argsort()[::-1]] # Order eigenvectors in respect to eigenvalues (3,3)
    newArray = np.dot(np.transpose(eigVec),np.transpose(stArray)).transpose()[:,:newDim]
    #                (        3,3        )(         3,5         ) (   5,3   ) (5,newDim)       
    return (newArray - np.amin(newArray)) / (np.amax(newArray) - np.amin(newArray)) # Normalization (5,newDim)
