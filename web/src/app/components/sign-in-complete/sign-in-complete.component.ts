import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { filter } from 'rxjs/operators';

import { OAuthService } from 'angular-oauth2-oidc';

import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-sign-in-complete',
  templateUrl: './sign-in-complete.component.html',
  styleUrls: ['./sign-in-complete.component.css'],
})
export class SignInCompleteComponent implements OnInit {
  constructor(private router: Router, private oAuthService: OAuthService) {}

  ngOnInit(): void {
    const subscription = this.oAuthService.events
      .pipe(filter((event) => event.type === 'token_received'))
      .subscribe(() => {
        // Navigate back to stored url
        let returnPath = sessionStorage.getItem(
          environment.signInCompleteReturnPathKey
        );
        if (returnPath === null) {
          returnPath = '';
        } else {
          sessionStorage.removeItem(environment.signInCompleteReturnPathKey);
        }
        this.router.navigate([returnPath]);

        // Stop any other navigation
        subscription.unsubscribe();
      });
  }
}
