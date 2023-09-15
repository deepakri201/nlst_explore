# load_seg_slicer.py 
# 
# This script takes as input a manifest txt file with a list of SeriesInstanceUIDs, 
# which each correspond to the SeriesInstanceUID of the DICOM segmentation object. 
# 1. Each series is imported from the DICOM datastore. 
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

# Manifest - list of SeriesInstanceUIDs of the DICOM Segmentation objects 
manifest_file = "C://Users//deepa//git//nlst_explore//manifest//manifest_list.txt"
gcs_file = "C://Users//deepa//git//nlst_explore//manifest//gcs_list.txt" 

# GCP settings 
project_id = "idc-external-025"
dataset_id = "total_segmentator_nlst_total_070823"
datastore_id = "126k-series"
location_id = "us-central1"

# table 
table_id = "bigquery-public-datasets.idc_current.dicom_all"

##############################
#-- Read the manifest file --# 
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
downloadDirectory = os.path.join(slicer.dicomDatabase.databaseDirectory, 'tmp')
if not os.path.isdir(downloadDirectory):
  os.makedirs(downloadDirectory)

# Retrieve the instance using the DICOM web client  
retrievedInstance = DICOMwebClient.retrieve_instance(study_instance_uid=studyInstanceUID,
                                                     series_instance_uid=seriesInstanceUID, 
                                                     sop_instance_uid=sopInstanceUID)

# Write the file to a tmp folder 
pydicom.filewriter.write_file(os.path.join(downloadDirectory, "seg.dcm"), retrievedInstance)

# Import file into the dicom database 
db = slicer.dicomDatabase
DICOMUtils.importDicom(downloadDirectory,db)

#####################################################
#-- Get the corresponding referenced series files --#
#####################################################

import subprocess
output = subprocess.run(["gcloud", "auth", "application-default", "login"])
print(output)
# cmdCommand = "gcloud auth application-default login" 
# process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()
# print(output)
# print(error)

# # read the file with pydicom 
#
# # get the referenced SeriesInstanceUID 
#
# # use gsutil to download from the bucket 
# # can use s5cmd later 
#
# # Select all files from GCS for a given DICOM series
#
# client = bigquery.Client(project=project_id)
#
# query = f"""
# SELECT 
#   DISTINCT(CONCAT("cp s3://", SPLIT(gcs_url,"/")[SAFE_OFFSET(2)], "/", crdc_series_uuid, "/* .")) 
# FROM 
#     `bigquery-public-data.idc_current.dicom_all`
# WHERE 
#   SeriesInstanceUID = @series_id;
# """
#
# job_config = bigquery.QueryJobConfig(query_parameters=[
#                                                        bigquery.ScalarQueryParameter("series_id", "STRING", seriesInstanceUID)
#                                                        ])
# result = client.query(query, job_config=job_config) 
# series_df = result.to_dataframe(create_bqstorage_client=True)
# print(series_df)

# client = bigquery.Client(project=project_id)
#
# query_view = f"""
#   SELECT 
#     * 
#   FROM
#     {table_id}
#   WHERE
#     SeriesInstanceUID = @series_id;
#   """
#
# job_config = bigquery.QueryJobConfig(query_parameters=[
#                                                        bigquery.ScalarQueryParameter("series_id", "STRING", seriesInstanceUID)
#                                                        ])
# result = client.query(query_view, job_config=job_config) 
# series_df = result.to_dataframe(create_bqstorage_client=True)
# print(series_df)
#
# gcs_url = series_df['gcs_url'].values
# gcs_url.to_csv(gcs_file, header = False, index = False)
#
# # copy into temporary downloadDirectory
# import subprocess
# cmdCommand = "type " + str(gcs_url) + " | gsutil -m cp -I" 
# process = subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
# output, error = process.communicate()
# print(output)
# print(error)

 
#
# !cat SM_MAX_Series_gcs_manifest.txt | gsutil -m cp -I .

# #-- Load the DICOM files into the scene --# 
#
# loadedNodeIDs = []  # this list will contain the list of all loaded node IDs
# from DICOMLib import DICOMUtils
# with DICOMUtils.TemporaryDICOMDatabase() as db:
#   DICOMUtils.importDicom(dicomDataDir, db)
#   patientUIDs = db.patients()
#   for patientUID in patientUIDs:
#     loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))
#
# #-- Load the label files into the scene --# 
#
# [slicer.util.loadSegmentation(os.path.join(niftiDataDir,f)) for f in os.listdir(niftiDataDir)]
#
# #-- Get the reference volume node --#
# # The loadedNodeIDs will most likely contain a single scalar volume node, but if not, search for it 
#
# referenceVolumeNode = [] 
# for nodeID in loadedNodeIDs: 
#   node = slicer.mrmlScene.GetNodeByID(nodeID)
#   if node.IsA('vtkMRMLScalarVolumeNode'):
#     referenceVolumeNode = node 
# if not referenceVolumeNode: 
#   print('ERROR creating scalar volume from DICOM data directory, please check your data')
#
# #-- Create the subject hierarchy --# 
#
# # First get the list of segmentationNodes 
# segmentationNodes = slicer.util.getNodes('*SegmentationNode*') # segmentationNodes = slicer.util.getNodesByClass('*Segmentation*')
# segmentationNodes = list(segmentationNodes.values())
#
# # Get the subject hierarchy 
# shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
# seriesItem = shNode.GetItemByDataNode(referenceVolumeNode)
# studyItem = shNode.GetItemParent(seriesItem)
# patientItem = shNode.GetItemParent(studyItem)
#
# # Set the parent for each of the segmentationNodes 
# for segmentationNode in segmentationNodes: 
#   segmentationShItem = shNode.GetItemByDataNode(segmentationNode)
#   shNode.SetItemParent(segmentationShItem, studyItem)
#
# #-- Create the RTStruct --# 
#
# if not os.path.isdir(outputDir):
#   os.mkdir(outputDir)
#
# # Get exportables for the segmentations 
# exporter = DicomRtImportExportPlugin.DicomRtImportExportPluginClass()
# # exportables = exporter.examineForExport(segmentationShItem) 
# exportables = [] 
# [exportables.append(exporter.examineForExport(shNode.GetItemByDataNode(exp))[0]) for exp in segmentationNodes]
#
# # Get exportables for the reference volume 
# referenceVolumeShItem = shNode.GetItemByDataNode(referenceVolumeNode)
# exportables2 = exporter.examineForExport(referenceVolumeShItem)
# # Append to a single exportables list 
# [exportables.append(exp) for exp in exportables2]
#
# # Set the outputDir and export 
# for exp in exportables:
#   print(exp)
#   exp.directory = outputDir
# exporter.export(exportables)
#
# print('saved RTStruct')
#
# # -- Clean up the scene, necessary? -- # 



