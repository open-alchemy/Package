import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { map, catchError, switchMap, mergeMap } from 'rxjs/operators';

import { Actions, createEffect, ofType } from '@ngrx/effects';
import { SpecsService, SpecService } from '@open-alchemy/package-sdk';
import { OAuthService } from 'angular-oauth2-oidc';

import * as PackageActions from './package.actions';

@Injectable()
export class PackageEffects {
  constructor(
    private actions$: Actions,
    private oAuthService: OAuthService,
    private specsService: SpecsService,
    private specService: SpecService
  ) {}

  listSpecs$ = createEffect(() =>
    this.actions$.pipe(
      ofType(
        PackageActions.specsComponentOnInit.type,
        PackageActions.specsComponentRefresh.type,
        PackageActions.packageApiDeleteSpecsSpecIdSuccess.type
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
      ofType(PackageActions.specsComponentDeleteSpecId),
      mergeMap((action) =>
        this.specService
          .delete$({
            accessToken: this.oAuthService.getAccessToken(),
            id: action.specId,
          })
          .pipe(
            map(() => PackageActions.packageApiDeleteSpecsSpecIdSuccess()),
            catchError(() =>
              of(PackageActions.packageApiDeleteSpecsSpecIdError())
            )
          )
      )
    )
  );
}
