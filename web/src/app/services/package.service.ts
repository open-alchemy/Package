import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { filter } from 'rxjs/operators';

import { OAuthService } from 'angular-oauth2-oidc';

import { SpecInfo } from '../openapi/models';
import { isNotNullUndefined } from '../helpers/filters';

@Injectable({ providedIn: 'root' })
export class PackageService {
  constructor(
    private oAuthService: OAuthService,
    private httpClient: HttpClient
  ) {}

  private mSpecs$ = new BehaviorSubject<SpecInfo | null>(null);

  specs$(): Observable<SpecInfo> {
    return this.mSpecs$.pipe(filter(isNotNullUndefined));
  }
}
