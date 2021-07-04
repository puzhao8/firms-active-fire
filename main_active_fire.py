import ee
import os, sys
import time
import subprocess
import urllib.request as Request
import zipfile
from pathlib import Path
from prettyprinter import pprint

import logging
logger = logging.getLogger(__name__)

class Downloader():
    def __init__(self):
        pass

    def download(self, url, save_folder):
        print(url)

        save_name = os.path.split(url)[-1]

        self.url = url
        self.dst = Path(save_folder) / save_name
        self.save_folder = Path(os.path.split(self.dst)[0])
        self.unzip_folder = self.save_folder / "unzipped"

        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            level=logging.INFO,
            stream=sys.stdout)   

        if os.path.isfile(self.dst):
            os.system("rm {}".format(self.dst))
            logging.info("Existed file deleted: {}".format(self.dst))
        else:
            logging.info("File doesn't exist.")
        # replace with url you need

        # if dir 'dir_name/' doesn't exist
        if not os.path.exists(self.save_folder):
            logging.info("Make direction: {}".format(self.save_folder))
            os.mkdir(self.save_folder)

        def down(_save_path, _url):
            try:
                Request.urlretrieve(_url, _save_path)
                return True
            except:
                print('\nError when retrieving the URL:\n{}'.format(_url))
                return False

        # logging.info("Downloading file.")
        down(self.dst, self.url)
        print("------- Download Finished! ---------\n")


    def un_zip(self, src):
        save_folder = Path(os.path.split(src)[0])
    
        unzip_folder = save_folder / "unzipped" / os.path.split(src)[-1][:-4]

        """ unzip zip file """
        zip_file = zipfile.ZipFile(src)
        if os.path.isdir(unzip_folder):
            pass
        else:
            os.mkdir(unzip_folder)
        for names in zip_file.namelist():
            zip_file.extract(names, unzip_folder)
        zip_file.close()


if __name__ == "__main__":

    nasa_website = "https://firms.modaps.eosdis.nasa.gov"
    save_folder = Path("/Users/puzhao/PyProjects/firms-active-fire/outputs")
    
    firms = [
        "/data/active_fire/modis-c6.1/shapes/zips/MODIS_C6_1_Global_24h.zip",
        "/data/active_fire/suomi-npp-viirs-c2/shapes/zips/SUOMI_VIIRS_C2_Global_24h.zip",
        "/data/active_fire/noaa-20-viirs-c2/shapes/zips/J1_VIIRS_C2_Global_24h.zip"
    ]

    NRT_AF = subprocess.getstatusoutput("earthengine ls users/omegazhangpzh/NRT_AF/")
    asset_list = NRT_AF[1].replace("projects/earthengine-legacy/assets/", "").split("\n")
    pprint(asset_list)

    task_dict = {}
    for period_key in ['24h', '48h', '7d']:
        for i in range(len(firms)):
            url = nasa_website + firms[i]
            url = url.replace("24h", period_key)
            filename = os.path.split(url)[-1][:-4]

            # downloader = Downloader()
            # downloader.download(url, save_folder)
            # # downloader.un_zip(save_folder / f"{filename}.zip")

            asset_id = f"users/omegazhangpzh/NRT_AF/{filename}"
            print(f"\n{asset_id}")

            upload_to_bucket = f"gsutil -m cp -r {save_folder}/{filename}.zip gs://eo4wildfire/active_fire/{filename}.zip"
            # remove_asset = f"earthengine rm {asset_id}"
            ee_upload_table = f"earthengine upload table --force --asset_id={asset_id} gs://eo4wildfire/active_fire/{filename}.zip"

            # os.system(upload_to_bucket)
            # if asset_id in asset_list:
            #     os.system(remove_asset)
            
            # os.system(ee_upload_table)

            ee_upload_status = subprocess.getstatusoutput(ee_upload_table)
            task_id = ee_upload_status[1].split("ID: ")[-1]
            task_dict.update({filename: {'id': task_id}})

            pprint(task_id)

    # check uplpad status
    upload_finish_flag = False
    while(not upload_finish_flag):
        time.sleep(10) # delay 30s
        
        for filename in task_dict.keys():

            task_id = task_dict[filename]['id']
            check_upload_status = f"earthengine task info {task_id}"
            status = subprocess.getstatusoutput(check_upload_status)
            state = status[1].split("\n")[1].split(": ")[-1]
            task_dict[filename].update({'state': state})

            upload_finish_flag = upload_finish_flag and (state == "COMPLETED")

        print()
        pprint(task_dict)

    # set asset public
    if upload_finish_flag:
        NRT_AF = subprocess.getstatusoutput("earthengine ls users/omegazhangpzh/NRT_AF/")
        asset_list = NRT_AF[1].replace("projects/earthengine-legacy/assets/", "").split("\n")

        for asset in asset_list:
            os.system(f"earthengine acl set public {asset_id}")
            os.system(f"earthengine acl get {asset_id}")
            



# os.system(f"earthengine rm {asset_id}")
# os.system(f"earthengine upload table --asset_id={asset_id} gs://eo4wildfire/active_fire/{filename}.zip")

# earthengine task info 4DYDKYYRRHHRH3JVSLDZ63N5

# earthengine acl get users/username/asset_id
# earthengine acl set public users/username/asset_id
# earthengine acl ch -u username@gmail.com:R users/username/asset_id
# /Users/puzhao/PyProjects/firms-active-fire/outputs/MODIS_C6_1_Global_24h.zip