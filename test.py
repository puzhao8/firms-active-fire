
from http.client import responses
import os
# from prettyprinter import pprint
import subprocess

# task_id = "AV2U5GPNAH6QD5NS2527B7PR"
# check_upload_status = f"earthengine task info {task_id}"
# status = subprocess.getstatusoutput(check_upload_status)
# state = status[1].split("\n")[1].split(": ")[-1]

# pprint({task_id: state})


# asset_id = "users/omegazhangpzh/NRT_AF/J1_VIIRS_C2_Global_48h"
# remove_asset = f"earthengine rm {asset_id} --dry_run"
# status = subprocess.getstatusoutput(remove_asset)

# pprint(status)

# NRT_AF = subprocess.getstatusoutput("earthengine ls users/omegazhangpzh/NRT_AF/")
# asset_list = NRT_AF[1].replace("projects/earthengine-legacy/assets/", "").split("\n")

# for asset_id in asset_list:
#     print()
#     print(asset_id)
#     # os.system(f"earthengine acl set public {asset_id}")
#     # os.system(f"earthengine acl get {asset_id}")


task_id = "V3RVZCWUFUP3S7MOMLVL5LOQ"
check_upload_status = f"earthengine task info {task_id}"
response = subprocess.getstatusoutput(check_upload_status)[1]
# print(responses)


state = response.split("\n")[1].split(": ")[-1]
print(state)
