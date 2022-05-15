# Loginrate

 There is a Login, Register & Account Verify APIs.
 
1. Login API:
 
i. Takes the user details as input and generates a unique login token and returns as
response in case of successful login, else in case of any error return the error
message
ii. 5 consecutive failed attempts for any user will lock the user account and the user
needs to reset the password to proceed. (Hint: Keep a lock counter in the user
table)
iii. The account must be verified, else the user is not allowed to login.
iv. Maintain login history (but successful and failure case)

2. Register API:

i. taking user details and check whether it is present or not.

c. Verification API:
i. The mail sent to the user is assumed to call this API on tapping verify button, the
API should validate the user account (GET request with a unique key to
recognizing the account being verified)

3. Reset Password:

i. In case the account is blocked, this API would be used to reset password. (Hint:
This would reset the lock counter and the user will be able to login.)

4.DB 
There is  two tables - user, login_history to meet the above task requirement.
