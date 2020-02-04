import pandas as pd
import csv
from abc import ABC, abstractmethod 

df = pd.read_csv("gene_table.csv", delimiter=",")

class Project(ABC):

	@abstractmethod 	#part 2 needs abstract methods
	def record(self):	#remember to define the method everytime you implement a new class
		pass

class Number(Project):		#recording the numerical metadata consisting of the number of rows and columns of the dataset

	def record(self):
		return(df.shape)

class Semantics(Project):	#recording the general semantics of the dataset, i.e. the labels of the columns

	def record(self):
		return df.columns.values		#to get the labels of the rows --> df.index.values

class Genes(Project):		#recording the number of genes for each biotype. The list should be sorted in ascending order

	def record(self):
		number_genes=df.groupby('gene_biotype')['gene_biotype'].count()		#total number of genes for each biotype
		return number_genes.sort_values(ascending=True).to_frame().rename(columns={"gene_biotype": "number of genes"}).reset_index()	#Pandas Series.to_frame()	
	
class AssociatedGenes(Project):		#recording, given a certain biotype as input, the list of associated genes

	def record(self):
		return df.groupby('gene_biotype')['gene_name'].apply(lambda group_series:group_series.tolist()).to_dict()		#.reset_index()???
	
class Chromosomes(Project):	#recording the number of chromosomes in the dataset

	def record(self):
		return len(set(df.loc[:,'chromosome']))

class NumberOfGenes(Project):	#recording the number of genes for each chromosome. The list should be sorted in ascending order

	def record(self):
		number_genes=df.groupby('chromosome')['chromosome'].count()			#total number of genes for each chromosome
		return number_genes.sort_values(ascending=True).to_frame().rename(columns={"chromosome": "genes for each chromosome"}).reset_index()
		
		
class PlusStrand(Project):

	def record(self):
		df_tot = df.groupby('chromosome')['chromosome'].count()  # create a dataframe with chromosomes and number of total genes on the chromosome
		df_tot = pd.DataFrame(df_tot.items(), columns=['chromosome', 'tot_genes']).sort_values(by=['chromosome']).set_index('chromosome')  # rename the columns, put the chromosomes in order and change the index into the chromosome column
		df_plus = df[df['strand'] == '+'].groupby('chromosome')['chromosome'].count()  # select all the rows with plus strand and count how many genes per chromosome
		df_plus = pd.DataFrame(df_plus.items(), columns=['chromosome', 'plus_genes']).sort_values(by=['chromosome']).set_index('chromosome')  # change the columns' names and put the chromosome in order and change the index into the chromosome column
		df_tot['plus_genes'] = df_plus['plus_genes']  # create a new column of the first dataframe where pandas associates to each chromosome(index) the value of the second dataframe's column. where pandas doesn't find a corresponding number it writes Nan
		df_tot = df_tot.reset_index()  # reset index to numbers
		df_tot['percentage'] = df_tot['plus_genes'] * 100 // df_tot['tot_genes']
		return df_tot.loc[:, ['chromosome', 'percentage']].fillna(0)

class MinusStrand(Project):

	def record(self):
		df_tot = df.groupby('chromosome')['chromosome'].count()  # create a dataframe with chromosomes and number of total genes on the chromosome
		df_tot = pd.DataFrame(df_tot.items(), columns=['chromosome', 'tot_genes']).sort_values(by=['chromosome']).set_index('chromosome')  # rename the columns, put the chromosomes in order and change the index into the chromosome column
		df_minus = df[df['strand'] == '-'].groupby('chromosome')['chromosome'].count()  # select all the rows with minus strand and count how many genes per chromosome
		df_minus = pd.DataFrame(df_minus.items(), columns=['chromosome', 'minus_genes']).sort_values(by=['chromosome']).set_index('chromosome')  # change the columns' names, put the chromosome in order and change the index into the chromosome column
		df_tot['minus_genes'] = df_minus['minus_genes']  # create a new column of the first dataframe where pandas associates to each chromosome(index) the value of the second dataframe's column. where pandas doesn't find a corresponding number it writes Nan
		df_tot = df_tot.reset_index()  # reset index to numbers
		df_tot['percentage'] = df_tot['minus_genes'] * 100 // df_tot['tot_genes']
		return df_tot.loc[:, ['chromosome', 'percentage']].fillna(0)
