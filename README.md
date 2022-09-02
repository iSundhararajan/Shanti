# Shanti

Shanti in Hindi means Peace. This is a platform where people come to find peace. 

Shanti provides all of it's users, a community, a safe space where they can open up and discuss whatever's troubling them.

It is essentially a chatting platform where users can dedicate one session/server to any particular topic they want to have a conversation on.
Once they are in, they gain access to unlimited real time chat servers where countless decisions, events and feelings are being discussed.

For security, each user has to go through OTP verification which has been implemented with the help of twilio.

This repo is the backend for shaanti, a brief description of API end points is given bellow:

```/otp```
 - sends an otp to the given mobile number and country code
```
{
  "countryCode": "+91",
  "phone": "1234567890"
}
```

```users/signup```
 - users can create new accounts after verifying otp
 
 ```users/login```
 - to authenticate users and grant them access to the platform
 ```
 {
   "countryCode": "+91",
   "phone": "1234567890",
   "otp": "123456"
 }
 ```
 
 ```/sessions/create```
  - create a new session
  
 ```/message/send```
 
 - send a message to a server
 
 ```messages/<topic>```
 
  - diplay complete chat history of the chat room (if user is authenticated)
  
  
