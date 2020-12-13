import { SpecInfo } from '@open-alchemy/package-sdk';

import { initialState, packageReducer } from './package.reducer';
import * as PackageActions from './package.actions';

const SPEC_INFOS: SpecInfo[] = [
  {
    spec_id: 'spec id 1',
    version: 'version 1',
    model_count: 1,
  },
];

describe('packageReducer', () => {
  [
    {
      description: 'initial state: undefined, action: specs component on init',
      expectation: 'should set loading to true',
      initialState: undefined,
      action: PackageActions.specsComponentOnInit(),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: [],
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
          specInfos: [],
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
          specInfos: [],
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
          specInfos: [],
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
          specInfos: [],
          success: null,
          loading: true,
        },
      },
      action: PackageActions.packageApiListSpecsError(),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: [],
          success: false,
          loading: false,
        },
      },
    },
    {
      description:
        'initial state: specs loaded, action: specs component refresh',
      expectation:
        'should set loading to true, success to null and leave the specs',
      initialState: {
        ...initialState,
        specs: {
          specInfos: SPEC_INFOS,
          success: true,
          loading: false,
        },
      },
      action: PackageActions.specsComponentRefresh(),
      expectedFinalState: {
        ...initialState,
        specs: {
          specInfos: SPEC_INFOS,
          success: null,
          loading: true,
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
          expect(packageReducer(initialState, action)).toEqual(
            expectedFinalState
          );
        });
      });
    }
  );
});
