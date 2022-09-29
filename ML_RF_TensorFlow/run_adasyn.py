# def 
#imports
import os
import pickle
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import enlighten

from IPython.core.display import HTML
from IPython.display import SVG, Image, display

#RDKit related imports
from rdkit import RDLogger
from rdkit.Chem import PandasTools, AllChem as Chem, Descriptors
from rdkit.ML.Descriptors.MoleculeDescriptors import MolecularDescriptorCalculator
from rdkit.Chem import Draw
from rdkit import DataStructs

#scikit imports
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import ADASYN
from sklearn.model_selection import cross_val_score, train_test_split, validation_curve
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV



#tensorflow
import tensorflow as tf
from tensorflow import keras
import tensorflow_decision_forests as tfdf

RDLogger.logger().setLevel(RDLogger.CRITICAL)

import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

cols = pd.read_csv('backup_df.csv', nrows=1).columns
dataframe = pd.read_csv('backup_df.csv', index_col=False, usecols=cols[1:])
PandasTools.AddMoleculeColumnToFrame(dataframe, 'PUBCHEM_CANONICAL_SMILES', 'ROMol', includeFingerprints=True)


RF_dataset = dataframe.copy()
PandasTools.RemoveSaltsFromFrame(RF_dataset)
RF_dataset['Active'] = np.NaN

for index, row in RF_dataset.iterrows():
    activity = row.PUBCHEM_ACTIVITY_OUTCOME
    if activity == 'Active':
        RF_dataset.loc[index, 'Active'] = 1
    else:
        RF_dataset.loc[index, 'Active'] = 0

RF_dataset['Active'] = RF_dataset['Active'].astype(int)

activity_binary = []
ECFP6s = []
topols = []
atom_pairs = []



pbar = enlighten.Counter(total=len(RF_dataset.index), desc='Calculating molecular descriptors', unit='ticks')

for ID, row in RF_dataset.iterrows():
    # print(i)

    mol = row.ROMol# if i == max_radius else row[f'FRAG_R{i}']          

    ECFP6_vec = Chem.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=2048)
    topol_vec =  Chem.GetHashedTopologicalTorsionFingerprintAsBitVect(mol, nBits=2048)
    atpair_vec = Chem.GetHashedAtomPairFingerprintAsBitVect(mol, nBits=2048)

    ECFP6s.append(ECFP6_vec)
    topols.append(topol_vec)
    atom_pairs.append(atpair_vec)



    # print(descriptor)
    activity_binary.append(row.PUBCHEM_ACTIVITY_OUTCOME)
    pbar.update()

length = len(ECFP6s)

if all(len(lst) == length for lst in [ECFP6s, topols, atom_pairs]):
    print('Lists are equal in length')
else:
    print('Lists are unequal in length')

ECFP6s_np = []
topols_np = []
atom_pairs_np = []

for i in range(len(ECFP6s)):
    ecfp_arr = np.zeros((1,))
    topol_arr = np.zeros((1,))
    atpair_arr = np.zeros((1,))


    ecfp = ECFP6s[i]
    topol = topols[i]
    atompair = atom_pairs[i]

    DataStructs.ConvertToNumpyArray(ecfp, ecfp_arr)
    DataStructs.ConvertToNumpyArray(topol, topol_arr)
    DataStructs.ConvertToNumpyArray(atompair, atpair_arr)

    ECFP6s_np.append(ecfp_arr)
    topols_np.append(topol_arr)
    atom_pairs_np.append(atpair_arr)

x_ecfp6 = ECFP6s_np
y = RF_dataset.Active

unique, counts = np.unique(y, return_counts=True)
dict(zip(unique, counts))

count_acts = sns.catplot(x='Active', kind="count", palette="ch:.25", data=RF_dataset)

print('creating synthetic datapoints')
x_ecfp6_ada, y_ecfp6_ada = ADASYN().fit_resample(x_ecfp6, y)
ecfp6_sample_count = sorted(Counter(y_ecfp6_ada).items())

pickle.dump(x_ecfp6_ada, 'x_ecfpada.p')
pickle.dump(y_ecfp6_ada, 'y_ecfpada.p')


print('completed')






















