import { Action, createReducer, on } from '@ngrx/store';
import { SpecInfo, Credentials } from '@open-alchemy/package-sdk';

export { SpecInfo, Credentials };

import * as PackageActions from './package.actions';

export interface SpecsState {
  specInfos: SpecInfo[];
  success: boolean | null;
  loading: boolean;
}
export interface CredentialsState {
  value: Credentials | null;
  success: boolean | null;
  loading: boolean;
}
export interface PackageState {
  specs: SpecsState;
  credentials: CredentialsState;
}
export const initialState: PackageState = {
  specs: {
    specInfos: [],
    success: null,
    loading: false,
  },
  credentials: {
    value: null,
    success: null,
    loading: false,
  },
};

const packageReducerValue = createReducer(
  initialState,
  on(PackageActions.specsComponentOnInit, (state) => ({
    ...state,
    specs: { specInfos: [], success: null, loading: true },
    credentials: { value: null, success: null, loading: true },
  })),
  on(PackageActions.specsComponentRefresh, (state) => ({
    ...state,
    specs: {
      specInfos: [...state.specs.specInfos],
      success: null,
      loading: true,
    },
  })),
  on(PackageActions.packageApiListSpecsSuccess, (state, action) => ({
    ...state,
    specs: { specInfos: [...action.specInfos], success: true, loading: false },
  })),
  on(PackageActions.packageApiListSpecsError, (state) => ({
    ...state,
    specs: { specInfos: [], success: false, loading: false },
  })),
  on(PackageActions.packageApiGetCredentialsSuccess, (state, action) => ({
    ...state,
    credentials: {
      value: { ...action.credentials },
      success: true,
      loading: false,
    },
  })),
  on(PackageActions.packageApiGetCredentialsError, (state) => ({
    ...state,
    credentials: { value: null, success: false, loading: false },
  }))
);

export function packageReducer(
  state: PackageState | undefined,
  action: Action
) {
  return packageReducerValue(state, action);
}
