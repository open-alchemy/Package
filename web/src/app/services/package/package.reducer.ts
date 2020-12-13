import { Action, createReducer, on } from '@ngrx/store';
import { SpecInfo } from '@open-alchemy/package-sdk';

export { SpecInfo };

import * as PackageActions from './package.actions';

export interface SpecsState {
  specInfos: SpecInfo[];
  success: boolean | null;
  loading: boolean;
}
export interface PackageState {
  specs: SpecsState;
}
export const initialState: PackageState = {
  specs: {
    specInfos: [],
    success: null,
    loading: false,
  },
};

const _packageReducer = createReducer(
  initialState,
  on(PackageActions.specsComponentOnInit, (state) => ({
    ...state,
    specs: { specInfos: [], success: null, loading: true },
  })),
  on(PackageActions.specsComponentRefresh, (state) => ({
    ...state,
    specs: { specInfos: state.specs.specInfos, success: null, loading: true },
  })),
  on(PackageActions.packageApiListSpecsSuccess, (state, action) => ({
    ...state,
    specs: { specInfos: action.specInfos, success: true, loading: false },
  })),
  on(PackageActions.packageApiListSpecsError, (state) => ({
    ...state,
    specs: { specInfos: [], success: false, loading: false },
  }))
);

export function packageReducer(
  state: PackageState | undefined,
  action: Action
) {
  return _packageReducer(state, action);
}
