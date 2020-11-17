import os
import json
import argparse


def get_key(dic):
    return list(dic)

def get_sbj_ids(data):
    """
    creates a list of subject ids based on saved list of dictionaries

    """
    # data is a list of dictionaries
    sbj_ID=[]
    for dic in data:
        sbj=get_key(dic)
        for id in sbj:
            sbj_ID.append(id)
    return sbj_ID

def get_index(data_list,elm):
    index=[i for i, j in enumerate(data_list) if j == elm ]
    return index

def get_elm(data_list,idx):
    return data_list[idx]


if __name__=="__main__":

    data_path="/om4/project/biobank/all_bulk_files/all_data.json"

    with open(data_path) as f:
        data = json.load(f) # list of all dictionaries

    list_id=get_sbj_ids(data)

    parser = argparse.ArgumentParser()
    parser.add_argument("--index",help="enter the index",action="store",type=int)
    parser.add_argument("--id",help="enter the id value",action="store",type=str)
    args = parser.parse_args()
    
    if args.index != None:
        index=args.index
        print(get_elm(list_id,index))

    if args.id:
        id=args.id
        print(get_index(list_id,id))


