import { Injectable } from '@angular/core';
import {
  CanActivate,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
} from '@angular/router';

import { OAuthService } from 'angular-oauth2-oidc';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private oAuthService: OAuthService) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    // Check for valid tokens
    const hasIdToken = this.oAuthService.hasValidIdToken();
    const hasAccessToken = this.oAuthService.hasValidAccessToken();
    const canActivate = hasIdToken && hasAccessToken;

    if (!canActivate) {
      // Store the proposed path
      sessionStorage.setItem('signInComplete.ReturnPath', state.url);

      // Log the user in
      this.oAuthService.initLoginFlow();
    }

    return canActivate;
  }
}
