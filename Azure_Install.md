# Deploying the Function App in Azure via Docker Container

## Function Deployment

- Push the image to a docker hub of your choice. You can use Azure Container Registry for this. If you do, tag the image \<Login Server\>/\<container name\>(:\<Version\>).
- Create the Function App in a Resource Group and choose **'Docker Container'** for the publish setting. \
  Note: This requires an App Service Plan (recommended) or [Functions Premium Plan](https://docs.microsoft.com/en-us/azure/azure-functions/functions-premium-plan?tabs=portal)
- In your Function App navigate to the Deployment Center, choose **'Container Registry'** and configure accordingly. Copy the webhook URL at the bottom of the page.
- Configure the webhook URL in your container registry.

## Azure AD Authentication

- Create a new App Registration in AzureAD.
- Add a secret under **'Certificates & secrets'** and make sure to note the value.
- Under **'Expose an API'** click **'Set'** next to **'Application ID URI'** and just save and note the provided value.
- In the overview click **'Endpoints'** and note the **'OAuth 2.0 token endpoint (v2)'** value.
- Also note the tenant ID from the tenant where the app is registered.
- In your Function App go to the **'Authentication'** section, click **'Add a provider'** and choose **'Microsoft'**
- Fill in the ClientID and Secret from the App Registration
- Issuer URL: `https://sts.windows.net/<TenantID>/`
- Allowed Token Audiences: The **'Application ID URI'** from the App Registration

In order to authenticate against the API use the following OAuth2 configuration:

- Access Token URL: **OAuth 2.0 token endpoint (v2)**
- Client ID: **Client ID** from the App Registration
- Client Secret: **Client Secret** generated in the App Registration
- Scope: **\<Application ID URI\>/.default**
