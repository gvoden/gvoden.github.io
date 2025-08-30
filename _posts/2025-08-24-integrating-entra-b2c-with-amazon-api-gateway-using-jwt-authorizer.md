---
layout: post
title: "Integrating Entra B2C with Amazon API Gateway using JWT authorizer"
date: 2025-08-24T18:13:34
---

* * *

### Integrating Entra B2C with Amazon API Gateway using JWT authorizer

Entra ID can integrate with Amazon API Gateway using the Oauth2 authorization protocol. This is particularly useful if you want to secure APIs for machine to machine calls and you are familiar with Azure and choose not to use Amazon Cognito or an alternative IdP. The below diagram depicts a Entra ID B2C integration for the Client Credentials oauth grant:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-0.png)High level architecture, open sourced, courtesy of <https://github.com/secinaction101/azureadawsapigateway>

Step by step configuration can be found in this Microsoft article: <https://learn.microsoft.com/en-us/azure/active-directory-b2c/client-credentials-grant-flow?pivots=b2c-user-flow>

Note on how to get started: a Entra ID B2C tenant is required. You can use a free trial or pay-as-you-go Azure environment. You will also need an AWS account to create an API Gateway (I believe it only charges you if you have a large number of API calls, otherwise the cost is minimal). I used this site to poll fake data through the gateway using Postman: <https://jsonplaceholder.typicode.com/>

Azure side configuration looks as follows:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-1.png)

You need to create 2 App registrations in Azure B2C (make sure to create a Azure B2C directory first, do not use the default Azure AD (Entra ID).

App1 represents the client credentials app, and App2 represents the Web API you will be calling. Note that these are just security configuration in your IdP.

Example oauth flow trigger using Postman:

  1. We pass the client_id, client_secret and scope in a POST request
  2. The endpoint returns the access token (JWT token) that we then use to access the HTTP endpoint behind Amazon API Gateway



![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-2.png)

NOTE: You can decode the token to see the values it contains, such as scope, issuer, audience etc by going to jwt.io and pasting the value:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-3.png)

We then take the JWT token and pass that in the Authorization header to be used in the request to the API Gateway endpoint, the request is successful as we see mock data being returned, which means our token was authorized by the AWS API Gateway JWT authorizer:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-4.jpg)

Additional security can be achieved by adding scopes/permissions in the Client credentials app in Entra B2C which will be encoded in the JWT. On API Gateway side, the authorizer can validate the scopes after decoding the token.

Sample AWS API Gateway configuration can be seen below:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-5.png)

Revoking the app.read permissions on the Client Credentials App side in Azure B2C will result in a “Forbidden” HTTP response like so:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-6.png)

Postman test results:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-7.png)

This is because the JWT token no longer carries the app.read permissions:

![](/assets/images/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-8.png)

A few gotchas I encountered:

Flows configuration button missing in the GUI. This was super tricky as I had started configuring everything in the default Entra ID directory and not the B2C, so I had to repeat the whole configuration from scratch.

Also, this article came in handy while troubleshooting the configurations: <https://stackoverflow.com/questions/72781554/azure-ad-b2c-breaks-oidc-spec>

By [Georgi_V](https://medium.com/@gvoden) on [April 22, 2024](https://medium.com/p/926d8966141e).

[Canonical link](https://medium.com/@gvoden/integrating-entra-b2c-with-amazon-api-gateway-using-jwt-authorizer-926d8966141e)

Exported from [Medium](https://medium.com) on August 24, 2025.
