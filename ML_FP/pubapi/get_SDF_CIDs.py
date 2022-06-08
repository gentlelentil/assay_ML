#Downloads and creates a combined Structure Data File (.sdf)

#maybe not necessary
# import get_data_AID_csv

import requests
import sys
import urllib.parse as urlp
import os
import enlighten

URL_STEM = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/'

# test
# https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/2244/SDF

sdf_list = [2244, 1000]

def download_sdf(cid):
    #pubchem URL
    sdf_cid_url = f'compound/cid/{cid}/SDF'
    sdf_request = urlp.urljoin(URL_STEM, sdf_cid_url)
    SDF = requests.get(sdf_request)

    return SDF

    # with open('test.sdf', 'wb') as sdfile:
    #     sdfile.write(SDF.content)

#now write the sdf file to the main ones

# for i in sdf_list:
#     sdf_content = download_sdf(i)
#     with open(sdf_name, 'ab') as sdfile:
#         sdfile.write(sdf_content.content)

def compile_SDFs(cid_list, name=None):
    #create sdf_file
    if name == None:
        filename = 'compounds.sdf'
    else:
        filename = name + '.sdf'
    cwd = os.getcwd()
    try:
        os.mknod((os.path.join(cwd, filename)))
    except FileExistsError:
        print("SDF already exists")
        sys.exit()

    pbar = enlighten.Counter(total=(len(cid_list)), desc='Compiling SDFs...', unit='ticks')

    for i in cid_list:
        sdf_content = download_sdf(i)
        with open(filename, 'ab') as combined:
            combined.write(sdf_content.content)
        pbar.update()

