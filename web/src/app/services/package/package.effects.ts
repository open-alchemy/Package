import { Injectable } from '@angular/core';
import { from, of } from 'rxjs';
import { map, catchError, switchMap } from 'rxjs/operators';

import { Actions, createEffect, ofType } from '@ngrx/effects';
import { SpecsService } from '@open-alchemy/package-sdk';
import { OAuthService } from 'angular-oauth2-oidc';

import * as PackageActions from './package.actions';

@Injectable()
export class PackageEffects {
  constructor(
    private actions$: Actions,
    private oAuthService: OAuthService,
    private specsService: SpecsService
  ) {}

  listSpecs$ = createEffect(() =>
    this.actions$.pipe(
      ofType(PackageActions.specsComponentOnInit.type),
      switchMap(() =>
        from(
          this.specsService.list({
            accessToken: this.oAuthService.getAccessToken(),
          })
        ).pipe(
          map((specInfos) =>
            PackageActions.packageApiListSpecsSuccess({ specInfos })
          ),
          catchError(() => of(PackageActions.packageApiListSpecsError()))
        )
      )
    )
  );
}
