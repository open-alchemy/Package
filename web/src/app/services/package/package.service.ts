import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { createSelector, select } from '@ngrx/store';
import { Store } from '@ngrx/store';

import * as PackageActions from './package.actions';
import { PackageState, SpecsState, CredentialsState } from './package.reducer';
import { SpecId } from './types';
import { AppState, selectPackage } from '../app.state';

const selectSpecs = createSelector(
  selectPackage,
  (state: PackageState) => state.specs
);

const selectCredentials = createSelector(
  selectPackage,
  (state: PackageState) => state.credentials
);

@Injectable({ providedIn: 'root' })
export class PackageService {
  specs$: Observable<SpecsState>;
  credentials$: Observable<CredentialsState>;

  constructor(private store: Store<AppState>) {
    this.specs$ = store.pipe(select(selectSpecs));
    this.credentials$ = store.pipe(select(selectCredentials));
  }

  specsComponentOnInit(): void {
    this.store.dispatch(PackageActions.specsComponentOnInit());
  }

  specsComponentRefresh(): void {
    this.store.dispatch(PackageActions.specsComponentRefresh());
  }

  specsComponentDeleteSpec(specId: SpecId): void {
    this.store.dispatch(PackageActions.specsComponentDeleteSpec({ specId }));
  }
}
