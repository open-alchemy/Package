import { types } from '@open-alchemy/package-sdk';

import { initialState, reducer } from './package.reducer';
import * as PackageActions from './package.actions';

const SPEC_INFOS: types.SpecInfo[] = [
  {
    spec_id: 'spec id 1',
    version: 'version 1',
    model_count: 1,
  },
];

describe('PackageReducer', () => {
  [
    {
      description: 'initial state: undefined, action: specs component on init',
      expectation: 'should set loading to true',
      initialState: undefined,
      action: PackageActions.specsComponentOnInit(),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: null,
          success: null,
          loading: true,
        },
      },
    },
    {
      description: 'initial state: default, action: specs component on init',
      expectation: 'should set loading to true',
      initialState,
      action: PackageActions.specsComponentOnInit(),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: null,
          success: null,
          loading: true,
        },
      },
    },
    {
      description:
        'initial state: specs loaded, action: specs component on init',
      expectation: 'should set loading to true and clear specInfos and success',
      initialState: {
        ...initialState,
        specs: {
          specInfos: SPEC_INFOS,
          success: true,
          loading: false,
        },
      },
      action: PackageActions.specsComponentOnInit(),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: null,
          success: null,
          loading: true,
        },
      },
    },
    {
      description:
        'initial state: specs loading, action: package api list specs success',
      expectation:
        'should set loading to false, success to true and copy spec infos into state',
      initialState: {
        ...initialState,
        specs: {
          specInfos: null,
          success: null,
          loading: true,
        },
      },
      action: PackageActions.packageApiListSpecsSuccess({
        specInfos: SPEC_INFOS,
      }),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: SPEC_INFOS,
          success: true,
          loading: false,
        },
      },
    },
    {
      description:
        'initial state: specs loading, action: package api list specs error',
      expectation: 'should set loading to false, success to false',
      initialState: {
        ...initialState,
        specs: {
          specInfos: null,
          success: null,
          loading: true,
        },
      },
      action: PackageActions.packageApiListSpecsError(),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: null,
          success: false,
          loading: false,
        },
      },
    },
  ].forEach(
    ({
      description,
      expectation,
      initialState,
      action,
      expectedFinalState,
    }) => {
      describe(description, () => {
        it(expectation, () => {
          expect(reducer(initialState, action)).toEqual(expectedFinalState);
        });
      });
    }
  );
});
