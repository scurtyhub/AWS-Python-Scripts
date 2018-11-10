# AWS security check python script
Use this script to check for different security controls in your AWS account.

Dependencies
=======
Make sure you have [Python](https://www.python.org/downloads/) installed and PATH variable set.

Ubuntu
-----
If you don't have ```pip``` for Python:
```
sudo apt-get install python-pip
```
You will need modules ```requests``` installed, which are in ```requirements.txt```
```
pip install -r requirements.txt
```

Using script
-----
Before running the script, please make sure you have [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) installed. Create an Access key in your AWS account with proper permissions and [configure aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) it on your machine.

```
python AWS-Python-Scripts.py [-h] [-aU] [-cM] [-pP] [-aK] [-uA] [-pN]
OR
python AWS-Python-Scripts.py [--help] [--allUsers] [--checkMFA] [--checkPasswordPolicy] [--listAccessKeys] [--unUsedAccessKeys] [--passwordNotUpdated]
```

