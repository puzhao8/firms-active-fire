firms-active-fire
firms-active-fire


# earth engine upload
https://developers.google.com/earth-engine/guides/command_line#upload

earthengine upload table --force --asset_id=users/omegazhangpzh/NRT_AF/kamploop gs://eo4wildfire/active_fire/kamploop.zip
earthengine create folder projects/my-ee-enabled-project-id/assets/

os.system(f"earthengine rm {asset_id}")
os.system(f"earthengine upload table --asset_id={asset_id} gs://eo4wildfire/active_fire/{filename}.zip")

earthengine task info 4DYDKYYRRHHRH3JVSLDZ63N5

earthengine acl get users/username/asset_id
earthengine acl set public users/username/asset_id
earthengine acl ch -u username@gmail.com:R users/username/asset_id
/Users/puzhao/PyProjects/firms-active-fire/outputs/MODIS_C6_1_Global_24h.zip