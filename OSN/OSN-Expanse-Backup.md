# How to back up data from Expanse to OSN

Here are the basics of OSN and how to transfer data from Expanse to OSN using rclone.

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
Go to the OSN Storage Portal, [https://portal.osn.xsede.org](https://portal.osn.xsede.org).

Clicking 'Login Using Your Home Instution' should take you to CILogon for XSEDE. Sign in with your XSEDE login and accept the DUO push.

The OSN home page lists your buckets and their access key and secret access key.

The naming convention is location/allocation, and the terminology is endpoint/bucket.  Our example bucket name is:
```
https://renc.osn.xsede.org/XYZ123415-bucket01
```
Your location may be different and is named for the pod nearest you.  This one is at RENCI.

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
Those were the latest modules as of 6/22/2022.  Do `module spider rclone` to check for newer versions. Use the newest ones. 

Configure rclone.  First, find the file location:
```
rclone config file
```

The result is the following, which means, the file rclone.conf does not exist, but when it does, it should be in that path.
```
Configuration file doesn't exist, but rclone will use this path:
/home/$USER/.config/rclone/rclone.conf
```

Edit the file rclone.conf.
```
[CoolStuff]
type = s3
provider = Ceph
access_key_id = <access key here>
secret_access_key = <secret key here>
endpoint = https://renc.osn.xsede.org
no_check_bucket = true
```
The first line is whatever you want. Pick something that describes your project. Yes, the square brackets are necessary.
- Note:  Do not put things like keys and passwords in documents. If you have read/write access, then find the keys on the [Storage Portal](https://portal.osn.xsede.org).  If not, ask your data manager to make the keys available to you in a secure fashion. 

Command are in the form:
```
rclone [command] CoolStuff:/XYZ123456-bucket01
```
To make it easier to follow the directions by cut/paste, define an environment variable with your bucket name.
```
export BUCKET=CoolStuff:/XYZ123456-bucket01
```
Do a test...check what is in the bucket.
```
rclone ls $BUCKET 
```
Create a text file and copy it to the bucket.
```
echo "hello!" > hello.txt
rclone copy hello.txt $BUCKET
```
Check is it really there.
```
rclone ls $BUCKET
```
Check the GUI too. [OSN Storage Portal](https://portal.osn.xsede.org)

When I do the `ls`, I get the following. It lists all my 'test' uploads.  The numbers on the left are file sizes.
```
(base) [llowe@login02 ~]$ rclone ls $BUCKET 
   129634 YT Thumbnail Requesting Consultation.png
        7 hello.txt
        7 hello2.txt
     5010 install-libs.txt
    72592 yellow_cube.png
```

## Adding users

To do this, you must be a 'data manager'.  On the OSN Storage Portal, you would see something like
* XYZ123456_Firstname_Lastname (manage)

Click 'manage'.  If you have an XSEDE allocation, all the members in the project given access to OSN should be listed, along with a red button to Remove. (Check access by going to the [XSEDE User Portal](https://portal.xsede.org/group/xup/add-remove-user).  Open a help ticket with XSEDE/OSN at help@xsede.org if the members are not listed.)

If you click the link for 'Add a user to this project', your options are limited to a pre-populated dropdown menu.  If a member is already listed in the table, they will not appear in the dropdown menu; if you need to change the role of a member, you have to click the red Remove button to remove them first.  Once removed, you can find them in the dropdown and choose the new role.

## Example
For this example, I want to copy the results from a hydrodynamics model that I ran on Expanse.  The group for my XSEDE allocation is `xyz123`. 

First, set the environment:
```
module load cpu/0.15.4
module load rclone/1.56.0
export BUCKET="CoolStuff:/XYZ123456-bucket01"
```
My model runs are in the scratch space, so I go there:
```
cd /expanse/lustre/projects/xyz123/$USER
```
My output is in the directory 'HydroFiles'. To copy the directory to OSN, I do:
```
rclone copy HydroFiles $BUCKET/HydroFiles
```

To keep a transfer running in the background, you can use `nohup`:
```
nohup rclone copy HydroFiles $BUCKET/HydroFiles & 
```

I heard `screen` might be better.  I never tried that.  When I do, I'll add some instructions here.

