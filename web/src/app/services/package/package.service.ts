import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { createSelector, select } from '@ngrx/store';
import { Store } from '@ngrx/store';

import * as PackageActions from './package.actions';
import { PackageState, SpecsState } from './package.reducer';
import { AppState, selectPackage } from '../app.state';

const selectSpecs = createSelector(
  selectPackage,
  (state: PackageState) => state.specs
);

@Injectable({ providedIn: 'root' })
export class PackageService {
  specs$: Observable<SpecsState>;

  constructor(private store: Store<AppState>) {
    this.specs$ = store.pipe(select(selectSpecs));
  }

  specsComponentOnInit(): void {
    this.store.dispatch(PackageActions.specsComponentOnInit());
  }

  specsComponentRefresh(): void {
    this.store.dispatch(PackageActions.specsComponentRefresh());
  }
}
