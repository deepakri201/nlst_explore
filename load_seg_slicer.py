# load_seg_slicer.py 
# 
# 1. This script takes as input the DICOM Segmentation object studyInstanceUID, 
#    seriesInstanceUID and SOPInstanceUID. It downloads the object from the DICOM 
#    datastore.  
# 2. The corresponding referenceSeriesInstanceUID is found for each series, and 
#    obtained from the IDC bucket. 
# 3. The DICOM files are read into the Slicer DICOM database. 
# 4. The Slicer scene is loaded with the SEGs, and the reference series automatically. 
# 
# Notes: 
# https://discourse.slicer.org/t/cant-export-segmentation-as-dicom-rtstruct-in-python-script/16981
# https://github.com/SlicerRt/SlicerRT/issues/184#issuecomment-814931832
# Need to install the QuantitativeReporting and SlicerRT extensions.
# 
# For now, 
# - input a list specified in the script itself. Later make this an input for the script. 
# - later only retrieve instances that do not exist already in the Slicer DICOM database, use the indexer 
# - use IDC API later to download!!! 
# 
# cd to C:\Users\deepa\AppData\Local\slicer.org\Slicer 5.5.0-2023-08-19
# Slicer.exe --python-script "C://Users//deepa//git//nlst_explore//load_seg_slicer.py" # --no-splash  --no-main-window
# 
# To do: 
# - change names of files that are written, so not to the same folder. Maybe name by SeriesInstanceUID instead? 
# - retrieve the series instead of instance for the DICOM SEG object. Then don't need StudyInstanceUID or SOPInstanceUID. 
#
# Deepa Krishnaswamy 
# Brigham and Women's Hospital
# September 2023 
###################################################################

### Imports ### 

import os 
import sys 
from DICOMLib import DICOMPlugin
import vtk, qt, ctk, slicer

import DicomRtImportExportPlugin
import DICOMwebBrowser
from DICOMwebBrowser import GoogleCloudPlatform

import dicomweb_client.log
dicomweb_client.log.configure_logging(2)
from dicomweb_client.api import DICOMwebClient

from DICOMLib import DICOMUtils

import pydicom 

from slicer.util import pip_install
pip_install("google-cloud-bigquery")
pip_install("google-cloud-storage")

from google.cloud import bigquery
from google.cloud import storage

#-- Install extensions --# 
 
##############
#-- Inputs --# 
##############

# GCP settings 
project_id = "idc-external-025"
dataset_id = "total_segmentator_nlst_total_070823"
datastore_id = "126k-series"
location_id = "us-central1"

# table 
table_id = "bigquery-public-datasets.idc_current.dicom_all"

##############################
#-- Set the UIDs --# 
##############################

studyInstanceUID = "1.2.840.113654.2.55.222358418596811829743750475747304078456"
seriesInstanceUID ="1.2.276.0.7230010.3.1.3.313263360.50439.1688804452.744648" 
sopInstanceUID = "1.2.276.0.7230010.3.1.4.313263360.50439.1688804452.744649"

########################################################################
#-- Download the DICOM segmentation objects from the DICOM datastore --#
########################################################################

# Setup gcloud 
import shutil 
args = [shutil.which('gcloud')]
if (None in args):
   logging.error(f"Unable to locate gcloud, please install the Google Cloud SDK")

# Setup the DICOMwebClient 
url = f"https://healthcare.googleapis.com/v1/projects/{project_id}/locations/{location_id}/datasets/{dataset_id}/dicomStores/{datastore_id}/dicomWeb"
session = None
headers = {}
headers["Authorization"] = f"Bearer {GoogleCloudPlatform().token()}"
DICOMwebClient = DICOMwebClient(url=url, session=session, headers=headers)

# first set the downLoad directory 
downloadDirectory_seg = os.path.join(slicer.dicomDatabase.databaseDirectory, 'tmp_seg')
if not os.path.isdir(downloadDirectory_seg):
  os.makedirs(downloadDirectory_seg)

# Retrieve the instance using the DICOM web client  
retrievedInstance = DICOMwebClient.retrieve_instance(study_instance_uid=studyInstanceUID,
                                                     series_instance_uid=seriesInstanceUID, 
                                                     sop_instance_uid=sopInstanceUID)

# Write the file to a tmp folder 
pydicom.filewriter.write_file(os.path.join(downloadDirectory_seg, "seg.dcm"), retrievedInstance)

# Import file into the dicom database 
db = slicer.dicomDatabase
DICOMUtils.importDicom(downloadDirectory_seg,db)

#####################################################
#-- Get the corresponding referenced series files --#
#####################################################

# Get the referenced SeriesInstanceUID
dcm = pydicom.dcmread(os.path.join(downloadDirectory_seg, "seg.dcm"))
referenced_series_instance_uid =  dcm.ReferencedSeriesSequence[0]['SeriesInstanceUID'].value
print('referenced_series_instance_uid: ' + str(referenced_series_instance_uid))

##################################
#-- query for crdc_series_uuid --#
##################################

client = bigquery.Client(project=project_id)

query = f"""
SELECT 
  DISTINCT(crdc_series_uuid) as series_uuid 
FROM 
    `bigquery-public-data.idc_current.dicom_all`
WHERE 
  SeriesInstanceUID = @series_id;
"""

job_config = bigquery.QueryJobConfig(query_parameters=[
                                                       bigquery.ScalarQueryParameter("series_id", "STRING", referenced_series_instance_uid)
                                                       ])
result = client.query(query, job_config=job_config) 
series_df = result.to_dataframe(create_bqstorage_client=True)
print(series_df)

########################################## 
# -- use gsutil to download the files -- #
##########################################

# first set the downLoad directory 
downloadDirectory = os.path.join(slicer.dicomDatabase.databaseDirectory, 'tmp')
if not os.path.isdir(downloadDirectory):
  os.makedirs(downloadDirectory)

# Use gsutil to copy the files to the downloadDirectory 
gcs_directory = "gs://public-datasets-idc/" + series_df['series_uuid'].values[0]
print('gcs_directory: ' + gcs_directory)

# Run gsutil 
import re
downloadDirectory = re.sub("/", r"\\", downloadDirectory)
args = [shutil.which("gsutil")]
subcommand = f" -m cp -r {gcs_directory}/* {downloadDirectory}"
args.extend(subcommand.split())
print(args)
print(args)
process = slicer.util.launchConsoleProcess(args)
print(process)
process.stdout.read()

#################################################
# Now add the CT files to the DICOM database -- # 
#################################################
    
DICOMUtils.importDicom(downloadDirectory,db)

##############################################
#-- Load the CT DICOM files into the scene --# 
##############################################

loadedNodeIDs = []  # this list will contain the list of all loaded node IDs
patientUIDs = db.patients()
for patientUID in patientUIDs:
    loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))

