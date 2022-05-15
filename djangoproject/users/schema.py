import graphene
import graphql_jwt
from .models import Suser,loginhistory
from graphql_auth import mutations
from graphene_django import DjangoObjectType
from graphql_jwt.shortcuts import get_token
from django.contrib.auth.hashers import check_password
import datetime

class UserType(DjangoObjectType):
    class Meta:
        model = Suser


class LoginUser(graphene.Mutation):

    user = graphene.Field(UserType)
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        log_id = Suser.objects.get(email=email)
        active=log_id.is_active #store users active state
        uid=log_id.id #store user's id
        if active == False: #if user's active status is False show them error
            raise Exception('Your account is deactivate')
        if Suser.objects.filter(email=email).exists(): # check if user's email is exists
            u = Suser.objects.get(email=email)
            haspassword = u.password  #  store user's password
            token = ''

            if Suser.objects.filter(email=email).exists() and check_password(password, haspassword):
                user = Suser.objects.get(email=email)
                token = get_token(user) # get user's token
                ab=loginhistory(sid=uid,status="Succes",login_time=datetime.datetime.now()) #if login successfull then it maintain a database of login history of status=success
                ab.save()
            else:
                ab=loginhistory(sid=uid,status="Fail",login_time=datetime.datetime.now())#if login fail then it maintain a database of login history of status=Fail
                fail_count=loginhistory.objects.filter(status="Fail").count() #count Fail login
                if fail_count>6: # if fail count not exceed 5 attempt
                    su = Suser.objects.filter(id=uid).update(is_active= False,login_count=fail_count) #user's active status set to False
                    su.save()
                    raise Exception('Your account is deactivate')
                raise Exception("Auth credential is not provided")

                ab.save()
        return LoginUser(user=user, token=token)


class CreateUser(graphene.Mutation): # User Registrations
    user = graphene.Field(UserType)

    # s_user=graphene.Field(S_user)
    class Arguments:

        username = graphene.String(required=True)
        phone_no = graphene.Int(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, phone_no, email):

        if Suser.objects.filter(email=email).exists(): #filter and check email with email entered by user
            raise Exception("email already used")
        users = Suser.objects.all()
        for user in users:
            if user.check_password(password): #check password with password entered by user
                raise Exception("password already used")
        user = Suser(
            username=username,
            phone_no=phone_no,
            email=email,
        )
        user.set_password(password)

        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    login_user = LoginUser.Field()   #login Api
    create_user = CreateUser.Field()   #registration of user Api
    verify_account = mutations.VerifyAccount.Field()  #User Account Verification Api
    send_password_reset_email = mutations.SendPasswordResetEmail.Field() # Send Password Reset link  through email Api
    password_reset=mutations.PasswordReset.Field() # Password Reset link
    resend_activation_email = mutations.ResendActivationEmail.Field() # resend Activation Link
class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info): #All User Information
        return Suser.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)