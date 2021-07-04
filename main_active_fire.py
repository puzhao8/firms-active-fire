import ee
import os, sys
import urllib.request as Request
import zipfile
from pathlib import Path

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
        print("------- Download Finished! ---------")


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
    save_folder = Path("/Users/puzhao/PyProjects/wildfire-s1s2-dataset/outputs")
    
    firms = [
        # "/data/active_fire/modis-c6.1/shapes/zips/MODIS_C6_1_Global_24h.zip",
        "/data/active_fire/suomi-npp-viirs-c2/shapes/zips/SUOMI_VIIRS_C2_Global_24h.zip",
        # "/data/active_fire/noaa-20-viirs-c2/shapes/zips/J1_VIIRS_C2_Global_24h.zip"
    ]

    for i in range(len(firms)):
        url = nasa_website + firms[i]
        filename = os.path.split(url)[-1][:-4]

        downloader = Downloader()
        downloader.download(url, save_folder)
        # downloader.un_zip(save_folder / f"{filename}.zip")

        asset_id = f"users/omegazhangpzh/NRT_AF/{filename}"
        print(asset_id)
        os.system(f"gsutil -m cp -r {save_folder}/SUOMI_VIIRS_C2_Global_24h.zip gs://eo4wildfire/active_fire/{filename}.zip")
        
        os.system(f"earthengine rm {asset_id}")
        os.system(f"earthengine upload table --asset_id={asset_id} gs://eo4wildfire/active_fire/{filename}.zip")
        
        os.system(f"earthengine acl set public {asset_id}")
        os.system(f"earthengine acl get {asset_id}")

        # earthengine task info 4DYDKYYRRHHRH3JVSLDZ63N5

        # earthengine acl get users/username/asset_id
        # earthengine acl set public users/username/asset_id
        # earthengine acl ch -u username@gmail.com:R users/username/asset_id
