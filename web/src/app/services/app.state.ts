import { createFeatureSelector } from '@ngrx/store';

import { PackageState } from './package/package.reducer';

export interface AppState {
  package: PackageState;
}

export const selectPackage = createFeatureSelector<AppState, PackageState>(
  'package'
);
