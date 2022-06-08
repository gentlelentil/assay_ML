#creates a list of the MeSH classifications from the CID of a compound on PubChem

import requests
from xml.etree import ElementTree as ET
import pubchempy as pcp
import urllib.parse as urlp

URL_STEM = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/'

#cid = 2244

def get_cid_MeSH(cid):
    """
    Get all the MeSH classifications from a CID.
    Returns list of the MeSH descriptions.
    """
    # MeSH_refs = []
    MeSH_names = []

    MeSH_stem = f'{cid}/XML?heading=MeSH+Pharmacological+Classification'
    MeSH_request = urlp.urljoin(URL_STEM, MeSH_stem)
    #make request
    MeSH_data = requests.get(MeSH_request)
    root = ET.fromstring(MeSH_data.content)
    #get the MeSH tree root
    mesh = root.findall('.//{http://pubchem.ncbi.nlm.nih.gov/pug_view}Information')

    for i in mesh:
        #get MeSH reference
        # meshref = i.find('{http://pubchem.ncbi.nlm.nih.gov/pug_view}ReferenceNumber').text
        #get MeSH name
        meshname = i.find('{http://pubchem.ncbi.nlm.nih.gov/pug_view}Name').text
        MeSH_names.append(meshname)
    return MeSH_names

def get_cid_from_SMILES(smiles):
    cid = pcp.get_cids(smiles, 'smiles')
    return cid

aspirin_mesh = get_cid_MeSH(1988)
for i in aspirin_mesh:
    print(i)
