import os
import subprocess as sp


def get_files(dir):
    lst=[file for file in os.listdir(dir) if not file.startswith(".")]
    return lst

def file_exist(file):
    # if file is found in any of the path return true else false
    with open("/om4/project/biobank/all_files.txt") as fp:
        for line in fp.readlines():
            if file in line:
                path=line.strip().replace("./", "/om4/project/biobank/")
                break
    return os.path.exists(path), path


if __name__ == '__main__':

    # load the list of untracked data
    list_path="/om4/project/biobank/tmp_dir/check_files"
    #list_path="ds_status.txt"
    ds_list=[]
    with open(list_path) as ls:
        ds_list=[line.strip().split()[0].split("_")[0] for line in ls.readlines()]

    prefix="/om4/project/biobank/ukb/inputs/subjects"
    ds_list=list(dict.fromkeys(ds_list))
    for ds in ds_list:
        directory=os.path.join(prefix,ds)
        file_list= get_files(directory)
        exist=[]
        for file in file_list:
            file_avail,_=file_exist(file)
            exist.append(file_avail)

        #subject_ID=ds.split("/")[-1]
        if sum(exist) == len(exist):
            # remove the whole dataset
            print(f"data found. {ds} is removed")
            # change the permission of the directory
            cmd=["chmod","-R","u+w",directory]
            p0=sp.run(cmd,stdout=sp.PIPE, stderr=sp.STDOUT ,text=True)
            # delete the folder
            p1=sp.run(["rm", "-rf", directory], stdout=sp.PIPE, stderr=sp.STDOUT ,text=True)
            print(p0.stdout)
            print(p1.stdout)
        else:
            # Add dataset name to a file to be checked manually
            print(f"data not founf.check {ds}")
            with open("/om4/project/biobank/tmp_dir/check_ds", "at") as fp:
                fp.writelines(f"{ds}\n")




