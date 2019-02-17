import boto3
import argparse
from datetime import datetime, date

#function Arg parse
def user_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-aU","--allUsers", action="store_true", help="displays all users the AWS account")
    parser.add_argument("-cM","--checkMFA", action="store_true", help="displays all users with MFA Disabled in the AWS account")
    parser.add_argument("-pP","--checkPasswordPolicy", action="store_true", help="checks the password policy for the account")
    parser.add_argument("-aK","--listAccessKeys", action="store_true", help="lists the access keys for each user")
    parser.add_argument("-uA","--unUsedAccessKeys", action="store_true", help="lists all the access keys not accessed in last 90 days")
    parser.add_argument("-pN","--passwordNotUpdated",action="store_true", help="lists all the accounts that has passwords not updated in the last 90 days")
    parser.add_argument("-nT","--noEc2Tags",action="store_true", help="lists all the Ec2 instances that have no tags")
    parser.add_argument("-uP","--unusedPassword",action="store_true", help="lists all the IAM users who's passwords were not used in last 90 days")
    parser.add_argument("-rM","--rootMFA",action="store_true", help="Checks if MFA is enabled or disabled on root account")
    parser.add_argument("-rA","--rootAccountAccessKeys",action="store_true", help="Checks if root account has access keys created")
    parser.add_argument("-mP","--IAMManagedPolicies",action="store_true", help="Checks if IAM account has managed policies directly attached")
    parser.add_argument("-lT","--listTrail",action="store_true", help="Lists Cloudtrail and its attributes")
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

    if (args.allUsers | args.checkMFA | args.checkPasswordPolicy | args.listAccessKeys | args.unUsedAccessKeys | args.passwordNotUpdated | args.noEc2Tags | args.unusedPassword | args.rootMFA | args.rootAccountAccessKeys | args.IAMManagedPolicies | args.listTrail ) == False:
        print("Choose an argument.\n-h    help")
    else:
        #prints list of users in the AWS account
        if args.allUsers:
            UsersAll = listAllUsers()
            print("Total number of Users in the account: " + str(len(UsersAll)))
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
                Min_Password_len = responsePasswordPolicy['MinimumPasswordLength']
                upperCase = responsePasswordPolicy['RequireUppercaseCharacters']
                print("Password Policy:\n")
                if(Min_Password_len < 14):
                    print("MinimumPasswordLength: "+str(Min_Password_len)+" (Recommended minimum password length is 14)")
                else:
                    print("MinimumPasswordLength: "+str(Min_Password_len))
                print()
                if('RequireUppercaseCharacters' in responsePasswordPolicy):
                    if(upperCase):
                        print("Current password policy is set to require upper case letters")
                    else:
                        print("Current password policy DOESN't require upper case letters (Recommeded to have minimum of atleast 1 upper case letter)")
                else:
                    print("RequireUppercaseCharacters is not set (Recommended to have minimum of atleast 1 upper case letter)")
                print()
                if('RequireLowercaseCharacters' in responsePasswordPolicy):
                    lowerCase = responsePasswordPolicy['RequireLowercaseCharacters']
                    if(lowerCase):
                        print("Current password policy is set to require lower case letters")
                    else:
                        print("Current password policy DOESN'T require lower case letters (Recommended to have minimum of atleast 1 lower case letter)")
                else:
                    print("RequireLowercaseCharacters is not set (Recommended to have minimum of atleast 1 lower case letter)")
                print()
                if('RequireSymbols' in responsePasswordPolicy):
                    requireSymbols = responsePasswordPolicy['RequireSymbols']
                    if(requireSymbols):
                        print("Current password policy is set to require symbols")
                    else:
                        print("Current password policy DOESN'T require symbols (Recommended to have minimum of atleast 1 symbol)")
                else:
                    print("RequireSymbols is not set (Recommended to have minimum of atleast 1 symbol)")
                print()
                if('RequireNumbers' in responsePasswordPolicy):
                    requireNumbers = responsePasswordPolicy['RequireNumbers']
                    if(requireNumbers):
                        print("Current password policy is set to require numbers")
                    else:
                        print("Current password policy DOESN'T require numbers (Recommended to have minimum of atleast 1 number)")
                else:
                    print("RequireNumbers is not set (Recommended to have minimum of atleast 1 number)")
                print()
                if('PasswordReusePrevention' in responsePasswordPolicy):
                    reusePassword = responsePasswordPolicy['PasswordReusePrevention']
                    if(reusePassword < 5):
                        print("PasswordReusePrevention is set to "+str(reusePassword)+" (Recommended to set password resuse prevention atleast 5!!!)")
                    else:
                        print("PasswordReusePrevention is set to "+str(reusePassword))
                else:
                    print("PasswordReusePrevention is not Set (Recommended to set password resuse prevention atleast 5!!!)")
                print()
                if('MaxPasswordAge' in responsePasswordPolicy):
                    maxpasswordage = responsePasswordPolicy['MaxPasswordAge']
                    if(maxpasswordage < 90):
                        print("MaxPasswordAge is "+str(maxpasswordage)+" (Recommended to have a maximum password age of 90 days)")
                    else:
                        print("MaxPasswordAge is "+str(maxpasswordage))
                else:
                    print("MaxPasswordAge is not set (Recommended to have a maximum password age of 90 days)")
                print()
            except passwordPolicy.exceptions.NoSuchEntityException:
                print("No Password Policy found!!!")     

        #lists the Access keys for the AWS accounts
        if args.listAccessKeys:
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
                    print("\nAccount: "+str(i))
                    print("\tNumber of Access Keys for this account: "+str(len(accessKeysresponse)))
                    for a in accessKeysresponse:
                        if a['Status'] == 'Active':
                            activeAccessKeys[a['AccessKeyId']] = a['CreateDate']
                            print("            Access Key: "+str(a['AccessKeyId'])+", Created "+str(datetime.utcnow().date()-a['CreateDate'].date())+" ago")
                        else:
                            inactiveAccessKeys[a['AccessKeyId']] = a['CreateDate']
                    if len(activeAccessKeys) != 0:
                        print("\tActive No. of Access Keys:"+str(len(activeAccessKeys)))
                    if len(inactiveAccessKeys) != 0:
                        print("\tInactive No. of Access Keys:"+str(len(inactiveAccessKeys)))
            print("\nAccounts with NO Access Keys:")
            for i in emptyAccounts:
                print("\t"+str(i))
        
        #Check if Access keys used in the last 90 days
        if args.unUsedAccessKeys:
            access_key = input("Please enter the access key you want to check the last time it was accessed: \n")
            unUsedAccessKey = boto3.client('iam')
            unUsed_response = unUsedAccessKey.get_access_key_last_used(AccessKeyId=access_key)
            number_of_days = str(datetime.utcnow().date() - unUsed_response['AccessKeyLastUsed']['LastUsedDate'].date())
            if (int(number_of_days.split(' ')[0])) > 89:
                print("Access Key was NOT assessed in last 90 days")
            else:
                print("Access Key was assessed in the last 90 days")
        
        #display all the accounts with passwords not updated in more than 90 days
        if args.passwordNotUpdated:
            UsersAll = listAllUsers()
            if len(UsersAll) == 0:
                print("\nNo Users found!!!")
            else:
                print()
                for i in UsersAll:
                    try:
                        client = boto3.client('iam')
                        response = client.get_login_profile(UserName=i)
                        passwordAge = int(str(datetime.utcnow().date() - response['LoginProfile']['CreateDate'].date()).split(' ')[0])
                        if(passwordAge > 89):
                            print("For user \""+str(i)+"\", password last updated "+str(passwordAge)+" days ago")
                    except client.exceptions.NoSuchEntityException:
                        print("For User \""+str(i)+"\", no password creation date found!!!")

        #display EC2 instances that doesn't have any tags
        if args.noEc2Tags:
            client = boto3.client('ec2')
            reservations = client.describe_instances()['Reservations']
            print("Ec2 instances with no tags and its state:")
            for i in reservations:
                if 'Tags' not in i['Instances'][0]:
                    print("Instance Id "+str(i['Instances'][0]['InstanceId'])+" and Instance state is "+str(i['Instances'][0]['State']['Name']))

        #lists accounts that were not logged into in the last 90 days
        if args.unusedPassword:
            user_instance = boto3.client('iam')
            response_user = user_instance.list_users()
            for i in response_user['Users']:
                if 'PasswordLastUsed' in i:
                    if (datetime.utcnow().date() != i['PasswordLastUsed'].date()):
                        password_age = int(str(datetime.utcnow().date()-i['PasswordLastUsed'].date()).split(' ')[0])
                        if password_age > 89:
                            print("For IAM user "+str(i['UserName'])+", Password last used is "+str(password_age)+" days ago")
        
        #Checks if MFA is enabled on the root account
        if args.rootMFA:
            client = boto3.client('iam')
            if(client.get_account_summary()['SummaryMap']['AccountMFAEnabled']):
                print("root MFA is enabled")
            else:
                print("root MFA is disabled (Recommended to enable MFA)")

        #Checks if root account has access keys created
        if args.rootAccountAccessKeys:
            client = boto3.client('iam')
            if(client.get_account_summary()['SummaryMap']['AccountAccessKeysPresent']):
                print("root account has Access keys created (Recommended to disable them)")
            else:
                print("root account has NO access keys")
        
        #Checks if IAM users has managed policies direclty attached
        if args.IAMManagedPolicies:
            client = boto3.client('iam')
            response = client.get_account_authorization_details(Filter=['User'])
            print()
            for i in response['UserDetailList']:
               print(str(i['UserName'])+" has "+str(len(i['AttachedManagedPolicies']))+" managed policies attached")
        
        #Lists Cloudtrail trails and its attributes
        if args.listTrail:
            client = boto3.client('cloudtrail')
            response = client.describe_trails()
            if len(response['trailList']) == 0:
                print("No trails found. Enable Cloudtrail on all regions")
            else:
                for i in response['trailList']:
                    trailStatus = client.get_trail_status(Name=i['Name'])
                    if trailStatus['IsLogging']:
                        StatusOn = "turned On"
                    else:
                        StatusOn = "turned Off (Recommended to be turned On)"
                    if i['IsMultiRegionTrail']:
                        regionAll = "True"
                    else:
                        regionAll = "False (Recommended to be enabled on ALL regions)"
                    if i['LogFileValidationEnabled']:
                        fileValidate = "Pass"
                    else:
                        fileValidate = "Fail (Recommended to turn On log file validation for log integrity check"
                    bucketClient = boto3.client('s3')
                    bucketResponse = client.get_bucket_encryption(Bucket=i['S3BucketName'])
                    print(str(i['Name'])+":")
                    print("    Logging to the bucket: "+str(i['S3BucketName']))
                    print("    Status: "+StatusOn)
                    print("    Logging on ALL regions: "+regionAll)
                    print("    Log file Integrity check: "+fileValidate)
