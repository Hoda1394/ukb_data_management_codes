import os
import subprocess as sp
import json
import pydra
import typing as ty

@pydra.mark.task
def extract_info(dic) -> ty.NamedTuple("output", [("eid",ty.Any),("fid",ty.Any)]):
    eid=list(dic.keys())[0]
    fid=list(dic.values())[0]
    return eid,fid


@pydra.mark.task
def ukb_create_dataset(key_file,path,eid,f_id):
    """
    key_file: path for key_file
    eid: patient ID
    f_id: list of feild ids, realted to the patient ID

    """
    dset_path=os.path.join(path,eid)
    out=[]
    
    if not os.path.exists(dset_path):

        init_cmd=["datalad","ukb-init","-d", dset_path, eid] + f_id
    
        #print("============ initializing eid-{} ============".format(eid))
        p0=sp.run(["datalad","create","-d", dset_path], stdout=sp.PIPE, stderr=sp.STDOUT,text=True)
        out.append(p0.stdout)
        #print(p0.stdout)

        p1=sp.run(init_cmd, stdout=sp.PIPE, stderr=sp.STDOUT ,text=True)
        out.append(p1.stdout)
        #print(p1.stdout)
        
    #print("============== updating eid-{} ================".format(eid))
    p2=sp.run(["datalad", "ukb-update", "-k", key_file,"-d", dset_path], stdout=sp.PIPE, stderr=sp.STDOUT ,text=True)
    out.append(p2.stdout)
    #print(p2.stdout)
    return out

# define hook
def out_hook(wf,result,*args):
    print("======================================================================================")
    for out in result.output.out:
        print(out)



if __name__=="__main__":

    # 
    key="/om4/project/biobank/ukb/inputs/data/34746/k30805r34746.key"
    data_path="/om4/project/biobank/all_bulk_files/all_data.json"
    ds_path="/om4/project/biobank/ukb/inputs/subjects"
    

    with open(data_path) as f:
       data = json.load(f) # list of all dictionaries

    
    # workflow
    wf1=pydra.Workflow(name="wf1", input_spec=["x","key","path"],key=key, path=ds_path)
    wf1.split("x",x=data[3:6])
    wf1.add(extract_info(name="get_data", dic= wf1.lzin.x))
    wf1.add(ukb_create_dataset(name="init_update", key_file=wf1.lzin.key, path=wf1.lzin.path, eid=wf1.get_data.lzout.eid, f_id=wf1.get_data.lzout.fid ))
    wf1.set_output([("out", wf1.init_update.lzout.out)])
    wf1.hooks.post_run_task=out_hook


    with pydra.Submitter(plugin="cf",n_procs=20) as sub:
        sub(wf1)

    #print(wf1.result())



