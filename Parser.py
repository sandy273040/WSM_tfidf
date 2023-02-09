#http://tartarus.org/~martin/PorterStemmer/python.txt
from PorterStemmer import PorterStemmer
import jieba
import string
import re
# from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

class Parser:

	#A processor for removing the commoner morphological and inflexional endings from words in English
	stemmer=None

	stopwords=[]
	# chineseStopwords = []

	def __init__(self,):
		self.stemmer = PorterStemmer()

		#English stopwords from ftp://ftp.cs.cornell.edu/pub/smart/english.stop
		self.stopwords = open('C:\\Users\\USER\\py_workspace\\wsm-codes\\english.stop', 'r').read().split()
		# self.chineseStopwords = open('C:\\Users\\USER\\py_workspace\\wsm-codes\\stopwords.txt', 'r', encoding='utf-8').read().split('\n')
		# jieba.set_dictionary('C:\\Users\\USER\\py_workspace\\wsm-codes\\dict.txt.big.txt')

	def clean(self, string):
		""" remove any nasty grammar tokens from string """
		string = string.replace(".","")
		string = string.replace("\s+"," ")
		string = string.lower()
		return string
	

	def removeStopWords(self,list):
		""" Remove common words which have no search value """
		return [word for word in list if word not in self.stopwords ]


	def tokenise(self, string, chinese=False):
		""" break string up into tokens and stem words """
		if chinese == True:#input a list of strings(aka documents)
			additional_words = []
			for word in string:#a document
				word = self.clean(word)
				word = [self.preprocessing(w) for w in word]
				for w in word: w = w.replace('', r'　')
				word = ''.join(word)
				
				words_in_word = jieba.lcut(word, cut_all = False)
				# words_in_word = [w for w in words_in_word if w not in self.chineseStopwords]
				words_in_word = [w for w in words_in_word if w != ' ']
				# print('jieba', words_in_word, sep='\t')
				additional_words.extend(words_in_word)
				# print('additional', additional_words, sep='\t')
			words = additional_words
		else:#english input a document string, clean it and split string into a list of words
			string = self.clean(string)
			words = string.split(' ')#words is list of words of all the sentences
   
		#stemmatization on each single word
		return [self.stemmer.stem(word,0,len(word)-1) for word in words if word != '']

	def preprocessing(self, x):
		for i in string.punctuation:#清理半形標點符號
			x = x.replace(i, " ")
		x = re.sub(r"\n", "", x)
		x = x.replace("“", "")
		x = x.replace("”", "")
		x = x.replace(' ', " ")
		x = x.replace('，', ' ')
		x = x.replace('。', ' ')
		x = x.replace('「', ' ')
		x = x.replace('」', ' ')
		x = x.replace(',', ' ')
		x = x.replace('／', ' ')
		x = x.replace('！', ' ')
		x = x.replace('？', ' ')
		x = x.replace('》', ' ')
		x = x.replace('《', ' ')
		x = x.replace('：', ' ')
		x = x.replace('（', ' ')
		x = x.replace('）', ' ')
		x = x.replace(r"\s+"," ")
		x = x.replace('、', '')
		x = x.replace('｜', '')
		x = x.replace('【', '')
		x = x.replace('】', '')
		return x


