# -*- coding: utf-8 -*-

"""Main module."""
from pathlib import Path
import data_preparation
import dbpResourceFinder
import dbpediaqueries
import dbpedia_graph_extraction
import dbpedia_graph_extraction_phase2
import combining_dbpediaconcepts
import abstract_tokenizer
def main():
    input_path = Path.cwd().parent.joinpath("text", "process.txt")
    if input_path.exists():
        """ 
        This function cleans the unstructured text, removes the stopwords and does tokenization of the text into unigram, bigrams and trigrams.
        It also generates the initial reference context for the COBEC phase-1 ranking". 
        Parameters: 
        Input_path: Path to the input text file
        unigram_frequency: the threshold to keep unigrams for further process, default is 5 for short/medium textual documents i.e a chapter,
        but for the longer text more is recommended. 
        bigram_frequency: the threshold to keep bigrams for further process, default is 4 for short/medium textual documents i.e a chapter, 
        but for the longer text more is recommended. 
        trigram_frequency: the threshold to keep trigrams for further process, default is 2 for short/medium textual documents i.e a chapter, 
        but for the longer text the more is recommended. 

        """
        temp_path = Path.cwd().parent.joinpath("temp")

        #data_preparation.ngrams_preparation(input_path, temp_path, unigram_frequency=5, bigram_frequency=4, trigram_frequency=2, )
        print("Step-1: Data is pre-processed and tokenized into 1-gram, 2-grams, and 3-grams")
        """
        This filtration stage filters those n-grams for which there does not exist a Uniform Resource Identifier(URI) in DBpedia.
        """
        path_resultphase1 = Path.cwd().parent.joinpath("output", "phase1")
        #dbpResourceFinder.dbpedia_existence_check(temp_path, path_resultphase1)
        print("Step-2: The n-grams are filtered using DBpedia")
        """
        The filtered n-grams are ranked using the associated DBpedia abstract of a candidate concept. This phase also combines the semantically or logically similar
        concepts together
        """
        #Results=dbpedia_graph_extraction.ranking_phase1(path_resultphase1)
        #print("Step-3: Concepts are ranked by COBEC phase-1 ","\n",Results)

        """
        This function extracts the subgraph from DBpedia for top-n (default n=5) ranked concepts from phase1 of COBEC and updated the context.
        """
        path_totoprankedconcepts = Path.cwd().parent.joinpath("output", "phase1")
        combining_dbpediaconcepts.contextupdate(path_totoprankedconcepts)
        print("Step-4: The context information is updated")
        """
        This function re-ranks the candidate concepts using the updated context information
        """
        path_resultphase2 = Path.cwd().parent.joinpath("output", "phase2")
        Results=dbpedia_graph_extraction_phase2.ranking_phase2(path_resultphase2)
        print("Final step: Concepts are re-ranked by COBEC phase-2 ","\n",Results)

if __name__ == "__main__":
    main()


