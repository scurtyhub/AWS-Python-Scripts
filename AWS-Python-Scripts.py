import boto3
import argparse
from datetime import datetime, date

#function Arg parse
def user_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-aU","--allUsers", action="store_true", help="displays all users the AWS account")
    parser.add_argument("-cM","--checkMFA", action="store_true", help="displays all users with MFA Disabled in the AWS account")
    parser.add_argument("-pP","--checkPasswordPolicy", action="store_true", help="checks the password policy for the account")
    parser.add_argument("-aK","--ListAccessKeys", action="store_true", help="Lists the access keys for each user")
    return parser.parse_args()

#Function to list all the users in the account
def listAllUsers():
    user_instance = boto3.client('iam')
    response_user = user_instance.list_users()
    allUsersNames = []
    for k,v in response_user.items():
        if k == "Users":
            for i in v:
                for a,b in i.items():
                    if a == "UserName":
                        allUsersNames.append(b)
    return allUsersNames

#Function to check if MFA is enable for a user
def checkMFA(userMFA):
    user_instance = boto3.client('iam')
    response_MFA = user_instance.list_mfa_devices(UserName=userMFA)
    mfa_is_True = False
    for c,d in response_MFA.items():
        if c == "MFADevices":
            if len(d) != 0:
                mfa_is_True = True
    return mfa_is_True

if __name__ == '__main__':
    args = user_parse_args()

    if (args.allUsers | args.checkMFA | args.checkPasswordPolicy | args.ListAccessKeys) == False:
        print("Choose an argument.\n-h    help")
    else:
        #prints list of users in the AWS account
        if args.allUsers:
            UsersAll = listAllUsers()
            print("Total number of Users in the account:" + str(len(UsersAll)))
            print("\nUsers:")
            for i in UsersAll:
                print(i)

        #checks all users if MFA is enabled or disabled    
        if args.checkMFA:
            AllUsers = listAllUsers()
            for i in AllUsers:
                if checkMFA(i):
                    print("UserName: "+str(i)+", MFAEnabled: Yes")
                else:
                    print("UserName: "+str(i)+", MFAEnabled: No")
        
        #checks the password policy for the AWS account
        if args.checkPasswordPolicy:
            try:
                passwordPolicy = boto3.client('iam')
                responsePasswordPolicy = passwordPolicy.get_account_password_policy()['PasswordPolicy']
                print("Password Policy Set. Below are the Parameters:\n")
                for k,v in responsePasswordPolicy.items():
                    print(str(k)+": "+str(v))
            except passwordPolicy.exceptions.NoSuchEntityException:
                print("No Password Policy found!!!")     

        #lists the Access keys for the AWS accounts
        if args.ListAccessKeys:
            AllUsers = listAllUsers()
            accessKeys = boto3.client('iam')
            emptyAccounts = []
            for i in AllUsers:
                accessKeysresponse = accessKeys.list_access_keys(UserName=i)['AccessKeyMetadata']
                
                if len(accessKeysresponse) == 0:
                    emptyAccounts.append(i)
                else:
                    activeAccessKeys = {}
                    inactiveAccessKeys = {}
                    print("\nAcccount: "+str(i))
                    print("\tNumber of Access Keys for this account: "+str(len(accessKeysresponse)))
                    for a in accessKeysresponse:
                        if a['Status'] == 'Active':
                            activeAccessKeys[a['AccessKeyId']] = a['CreateDate']
                            print(datetime.utcnow().date()-a['CreateDate'].date())
                        else:
                            inactiveAccessKeys[a['AccessKeyId']] = a['CreateDate']
                    if len(activeAccessKeys) != 0:
                        print("\tActive No. of Access Keys:"+str(len(activeAccessKeys)))
                    if len(inactiveAccessKeys) != 0:
                        print("\tInactive No. of Access Keys:"+str(len(inactiveAccessKeys)))
            print("\nAccounts with NO Access Keys:")
            for i in emptyAccounts:
                print("\t"+str(i))




                



                                
