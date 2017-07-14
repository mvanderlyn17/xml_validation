import boto3
import os
import os, time


s3 = boto3.resource('s3')

path_to_watch = "../xmls"
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
while 1:
  time.sleep (10)
  after = dict ([(f, None) for f in os.listdir (path_to_watch)])
  added = [f for f in after if not f in before]
  if added:
      print "Added: ", ", ".join (added)
      data = open("../xmls"+added, 'rb')
      s3.Bucket("gen3-interns-trigger").put_object(key=added, Body=data)
