import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { map, catchError, switchMap, mergeMap } from 'rxjs/operators';

import { Actions, createEffect, ofType } from '@ngrx/effects';
import {
  SpecsService,
  SpecService,
  CredentialsService,
} from '@open-alchemy/package-sdk';
import { OAuthService } from 'angular-oauth2-oidc';

import * as PackageActions from './package.actions';

@Injectable()
export class PackageEffects {
  listSpecs$ = createEffect(() =>
    this.actions$.pipe(
      ofType(
        PackageActions.specsComponentOnInit.type,
        PackageActions.specsComponentRefresh.type,
        PackageActions.packageApiDeleteSpecsSpecNameSuccess.type
      ),
      switchMap(() =>
        this.specsService
          .list$({
            accessToken: this.oAuthService.getAccessToken(),
          })
          .pipe(
            map((specInfos) =>
              PackageActions.packageApiListSpecsSuccess({ specInfos })
            ),
            catchError(() => of(PackageActions.packageApiListSpecsError()))
          )
      )
    )
  );

  deleteSpecsSpecId$ = createEffect(() =>
    this.actions$.pipe(
      ofType(PackageActions.specsComponentDeleteSpec),
      mergeMap((action) =>
        this.specService
          .delete$({
            accessToken: this.oAuthService.getAccessToken(),
            name: action.specName,
          })
          .pipe(
            map(() => PackageActions.packageApiDeleteSpecsSpecNameSuccess()),
            catchError(() =>
              of(PackageActions.packageApiDeleteSpecsSpecNameError())
            )
          )
      )
    )
  );

  getCredentials$ = createEffect(() =>
    this.actions$.pipe(
      ofType(PackageActions.specsComponentOnInit.type),
      switchMap(() =>
        this.credentialsService
          .get$({
            accessToken: this.oAuthService.getAccessToken(),
          })
          .pipe(
            map((credentials) =>
              PackageActions.packageApiGetCredentialsSuccess({ credentials })
            ),
            catchError(() => of(PackageActions.packageApiGetCredentialsError()))
          )
      )
    )
  );

  constructor(
    private actions$: Actions,
    private oAuthService: OAuthService,
    private specsService: SpecsService,
    private specService: SpecService,
    private credentialsService: CredentialsService
  ) {}
}
