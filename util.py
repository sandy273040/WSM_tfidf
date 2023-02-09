import sys
import pandas as pd
import numpy as np

#http://www.scipy.org/
try:
	from numpy import dot
	from numpy.linalg import norm
	import numpy as np
except:
	print("Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?")
	sys.exit() 

def removeDuplicates(list):
	""" remove duplicates from a list """
	return set((item for item in list))


# def cosine(vector1, vector2):
# 	""" related documents j and q are in the concept space by comparing the vectors :
# 		cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
# 	return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))

def cosineMatrix(docs, queryVector, cos_len_list):
    cos = docs @ queryVector
    np.reshape(cos, (1, len(cos)))
    # print(cos)
    for (cos_value, cos_len) in zip(cos, cos_len_list):
        cos_value /= cos_len
    return cos

def euclidean(vector1, vector2):
	vector1 = np.array(vector1)
	vector2 = np.array(vector2)
	return float(np.linalg.norm(vector1-vector2))