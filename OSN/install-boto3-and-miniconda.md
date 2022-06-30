# Installing boto3
SDK means Software Development Kit. If you know that already, you might think it is silly that I bothered to define that. If you only Fortran code, I bet you not only *didn't* know that, but you didn't care, and you might even kind of resent needing to know it now.

## The AWS SDK for Python is Boto3. 

To check whether your Python distribution already has boto3, do
```
python
import boto3
```

If it isn't installed, then on your favorite supercomputer, load the Python 3 module and use `pip install`.  On Expanse, you would do 
```
module load anaconda3
pip install boto3
```

If the only nonstandard Python library you will use is boto3, then you're done.

## Using Conda

If you use a bunch of different and perhaps complicated Python libraries, then you should probably never use `pip install`.  There is a chance that doing so will break all of your existing libraries, and your scripts won't work anymore.

I recommend using Conda.  If you or your supercomputer don't have Conda installed, then here are instructions to install it. 

Anaconda is a monster that takes a ton of space and contains a bunch of packages you don't need.  I recommend using miniconda for the base Conda install.

From the [Miniconda page](https://docs.conda.io/en/latest/miniconda.html), go to 'Latest Miniconda Installer Links', find the appropriate Platform, right-click on the link, 'Copy Link Address'of the installer, and download it using wget.  (If you are using 64-bit Linux, just copy the following.)
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

Run the installer
``
bash Miniconda3-latest-Linux-x86_64.sh
```

It will ask you to accept a licence agreement, and then ask where you want in installed.  'At home' I install to my home directory.  On a supercomputer, your home directory might be too small and you might install somewheres else.

After that, please see this [brilliant documentation](https://hpc.ncsu.edu/Software/Apps.php?app=Conda) on best practices for installing stuff with Conda.
