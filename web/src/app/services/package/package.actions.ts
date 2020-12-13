import { createAction, props } from '@ngrx/store';

import { types } from '@open-alchemy/package-sdk';

export const specsComponentOnInit = createAction('[specs component] on init');
export const packageApiListSpecsSuccess = createAction(
  '[package api] list specs success',
  props<{ specInfos: types.SpecInfo[] }>()
);
export const packageApiListSpecsError = createAction(
  '[package api] list specs error'
);
