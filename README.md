# AWS security check python script
Use this script to check for different security controls in your AWS account.

Dependencies
=======
Make sure you have [Python](https://www.python.org/downloads/) installed and PATH variable set.

Mac OS
-----
If you don't have ```pip``` for Python:
```
sudo easy_install pip
```
You will need modules ```requests``` installed, which are in ```requirements.txt```
```
pip install -r requirements.txt
```

Using script
-----
Before running the script, please make sure you have [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) installed. Create an Access key in your AWS account with read permissions (they don't need admin privileges) and [configure aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) on your machine.

```
python AWS-Python-Scripts.py [-h] [-aU] [-cM] [-pP] [-aK] [-uA] [-pN] [-nT] [-uP] [-rM] [-rA] [-mP] [-lT]

python AWS-Python-Scripts.py [--help] [--allUsers] [--checkMFA] [--checkPasswordPolicy] [--listAccessKeys] [--unUsedAccessKeys] [--passwordNotUpdated] [--noEc2Tags] [--unusedPassword] [--rootMFA] [--rootAccountAccessKeys] [--IAMManagedPolicies] [--listTrail]
```

* ```--allUsers```: Lists all users in your AWS account.
* ``--checkMFA``: Checks and displays all the IAM users that has MFA disabled.
* ``--checkPasswordPolicy``: Checks the password policy for the account.
* ``--listAccessKeys``: Lists the access keys for each user.
* ``--unUsedAccessKeys``: Lists all the access keys not accessed in last 90 days.
* ``--passwordNotUpdated``: Lists all the accounts that has passwords not updated in the last 90 days.
* ``--noEc2Tags``: Lists Ec2 instance ids that doesn't have tags.
* ``--unusedPassword``: Lists IAM users that has passwords not accessed in last 90 days.
* ``--rootMFA``: Checks if MFA is enabled on the root account.
* ``--rootAccountAccessKeys``: Checks if root account has any access keys.
* ``--IAMManagedPolicies``: Checks if IAM users has managed policies directly attached
* ``--listTrail``: Lists Cloudtrail and its attributes in the account
 
Example:
-----

```
python AWS-Python-Scripts.py -aU
```

### Output:
```
Total number of Users in the account:6

Users:
awssecurity
deployment
test_user_123
test_user_password_policy
test_user_password_policy_two
test_user_check
```

