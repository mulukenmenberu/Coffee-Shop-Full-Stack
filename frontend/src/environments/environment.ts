
export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev--0iw-l86.us.auth0.com', // the auth0 domain prefix
    audience: 'http://localhost:4200/', // this is MY AUTH0 DOMAIN
    clientId: 'ySIXMAE9CFJTzMtSy3O1qAtNGnHgkL0C', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
