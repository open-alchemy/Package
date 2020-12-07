import { Component } from '@angular/core';

import { OAuthService, AuthConfig } from 'angular-oauth2-oidc';

const AUTH_CODE_FLOW_CONFIG: AuthConfig = {
  // Url of the Identity Provider
  issuer: 'https://cognito-idp.us-east-1.amazonaws.com/us-east-1_XBKoHuMO2',

  // URL of the SPA to redirect the user to after login
  redirectUri: `${window.location.origin}/sign-in-complete`,

  // The SPA's id. The SPA is registerd with this id at the auth-server
  // clientId: 'server.code',
  clientId: '334j6ddju1hkt6gdb1nodfidmb',

  responseType: 'code',

  // set the scope for the permissions the client should request
  // The first four are defined by OIDC.
  // Important: Request offline_access to get a refresh token
  // The api scope is a usecase specific one
  scope:
    'https://package.api.openalchemy.io/spec.read https://package.api.openalchemy.io/spec.write',

  showDebugInformation: true,

  strictDiscoveryDocumentValidation: false,
};

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'package';

  constructor(private oauthService: OAuthService) {
    this.oauthService.configure(AUTH_CODE_FLOW_CONFIG);
    this.oauthService.setStorage(localStorage);
    this.oauthService.loadDiscoveryDocumentAndTryLogin();
    this.oauthService.setupAutomaticSilentRefresh();
  }
}
