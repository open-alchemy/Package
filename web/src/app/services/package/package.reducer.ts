import { Action, createReducer, on } from '@ngrx/store';
import { SpecInfo } from '@open-alchemy/package-sdk';

import * as PackageActions from './package.actions';

export interface State {
  specs: {
    specInfos: SpecInfo[] | null;
    success: boolean | null;
    loading: boolean;
  };
}
export const initialState: State = {
  specs: {
    specInfos: null,
    success: null,
    loading: false,
  },
};

const packageReducer = createReducer(
  initialState,
  on(PackageActions.specsComponentOnInit, (state) => ({
    ...state,
    specs: { specInfos: null, success: null, loading: true },
  })),
  on(PackageActions.packageApiListSpecsSuccess, (state, action) => ({
    ...state,
    specs: { specInfos: action.specInfos, success: true, loading: false },
  })),
  on(PackageActions.packageApiListSpecsError, (state) => ({
    ...state,
    specs: { specInfos: null, success: false, loading: false },
  }))
);

export function reducer(state: State | undefined, action: Action) {
  return packageReducer(state, action);
}
