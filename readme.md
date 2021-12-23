# Readme

## Overview
This repository contains the source code for our paper "Context-based Extraction 
of Concepts from Unstructured Textual Documents". Furthermore, it contains our 
three newly created data sets from the domains Data Mining (DM), Database 
Management Systems (DB), and Operating Systems (OS). 

## Abstract
COBEC is a novel unsupervised method for extracting the relevant concepts from 
a collection of unstructured textual documents assuming that the documents are 
related to a certain topic. Our two-step method first identifies candidate 
concepts from the textual documents, then infers the context information for 
the input documents and finally ranks them with respect to the inferred 
context. In the second step this context information is enriched with more 
abstract information to improve the ranking process. In the experimental 
results our method outperforms seven supervised and unsupervised approaches 
on five datasets and is competitive on the other two. Furthermore, we release 
three new benchmark datasets that were created from books in the educational 
domain.

## Project structure
Our repository is structured as follows:
* ``` data: ``` contains our 3 newly created data sets DM, DB, OS
* ``` src: ``` actual source code
  * ``` COBEC.py ``` running this script runs generates outputs for a specified dataset
* ``` text: ``` contains a single input text document (.txt) that represents the text from 
which concepts will be extracted with COBEC
* ``` output: ``` contains the results (=concepts) of an input dataset
* ``` temp: ``` contains the preprocessed texts of a dataset -> will be created automatically
* ``` requirements.txt ``` contains all libraries to be installed to run our code

## Installation
Install all libraries in requirements.txt

## How to run
Run COBEC.py to extract concepts from a given dataset. 

**Note that the current 
version of our code takes as input a single dataset and stores its extracted 
concepts in output/. This means that if you want results for two datasets,
you first run COBEC.py, then save the results from outputs/ manually somewhere 
else, because when running COBEC.py again, existing results in output/ will be 
overridden.**

## Interpreting results
The list of all ranked concepts (for phase 1 and phase 2, respectively) are stored in output/phase1/ranked_concepts.json and output/phase2/ranked_concepts.json

The output is in the following format:
```
{"1": [["Interrupt_handler", "Handler"], "Interrupt handler"], "2": ["Program", "Computer programming"],...}
```
The key in the dictionary is the rank and concepts ranked at the top are more likely to be concepts. The value of each rank contains two entries, where the first one is either a list or a string. This entry contains the candidate concepts from the unstructured input text. If there are semantically or logically similar concepts, it will be a list of candidate concepts, otherwise it will be a string. The second entry of corresponds to the DBpedia label for those candidate concepts. For example, the most likely candidate concepts in the raw text according to the above result are "Interrupt_handler" and "Handler" which are both mapped to the DBpedia label "Interrupt handler". Likewise, on the second rank there is the candidate concept "Program" which is mapped to the DBpedia label "Computer programming".

## How to extract concepts from other data sets using our code
Add your raw, unstructured text file in text/, then run COBEC.py.
The text file represents the text from which concepts should be extracted. 
Please, keep in mind that if you want to combine multiple texts, you should 
just merge them into a single file that you add in texts/.
Moreover, as noted in the paper, COBEC assumes that all identified concepts in
that text file are related to an overarching topic. For example,
combining multiple chapters of a book about data mining into a single text 
file, is possible because all chapters are related to the topic "data mining".
In contrast, if you combine a chapter from a chemistry book with a chapter from
a data mining book, COBEC will identify concepts, but most likely they won't be 
accurate, as both chapters don't share an overarching topic.



## Data sets
Our three newly created data sets are included in inputs/ and their creation is  
described in our paper. Their main characteristics are listed below (Taken from Table 1 in our paper).

| Data set | #Documents | #Words/Document | #Gold concepts | Document length | Avg. #gold concepts per document |       Topic       | #Gold concepts with > 3 words |
|:--------:|:----------:|:---------------:|:--------------:|:---------------:|:--------------------------------:|:-----------------:|:-----------------------------:|
|   DM	    |     20     |     	15530	     |      477	      |    29 pages	    |              23.85	              |    Data Mining    |              	4               |	  
|   DB	    |     27     |     	10994	     |      395	      |    26 pages	    |              14.63	              |     Databases     |              	0               |	   
|   OS	    |     1      |     	4834	      |      43	       |    19 Pages	    |               43	                | Operating Systems |              	0               |	 


## Citation
If you use our source code or data sets, please cite our paper:

@article{GUL2021context,
title = {Context-based Extraction of Concepts from Unstructured Textual Documents},
journal = {Information Sciences},
year = {2021},
issn = {0020-0255},
doi = {https://doi.org/10.1016/j.ins.2021.12.056},
url = {https://www.sciencedirect.com/science/article/pii/S0020025521012779},
author = {Saima Gul and Stefan Räbiger and Yücel Saygın}
}
