import { createAction, props } from '@ngrx/store';

import { SpecInfo, SpecId, Credentials } from './types';

export const specsComponentOnInit = createAction('[specs component] on init');
export const specsComponentRefresh = createAction('[specs component] refresh');
export const specsComponentDeleteSpec = createAction(
  '[specs component] delete spec',
  props<{ specId: SpecId }>()
);

export const packageApiListSpecsSuccess = createAction(
  '[package api] list specs success',
  props<{ specInfos: SpecInfo[] }>()
);
export const packageApiListSpecsError = createAction(
  '[package api] list specs error'
);
export const packageApiDeleteSpecsSpecIdSuccess = createAction(
  '[package api] delete specs spec id success'
);
export const packageApiDeleteSpecsSpecIdError = createAction(
  '[package api] delete specs spec id error'
);
export const packageApiGetCredentialsSuccess = createAction(
  '[package api] get credentials success',
  props<{ credentials: Credentials }>()
);
export const packageApiGetCredentialsError = createAction(
  '[package api] get credentials error'
);
