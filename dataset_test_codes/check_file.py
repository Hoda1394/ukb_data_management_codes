import os
from data_check import *


if __name__ == '__main__':

	ds_list="/om4/project/biobank/tmp_dir/check_ds"
	list=[]
	with open(ds_list) as chk_ls:
		list=[line.strip() for line in chk_ls.readlines()]

	prefix="/om4/project/biobank/ukb/inputs/subjects"

	for ds in list:
		dir=os.path.join(prefix,ds)
		file_list= get_files(dir)
		for file in file_list:
			exist,path=file_exist(file)
			if not exist:
				with open("/om4/project/biobank/tmp_dir/check_files", "at") as fp:
					fp.writelines(f"{file} not in {path}\n")

