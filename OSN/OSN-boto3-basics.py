#To edit with Vim, use this
#:set tabstop=8 expandtab shiftwidth=4 softtabstop=4

## OSN-boto3-basics.py
#  Author: Jim Culbert, MGHPCC

# Basic boto3 commands for accessing OSN with Python  
#  List bucket contents, copy or delete a file

#You probably have these:
from urllib.parse import urlparse
import io
#And you probably need to install this:
import boto3

#Define your bucket and keys
ACCESS_KEY = "youraccesskey"
SECRET_KEY = "yoursecretaccesskey"
BUCKET = "https://your/bucket/name"

#Name a file
HELLO_OSN_KEY = 'hello_osn.txt'

# Convenience function to pull endpoint and bucket out of
# OSN URI
def parse_osn_bucket(bucket_uri):
    uri_parts = urlparse(bucket_uri)
    bucket_part = uri_parts.path.strip("/")
    endpoint_part = f'{uri_parts.scheme}://{uri_parts.netloc}'
    
    return (endpoint_part, bucket_part)

#endpoint is location
endpoint, bucket_name = parse_osn_bucket(BUCKET)

#Setup session with keys and define bucket
session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)
s3 = session.resource('s3', endpoint_url=endpoint)
bucket = s3.Bucket(bucket_name)

# List your bucket
print("****BUCKET CONTENTS: START***")
for o in bucket.objects.all():
    print(o.key)

# Upload an object
# Note using in-memory file here. Normally would be
# "regular" disk file
with io.BytesIO(bytes("HELLO OSN!!", encoding='utf-8')) as f:
    r = bucket.upload_fileobj(f, HELLO_OSN_KEY)

# List your bucket again, will show new "hello_osn.txt" object
print("****BUCKET CONTENTS: AFTER UPLOAD***")
for o in bucket.objects.all():
    print(o.key)

# Download test object and print contents
print("****DOWNLOAD OBJECT CONTENTS***")   
with io.BytesIO() as f:
    bucket.download_fileobj(HELLO_OSN_KEY, f)
    print(f.getvalue())

# Delete the test object
response = bucket.delete_objects(
    Delete={
        'Objects': [
            {
                'Key': HELLO_OSN_KEY,
            },
        ],
    },
)

# List your bucket again, will show that test object
# has been deleted.
print("****BUCKET CONTENTS: AFTER DELETE***")
for o in bucket.objects.all():
    print(o.key)

# Upload an object
# Note using in-memory file here. Normally would be
# "regular" disk file
with io.BytesIO(bytes("HELLO OSN!!", encoding='utf-8')) as f:
    r = bucket.upload_fileobj(f, HELLO_OSN_KEY)

# Download test object and print contents
print("****DOWNLOAD OBJECT CONTENTS***")   
with io.BytesIO() as f:
    bucket.download_fileobj(HELLO_OSN_KEY, f)
    print(f.getvalue())


# List your bucket again, will show new "hello_osn.txt" object
print("****BUCKET CONTENTS: AFTER UPLOAD***")
for o in bucket.objects.all():
    print(o.key)


#To edit with Vim, use this
#:set tabstop=8 expandtab shiftwidth=4 softtabstop=4
