import json 
import os
import sys
import boto3 
import datetime


if __name__ == "__main__":
    dirname = sys.argv[1]
    groupname = sys.argv[2]
    assert type(dirname == str)
    assert type(groupname == str)

    ## Declare boto client. 
    s3client = boto3.client("s3")

    with open(os.path.join(dirname,"stack_config_template.json"),'r') as f:
        d = json.load(f)
    ## Initialize a testing pipeline with all the relevant details:
    bucket=d["PipelineName"] 
    groupname=d["UXData"]["Affiliates"][0]["AffiliateName"] 
    grouppath = "s3://{}".format(os.path.join(dirname,groupname,"testdir")) 
    
    ## make a dataset file
    dataset = {"field":"values"}
    dname = "dataset1.json"
    dname_localpath = os.path.join(dirname,"test_resources",dname)
    dname_remotepath = os.path.join(groupname,"testdir",dname)
    with open(dname_localpath,"w") as f:
        json.dump(dataset,f,indent =4)
    s3client.put_object(Body = dname_localpath,
            Bucket=dirname,
            Key=dname_remotepath)

    ## make a config file
    config = {"__duration__":10,"__dataset_size__":10}
    cname = "config.json"
    cname_localpath = os.path.join(dirname,"test_resources",cname)
    cname_remotepath = os.path.join(groupname,"testdir",cname)
    with open(os.path.join(dirname,"test_resources",cname),'w') as f:
        json.dump(config,f,indent =4)
    s3client.put_object(Body = cname_localpath,
            Bucket=dirname,
            Key=cname_remotepath)

    ## make a submit file 
    submit = {"dataname":dname_remotepath,
              "configname":cname_remotepath,
              "timestamp":str(datetime.datetime.now()).replace(" ","T")} 
    sname = "submit.json"
    sname_localpath = os.path.join(dirname,"test_resources",sname)
    sname_remotepath = os.path.join(groupname,"testdir",sname)
    with open(os.path.join(dirname,"test_resources",sname),'w') as f:
        json.dump(submit,f,indent =4)
    s3client.put_object(Body = sname_localpath,
            Bucket=dirname,
            Key=sname_remotepath)

