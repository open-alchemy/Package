import { Injectable } from '@angular/core';

import { createSelector, select } from '@ngrx/store';
import { Store } from '@ngrx/store';

import * as PackageActions from './package.actions';
import { PackageState } from './package.reducer';
import { SpecName } from './types';
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
  specs$ = this.store.pipe(select(selectSpecs));
  credentials$ = this.store.pipe(select(selectCredentials));

  constructor(private store: Store<AppState>) {}

  specsComponentOnInit(): void {
    this.store.dispatch(PackageActions.specsComponentOnInit());
  }

  specsComponentRefresh(): void {
    this.store.dispatch(PackageActions.specsComponentRefresh());
  }

  specsComponentDeleteSpec(specName: SpecName): void {
    this.store.dispatch(PackageActions.specsComponentDeleteSpec({ specName }));
  }
}
