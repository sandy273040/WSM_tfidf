from pprint import pprint
from Parser import Parser
import util
import nltk

class VectorSpace:
    """ A algebraic model for representing text documents as vectors of identifiers. 
    A document is represented as a vector. Each dimension of the vector corresponds to a 
    separate term. If a term occurs in the document, then the value in the vector is non-zero.
    """

    #Collection of document term vectors
    documentVectors = []

    #Mapping of vector index to keyword
    vectorKeywordIndex=[]

    #Tidies terms
    parser=None
    
    #a list of unique vocabulary after word tokenization, and stopwords removal
    # uniqueVocabularyList = []


    def __init__(self, documents=[], chinese=False):#建構元
        self.documentVectors=[]
        self.parser = Parser()#produce instance variable of the class Parser
        # print('documents ', documents)
        if(len(documents)>0):
            self.build(documents, chinese)

    def build(self,documents, chinese):#create空間 for documents
        """ Create the vector space for the passed document strings """
        self.vectorKeywordIndex = self.getVectorKeywordIndex(documents, chinese)
        # for document in documents:
        #     self.check(document, chinese)#index check
        if chinese == True:#input list of lists(doc)
            self.documentVectors = [self.makeVector([document], chinese) for document in documents]
        else:#input string
            self.documentVectors = [self.makeVector(document, chinese) for document in documents]
        
        #stuffed with zero to avoid key error
        for document in self.documentVectors:
            document.extend([0] * ((len(self.vectorKeywordIndex) - len(document))))

        # print(self.vectorKeywordIndex)
        # print(self.documentVectors)


    def getVectorKeywordIndex(self, documentList, chinese=False):#for documents
        """ create the keyword associated to the position of the elements within the document vectors """
        
        #a list of keywords
        if chinese == True:
            vocabularyList = self.parser.tokenise(documentList, chinese)
        else:
            vocabularyString = " ".join(documentList)#Mapped documents into a single word string	
            vocabularyList = self.parser.tokenise(vocabularyString, chinese)
            #Remove common words which have no search value
            vocabularyList = self.parser.removeStopWords(vocabularyList)
        
        uniqueVocabularyList = util.removeDuplicates(vocabularyList)

        vectorIndex={}# a dictionary: word:position
        offset=0
        #Associate a position with the keywords which maps to the dimension on the vector used to represent this word
        for word in uniqueVocabularyList:
            vectorIndex[word]=offset
            offset+=1
        return vectorIndex  #(keyword:position)
    
    def makeVector(self, wordString, chinese=False):#for query
        """ @pre: unique(vectorIndex) """

        #for query, to make string query a term vector
        #Initialise vector with 0's
        vector = [0] * len(self.vectorKeywordIndex)
        wordList = self.parser.tokenise(wordString, chinese)
        wordList = self.parser.removeStopWords(wordList)
        
        # for word in self.uniqueVocabularyList:
        for word in wordList:
            if self.vectorKeywordIndex.get(word) == None:
                self.vectorKeywordIndex[word] = len(self.vectorKeywordIndex)
                # vector[len(self.vectorKeywordIndex)] = 1
                vector.append(1)
            else:
                vector[self.vectorKeywordIndex[word]] += 1; #Use simple Term Count Model
        #vector's each dimension means the frequency of the term in query
        return vector

    #query string: the input is the list not string!!!
    def buildQueryVector(self, termList):
        """ convert query string into a term vector """
        query = self.makeVector(" ".join(termList))
        return query


    def related(self,documentId):
        """ find documents that are related to the document indexed by passed Id within the document Vectors"""
        ratings = [util.cosine(self.documentVectors[documentId], documentVector) for documentVector in self.documentVectors]
        ratings.sort(reverse=True)
        return ratings


    def search(self,searchList):
        """ search for documents that match based on a list of terms """
        #return list of score of each document
        queryVector = self.buildQueryVector(searchList)

        ratings = [util.cosine(queryVector, documentVector) for documentVector in self.documentVectors]
        ratings.sort(reverse=True)
        return ratings
    #算相似度用matrix
    
    def feedback(self, fb_doc, queryVector):
        ''' 1: tokenize and tag pos for feedback doc(fb_doc) since we only need noun and verb
            2: build vector based on the result from step1
            3: then get noun and verb to make new query to get relevance feedback 
            return adjusted ratings for each doc from adjusted query vector'''
        text = nltk.word_tokenize(fb_doc)
        pos_tagged = nltk.pos_tag(text)

        feedbackQueryList = [item[0] for item in filter(lambda x:x[1][:2]=='NN' or x[1][:2]=='VB',pos_tagged)]
        feedbackQueryVector = self.buildQueryVector(feedbackQueryList)
        #if len(queryVector)==0: queryVector = self.buildQueryVector(self.queryList)

        queryVector = [original + 0.5 * feedback for original, feedback in zip(queryVector,feedbackQueryVector)]
        
        return queryVector

###################################################
