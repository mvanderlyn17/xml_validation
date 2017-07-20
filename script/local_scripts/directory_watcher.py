import boto3
import os, time
path_to_watch = "../../xmls/"
s3 = boto3.resource('s3')
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  #time.sleep (10)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  removed = [f for f in before if not f in after]
  if added:
      file = ", ".join(added)
      print("Upload started: "+file)
      data = open("../../xmls/"+file, 'rb')
      s3.Bucket('gen3-interns-trigger').put_object(Key=file, Body=data)
      print "Uploaded Complete"
  if removed:
      print "Removed: ", ", ".join (removed)
  before = after
