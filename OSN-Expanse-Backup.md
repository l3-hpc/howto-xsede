# How to back up data from Expanse to OSN

Here are the basics of OSN, and how to transfer data from Expanse to OSN using rclone.

## OSN - Open Storage Network
From OSN User Guide:
- The Open Storage Network (OSN) is a distributed data sharing and transfer service
intended to facilitate exchanges of active scientific data sets between research
organizations, communities and projects, providing easy access and high bandwidth
delivery of large data sets to researchers.

### OSN Links
- [OSN - Home](https://www.openstoragenetwork.org)
- [OSN - User Guide](https://www.openstoragenetwork.org/wp-content/uploads/2021/04/OSN-UserGuide.pdf)

## Introducing the OSN Storage Portal
Go to the OSN Storage Portal, [https://portal.osn.xsede.org](https://portal.osn.xsede.org)

Sign in with your XSEDE login and accept the DUO push.

The home page lists your buckets and their access key and secret access key.

The name convention is location/allocation, and the terminology is endpoint/bucket.  Our bucket is:
```
https://renc.osn.xsede.org/ees210015-bucket01
```
The location is the pod nearest you.  Ours is at RENCI.

Do a quick test by uploading a file through the OSN GUI interface.
- Click the link for the bucket
- Click on the gear in the top right corner, and fill out the S3 Explorer Settings. 
- Endpoint is pre-populated since I have only one bucket 
- Choose the bucket from the dropdown list
- I chose 'Private Bucket (I have AWS credentials)'. 
- Add the Access Key and Secret Access Key.  These are listed on the Storage Portal landing page by bucket. (Click *Storage Portal* or *Home* in the top nav bar to get back to the landing page.)
- I chose no MFA
- I skipped the options
- Click the Query S3 button
- Find the file on your local machine and drag and drop to upload.
   - There is (as of 6.22.2022) no option to click something on the page and choose which file to upload. You also have to aim the drop inside the table.

## Access OSN from Expanse
On Expanse, let's use [rclone](https://rclone.org). 
 
First, log in to Expanse using ssh or by using the [Expanse Portal Login](https://portal.expanse.sdsc.edu) and clicking 'expanse Shell Access'.

I needed to do `module spider rclone` to figure out whether rclone is installed.  

To load rclone, do:
```
module load cpu/0.15.4
module load rclone/1.56.0
```

Configure rclone.  First, find the file location:
```
rclone config file
```

The result is the following, which means, the file rclone.conf does not exist, but when it does, it should be in that path.
```
Configuration file doesn't exist, but rclone will use this path:
/home/llowe/.config/rclone/rclone.conf
```

Edit the file rclone.conf.
```
[OyBcSt]
type = s3
provider = Ceph
access_key_id = <access key here>
secret_access_key = <secret key here>
endpoint = https://renc.osn.xsede.org
no_check_bucket = true
```
Note:  Do not put things like keys and passwords in documents. If you have read/write access, then find the keys on the [Storage Portal](https://portal.osn.xsede.org). And yes, the square brackets are necessary.

Command are in the form:
```
rclone [command] OyBcSt:/ees210015-bucket01
```
Do a test...check what is in the bucket:
```
rclone ls OyBcSt:/ees210015-bucket01
```
Create a text file and copy it to the bucket
```
echo "hello!" > hello.txt
rclone copy hello.txt OyBcSt:/ees210015-bucket01
```
Check is it really there.
```
rclone ls OyBcSt:/ees210015-bucket01
```
Check the GUI too. [OSN Storage Portal](https://portal.osn.xsede.org)

When I do the `ls`, I get the following. The numbers on the left are file sizes.
```
(base) [llowe@login02 ~]$ rclone ls OyBcSt:/ees210015-bucket01
   129634 YT Thumbnail Requesting Consultation.png
        7 hello.txt
        7 hello2.txt
     5010 install-libs.txt
    72592 yellow_cube.png
```

## Adding users

To do this, you must be a 'data manager'.  On the OSN Storage Portal, you would see something like
..* EES210015_Lisa_Lowe (manage)

Click 'manage'.  If you have an XSEDE allocation, all the members in the project given access to OSN should be listed, along with a red button to Remove. (Check access by going to the [XSEDE User Portal](https://portal.xsede.org/group/xup/add-remove-user).  Open a help ticket with XSEDE/OSN if the members are not listed.)

If you click the link for 'Add a user to this project', your options are limited to a pre-populated dropdown menu.  If a member is already listed in the table, they will not appear in the dropdown menu; if you need to change the role of a member, you have to remove them first.  Once removed, you can find them in the dropdown and choose the new role.

```
export BUCKET="OyBcSt:/ees210015-bucket01"
rclone copy test $BUCKET/test
rclone copy ROMS_Results $BUCKET/harisree/ROMS_Results
```
