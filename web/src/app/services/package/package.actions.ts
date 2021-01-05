import { createAction, props } from '@ngrx/store';

import { SpecInfo, SpecName, Credentials } from './types';

export const specsComponentOnInit = createAction('[specs component] on init');
export const specsComponentRefresh = createAction('[specs component] refresh');
export const specsComponentDeleteSpec = createAction(
  '[specs component] delete spec',
  props<{ specName: SpecName }>()
);

export const packageApiListSpecsSuccess = createAction(
  '[package api] list specs success',
  props<{ specInfos: SpecInfo[] }>()
);
export const packageApiListSpecsError = createAction(
  '[package api] list specs error'
);
export const packageApiDeleteSpecsSpecNameSuccess = createAction(
  '[package api] delete specs spec id success'
);
export const packageApiDeleteSpecsSpecNameError = createAction(
  '[package api] delete specs spec id error'
);
export const packageApiGetCredentialsSuccess = createAction(
  '[package api] get credentials success',
  props<{ credentials: Credentials }>()
);
export const packageApiGetCredentialsError = createAction(
  '[package api] get credentials error'
);
