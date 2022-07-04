#Returns the list of compounds from a selected assay on PubChem.
#Includes molecule SID, AID, CID, activity (active/inactive)
#Returns as: [index, AID, SID, CID, activity]

#NOTE The issue of 10000+ SIDs remains, have to create a csv and append the values into this.

import requests
import csv
import urllib.parse as urlp
from xml.etree import ElementTree as ET
# import sys
# import pickle
import enlighten


URL_STEM = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/'

def get_num_cids(assay):
    summary_url = f'assay/aid/{assay}/summary/XML'
    request = urlp.urljoin(URL_STEM, summary_url)
    data = requests.get(request)
    root = ET.fromstring(data.content)
    num_cids = int(root.find('.//{http://pubchem.ncbi.nlm.nih.gov/pug_rest}CIDCountAll').text)
    return num_cids


def check_assay_length(assay):
    listkey = None
    listurl = f'assay/aid/{assay}/sids/XML?list_return=listkey'
    request = urlp.urljoin(URL_STEM, listurl)
    data = requests.get(request)
    root = ET.fromstring(data.content)
    assay_size = int(root.find('{http://pubchem.ncbi.nlm.nih.gov/pug_rest}Size').text)
    print(f'Number of substances tested in assay AID {assay} are: {assay_size}')
    if assay_size > 9999:
        print("Assay size is over 10,000\nThis exceeds the max number of lines that can be requested at once.")
        listkey = listkey = root.find('{http://pubchem.ncbi.nlm.nih.gov/pug_rest}ListKey').text
        # return listkey, assay_size
    return listkey, assay_size




def create_URL(assay):
    URL_STEM = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/'
    #CSV is the only way to get CIDs alongside SIDs
    assay_url = f'assay/aid/{assay}/CSV'
    request = urlp.urljoin(URL_STEM, assay_url)
    return request

def get_assay_info(request, AID, listkey=None, assay_size=None):
    if listkey == None:
        print(f'Requesting info of assay {AID}')
        with requests.Session() as sesh:
            download = sesh.get(request)

            decoded = download.content.decode('utf-8')
            reader = csv.reader(decoded.splitlines(), delimiter=',')
            aid_list = list(reader)
            
            cleanedlist = []
            CIDs = []

            for ID, i in enumerate(aid_list):
                if ID == 0:
                    #header line
                    # header = [i[0], 'PUBCHEM_ASSAY_ID', i[1], i[2], i[3]]
                    header = ['PUBCHEM_ASSAY_ID', i[1], i[2], i[3], i[4]]
                    cleanedlist.append(header)
                    continue
                try: 
                    int(i[0]) == 1
                except ValueError:
                    #line is descriptive
                    continue
                if i[2] == '':
                    #CID is missing/not present
                    i[2] = 0
                    #continue

                # line = [int(i[0]), AID, int(i[1]), int(i[2]), i[3]]
                line = [AID, int(i[1]), int(i[2]), i[3], int(i[4])]
                cleanedlist.append(line)
                CIDs.append(int(i[2]))
    
    else:
        count = 0
        iter = 10000 #
        cleanedlist = []
        CIDs = []
        print(f'Requesting info of assay {AID}')
        pbar = enlighten.Counter(total=(round(assay_size/iter)), desc=f'Downloading AID: {AID}...', unit='ticks')
        while count < (assay_size - 1):
            # if count > 30000:
            #     break
            #start = count
            if (count + iter) > assay_size:
                iter = (assay_size - count) #-1
            iter_req = f'?sid=listkey&listkey={listkey}&listkey_start={count}&listkey_count={iter}'
            # print(f'Requesting index {count} to {count + iter} of assay {AID}')
            request = urlp.urljoin(request, iter_req)

            with requests.Session() as sesh:
                download = sesh.get(request)
                decoded = download.content.decode('utf-8')
                reader = csv.reader(decoded.splitlines(), delimiter=',')
                aid_list = list(reader)

                for ID, i in enumerate(aid_list):
                    if ID == 0 and count ==0:
                        #header line
                        #header = [i[0], 'PUBCHEM_ASSAY_ID', i[1], i[2], i[3]]
                        header = ['PUBCHEM_ASSAY_ID', i[1], i[2], i[3], i[4]]
                        cleanedlist.append(header)
                        continue
                    try: 
                        int(i[0]) == 1
                    except ValueError:
                        #line is descriptive
                        continue
                    if i[2] == '':
                        #CID is missing/not present
                        i[2] = 0
                        continue

                    #line = [int(i[0]), AID, int(i[1]), int(i[2]), i[3]]
                    line = [AID, int(i[1]), int(i[2]), i[3], int(i[4])]
                    cleanedlist.append(line)
                    CIDs.append(int(i[2]))
            pbar.update()
            count += iter
            # print(count)
        print("Done.")
        print(f'Assay {AID} has been successfully downloaded.')



        #throw it all in a pickle file for whatever
        # with open(f'{AID}_info.p', 'wb') as ifile:
        #     pickle.dump(cleanedlist, ifile)

    #return the list of assay info, form is [index, AID, SID, CID, activity]
    return cleanedlist#, CIDs

def get_data_AID_csv(assay):
    #check assay size:
    listkey, assay_size = check_assay_length(assay)
    if listkey == None:
        request = create_URL(assay)
        assay_data = get_assay_info(request, assay)
    else:
        request = create_URL(assay)
        assay_data = get_assay_info(request, assay, listkey, assay_size)
        #have to create a function that compiles a csv

    if (len(assay_data) - 1) != assay_size:
        print(len(assay_data) - 1)
        print(assay_size)
        print("Error in download")
        print("Total number of downloaded compounds is less than the actual number of compounds")
        # raise ValueError

    #This doesn't work because PubChem is inconsisten with SIDs and CIDs, often both are present
    # #small checksum
    # total_cids = get_num_cids(assay)
    # if len(assay_data) - 1 != total_cids:
    #     print(len(assay_data) - 1)
    #     print(total_cids)
    #     raise ValueError

    # print(request)
    return assay_data




# if __name__ == '__main__':
#     print("Should be called from main")