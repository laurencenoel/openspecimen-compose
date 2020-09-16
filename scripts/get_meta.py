import glob
import pandas as pd
import requests
import json
import os
import csv
import numpy as np
import time, datetime
import subprocess

DATADIR = "/mnt/openspecimen-compose/data/os-data/"
IMGDIR = DATADIR + "de-file-data/"
JOBDIR = DATADIR + "query-exported-data/"
#define the id of the scheduled query (can be seen in de-file-data)
JOB_EMB_FILE = "scheduled_query_24"
JOB_ORG_FILE = "scheduled_query_25"
#in baseURL, 102 is the id of specimen_complEF_form
BASEURL = "http://localhost:80/"
API_FORM= "openspecimen/rest/ng/forms/102/data/"
API_SPE= "openspecimen/rest/ng/specimens/"
SCRIPTDIR= "/mnt/openspecimen-compose/scripts/"
TRANSFERFILE = SCRIPTDIR + "transfer_path.tsv"
ANNOTFILE = SCRIPTDIR + "annotation.csv"
TRANSFERFILE_ORG = SCRIPTDIR + "transfer_org_path.tsv"
ANNOTFILE_ORG = SCRIPTDIR + "annotation_org.csv" 
ALLFILES=[TRANSFERFILE,ANNOTFILE,TRANSFERFILE_ORG,ANNOTFILE_ORG]
OLDFILES = []

headers = {
        'Content-type':'application/json',
        'Authorization':'Basic bGF1cmVuY2U6SHVkZWNhMjAxOSEm'
        }

def files_after(files,min):
    # NOT USED
    #get list of files created within a given number of min
    lower_time_bound = datetime.datetime.now() - datetime.timedelta(minutes=min)
    return filter(lambda f:datetime.datetime.fromtimestamp(os.path.getctime(f)) > lower_time_bound, files) 


def checkIsNew(imgFileName) : 
    isNew = True
    #dirFile = glob.glob(IMGDIR+"*-*")
    #lastCreatedFiles = files_after(dirFile,60)
    command="find "+IMGDIR+" -mmin -60"
    result=subprocess.run(command,shell=True,stdout=subprocess.PIPE)
    lastCreatedFiles = result.stdout.decode('utf-8')
    pathFile = IMGDIR + imgFileName    
    #print("pathFile ",pathFile)
    
    if imgFileName in lastCreatedFiles: 
    #for elt in lastCreatedFiles:   
       # if pathFile == elt : 
       print("NEW : ", imgFileName)
            #print(imgFileName, "is a new file")
       return True
    print("NOT NEW : ", pathFile)
    #print(imgFileName, " is not a new file")
    OLDFILES.append(imgFileName)
    
    return False

def addImgId(row, ImgInfo):
    #get the image identifier via the API
    print("getting image identifier via the API")
    dicoL = {}
    for key in ImgInfo.keys():
        dicoL[key] = []
    list_ID = []

    
    for i, item in enumerate(row):
        url = BASEURL+API_FORM+str(item)
        response = requests.request("GET",url,headers=headers)
        #print(headers)
        json_data = response.json()
        #print(json_data) 
        for key in ImgInfo.keys():
            if json_data[ImgInfo[key]["osUploadName"]] is None : 
                dicoL[key].append("None")
            else : 
                dicoL[key].append(json_data[ImgInfo[key]["osUploadName"]]["fileId"]) 

        #for elt in dicoL :
           # print(elt,dicoL[elt])
    return dicoL

def create_transfer_file(df,ImgInfo,file) : 
    #create tsv file for omero (target, name, path)
    print("creating transfer file ")
    dicoTransfer = []

    for key in ImgInfo.keys():
    
        df3 = df.filter(items=["Code",ImgInfo[key]["osImgId"],ImgInfo[key]["osImgName"]])
        print(df3)
        df3.columns = ["target","path","name"]
        
        #on enlève les fichiers images créés il y a plus d'une heure
    

        dico = df3.to_dict("records")
   
        for elt in dico :
            #print(elt)
            if elt["name"] !=  "None"  and elt["path"] != None and elt["path"] != "None" and checkIsNew(elt["path"]) :
                #print("adding elt")
                dicoTransfer.append({"target":"Project:name:H_CEF/Dataset:name:"+elt["target"],
                        "name":elt["name"],
                        "path":IMGDIR+elt["path"]})      

    f=open(file,"w")
    writer=csv.DictWriter(f,fieldnames=["target","path","name"],delimiter="\t")
    writer.writeheader()
    writer.writerows(dicoTransfer)
    f.close()
    

def create_annotation_file(df,ImgInfo) : 
    print("creating annotation file for embryo")
    dicoAnnot = []

    infoSpe = df.to_dict("records")

    for specimen in infoSpe :
        for key in ImgInfo.keys():
            #print(specimen[ImgInfo[key]["osImgName"]])
            imgType = ""
            if key == "Caryotype" or key == "SRY" :
                imgType = key
            else : 
                imgType = "Limb"

            if isinstance(specimen[ImgInfo[key]["osImgName"]],str) and specimen[ImgInfo[key]["osImgId"]] not in OLDFILES : 
                org = ""
                org_type = ""
                if key == "Foot" :
                    org="foot"
                elif key == "Femur":
                    org="leg"
                    org_type="femur"
                elif key == "Tibia":
                    org="leg"
                    org_type="tibia"
                elif key == "Ulna":
                    org="arm"
                    org_type="ulna"
                elif key == "Humeral":
                    org="arm"
                    org_type="humerus"

                dicoAnnot.append({"Dataset Name":specimen["Code"],
                    "Image Name":specimen[ImgInfo[key]["osImgName"]],
                    "Gender": specimen["Gender"],
                    "Age": specimen["Age"],
                    "Organ": org,
                    "OrganPart": org_type,
                    "CarnegieStage": specimen["Carnegie stage"],
                    "SpecimenID": specimen["Code"],
                    "Type":imgType                    
                    })

    #csvframe = pd.DataFrame()
    #csvframe["Dataset Name"]=df["Code"].str[:15]
    #csvframe["Image Name"]=df["Image"]
    #csvframe["Gender"]=df["Gender"]
    #csvframe["Age"]=df["Age"]
    #csvframe["Carnegie_stage"]=df["Carnegie stage"]
    #csvframe.to_csv(ANNOTFILE, index=False)
    with open(ANNOTFILE,"w") as f:
        writer = csv.DictWriter(f, fieldnames=["Dataset Name","Image Name","Gender","Age","Organ","OrganPart","CarnegieStage","SpecimenID","Type"])
        writer.writeheader()
        writer.writerows(dicoAnnot)
        
        
def create_annotation_org_file(df,ImgInfo) : 
    print("creating annotation file for organs")
    dicoAnnot = []
    infoSpe = df.to_dict("records")
    for specimen in infoSpe :
        url = BASEURL+API_SPE+str(specimen["Parent Specimen ID"])
        print(url)
        response = requests.request("GET",url,headers=headers)
        json_data = response.json()
        #print(json_data)
        gender = ""
        age = ""
        carnegie =""
        if json_data["extensionDetail"]["attrs"] != None : 
            for elt in json_data["extensionDetail"]["attrs"]:
                if elt["udn"] == "gender" : 
                    gender = elt["displayValue"]
                    #print(gender)
                elif elt["udn"] == "agePCW" : 
                    age = elt["displayValue"]
                    #print(age)
                elif elt["udn"] == "carnegie" : 
                    carnegie = elt["displayValue"]


        for key in ImgInfo.keys():
            if isinstance(specimen[ImgInfo[key]["osImgName"]],str) and specimen[ImgInfo[key]["osImgId"]] not in OLDFILES :
                
                #if specimen["Organ"] != "multiple" : 
                #print(specimen["Organ"]) 
                dicoAnnot.append({"Dataset Name":specimen["Code"],
                    "Image Name":specimen[ImgInfo[key]["osImgName"]],
                    "Organ": specimen["Organ"],
                    "Laterality": specimen["Laterality"],
                    "OrganPart": specimen["Organ_part"],
                    "SpecimenID": specimen["Code"][:15],
                    "Gender": gender,
                    "Age": age,
                    "CarnegieStage": carnegie
                    })                    
                #else : récupérer info  


    with open(ANNOTFILE_ORG,"w") as f:
        writer = csv.DictWriter(f, fieldnames=["Dataset Name","Image Name","Organ","OrganPart","Laterality","SpecimenID","Gender","Age","CarnegieStage"])
        writer.writeheader()
        writer.writerows(dicoAnnot)


def export_Embryo_Info():
    #for memo : the info must be present in the form to add specific fields in openspeciemn (specimenComplEF.xml)
    #then, it should be mapped to the export query (and the column name should correspond to the osImgName in the following array:
    
    ImgInfo = {"Compl":{"osUploadName":"FU13","osImgName":"Image","osImgId":"Image ID"},
        "Foot":{"osUploadName":"FUFoot","osImgName":"Foot image","osImgId":"ImgFoot ID"},
        "Tibia":{"osUploadName":"FUTibia","osImgName":"Tibia image","osImgId":"ImgTibia ID"},
        "Femur":{"osUploadName":"FUFemur","osImgName":"Femur image","osImgId":"ImgFemur ID"},
        "Ulna":{"osUploadName":"FUUlna","osImgName":"Ulna image","osImgId":"ImgUlna ID"},
        "Humeral":{"osUploadName":"FUhumeral", "osImgName":"Humeral image", "osImgId":"ImgHumeral ID"},
        "Caryotype":{"osUploadName":"FUCaryo","osImgName":"Caryotype image", "osImgId":"ImgCaryotype ID"},
        "SRY": {"osUploadName":"FUSRY", "osImgName":"SRY image", "osImgId":"ImgSRY ID"}
        }

    #get the last scheduled query file on openspecimen (the query number is specified in the the path)
    dirFile=glob.glob(JOBDIR+JOB_EMB_FILE+"*.csv")
    lastFile=max(dirFile, key=os.path.getctime)
    print(lastFile)

    #read csv file, continue if there is more than just the header line
    df=pd.read_csv(lastFile, skiprows=4)
    if len(df) >= 1 : 
        
        #add image identifier to the table
        df2 = df[["Record ID"]].copy()
        #get ID of all the different images in a dictionary via image API (RECORD ID is the ID of specimen EF form)
        dicoL = addImgId(df2["Record ID"], ImgInfo)
        #add the corresponding columns to the dataframe
        for key in ImgInfo.keys():
            df[ImgInfo[key]["osImgId"]] = dicoL[key] 
            
        #create files for transfer : two files are needed :
        #transfer_path.tsv file with three columns : target dataset(target), name of the file (name)  and path to the file to import
        #bulk_transfer.yml file defines the import options (and list the column names: target, name, path) : this file does not change
        create_transfer_file(df,ImgInfo,TRANSFERFILE)

        #create files to add annotations (csv containing the metadata and yml containing info about the different columns)
        create_annotation_file(df,ImgInfo)


def export_Organ_Info() :

    ImgInfo = {"Img1":{"osUploadName":"FUOrgan1","osImgName":"Img1","osImgId":"Image1 ID"},
        "Img2":{"osUploadName":"FUOrgan2","osImgName":"Img2","osImgId":"Image2 ID"},
        "Img3":{"osUploadName":"FUOrgan3","osImgName":"Img3","osImgId":"Image3 ID"}
        }
        
    #get the last scheduled query file on openspecimen 
    dirFile=glob.glob(JOBDIR+JOB_ORG_FILE+"*.csv")
    lastFile=max(dirFile, key=os.path.getctime)
    print(lastFile)

    #read csv file, continue if there is more than just the header line
    df=pd.read_csv(lastFile, skiprows=4)
    if len(df) >= 1 : 

        #add image identifier to the table
        df2 = df[["Record ID"]].copy()
        #get ID of all the different images in a dictionary via image API (RECORD ID is the ID of specimen EF form)
        dicoL = addImgId(df2["Record ID"],ImgInfo)
        #add the corresponding columns to the dataframe
        for key in ImgInfo.keys():
            df[ImgInfo[key]["osImgId"]] = dicoL[key] 
        #print(df.columns)
            
        #create files for transfer : two files are needed :
        #transfer_path.tsv file with three columns : target dataset(target), name of the file (name)  and path to the file to import
        #bulk_transfer.yml file defines the import options (and list the column names: target, name, path) : this file does not change
        create_transfer_file(df,ImgInfo,TRANSFERFILE_ORG)

        #create files to add annotations (csv containing the metadata and yml containing info about the different columns)
        create_annotation_org_file(df,ImgInfo)


if __name__=="__main__":
    #first, we clear the info files
    for filepath in ALLFILES : 
        file=open(filepath,"w")
        file.close()

    export_Embryo_Info()
    export_Organ_Info()
