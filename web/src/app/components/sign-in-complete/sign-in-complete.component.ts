import { Component, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';

import { filter } from 'rxjs/operators';

import { OAuthService, EventType } from 'angular-oauth2-oidc';

@Component({
  selector: 'app-sign-in-complete',
  templateUrl: './sign-in-complete.component.html',
  styleUrls: ['./sign-in-complete.component.css'],
})
export class SignInCompleteComponent implements AfterViewInit {
  constructor(private router: Router, private oAuthService: OAuthService) {}

  ngAfterViewInit(): void {
    this.oAuthService.events
      .pipe(filter((event) => event.type === 'token_received'))
      .subscribe(() => {
        const returnPath = sessionStorage.getItem('signInComplete.ReturnPath');
        sessionStorage.removeItem('signInComplete.ReturnPath');
        if (returnPath) {
          this.router.navigate([returnPath]);
        } else {
          this.router.navigate(['']);
        }
      });
  }
}
