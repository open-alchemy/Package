import { SpecInfo, Credentials } from '@open-alchemy/package-sdk';

import {
  initialState as packageInitialState,
  packageReducer,
} from './package.reducer';
import * as PackageActions from './package.actions';

// Front end does not control names of properties
const SPEC_INFOS: SpecInfo[] = [
  {
    id: 'spec id 1',
    // eslint-disable-next-line @typescript-eslint/naming-convention
    version: 'version 1',
    // eslint-disable-next-line @typescript-eslint/naming-convention
    model_count: 1,
  },
];
const CREDENTIALS: Credentials = {
  // eslint-disable-next-line @typescript-eslint/naming-convention
  public_key: 'public key 1',
  // eslint-disable-next-line @typescript-eslint/naming-convention
  secret_key: 'secret key 1',
};

describe('packageReducer', () => {
  [
    {
      description: 'initial state: undefined, action: specs component on init',
      expectation: 'should set loading to true',
      initialState: undefined,
      action: PackageActions.specsComponentOnInit(),
      expectedFinalState: {
        ...packageInitialState,
        specs: {
          specInfos: [],
          success: null,
          loading: true,
        },
        credentials: {
          value: null,
          success: null,
          loading: true,
        },
      },
    },
    {
      description: 'initial state: default, action: specs component on init',
      expectation: 'should set loading to true',
      initialState: packageInitialState,
      action: PackageActions.specsComponentOnInit(),
      expectedFinalState: {
        ...packageInitialState,
        specs: {
          specInfos: [],
          success: null,
          loading: true,
        },
        credentials: {
          value: null,
          success: null,
          loading: true,
        },
      },
    },
    {
      description:
        'initial state: specs loaded, action: specs component on init',
      expectation:
        'should set loading to true and clear credentials, specInfos and success',
      initialState: {
        ...packageInitialState,
        specs: {
          specInfos: SPEC_INFOS,
          success: true,
          loading: false,
        },
        credentials: {
          value: CREDENTIALS,
          success: true,
          loading: false,
        },
      },
      action: PackageActions.specsComponentOnInit(),
      expectedFinalState: {
        ...packageInitialState,
        specs: {
          specInfos: [],
          success: null,
          loading: true,
        },
        credentials: {
          value: null,
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
        ...packageInitialState,
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
        ...packageInitialState,
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
        ...packageInitialState,
        specs: {
          specInfos: [],
          success: null,
          loading: true,
        },
      },
      action: PackageActions.packageApiListSpecsError(),
      expectedFinalState: {
        ...packageInitialState,
        specs: {
          specInfos: [],
          success: false,
          loading: false,
        },
      },
    },
    {
      description:
        'initial state: credentials loading, action: package api get credentials success',
      expectation:
        'should set loading to false, success to true and copy credentials infos into state',
      initialState: {
        ...packageInitialState,
        credentials: {
          value: null,
          success: null,
          loading: true,
        },
      },
      action: PackageActions.packageApiGetCredentialsSuccess({
        credentials: CREDENTIALS,
      }),
      expectedFinalState: {
        ...packageInitialState,
        credentials: {
          value: CREDENTIALS,
          success: true,
          loading: false,
        },
      },
    },
    {
      description:
        'initial state: specs loading, action: package api get credentials error',
      expectation: 'should set loading to false, success to false',
      initialState: {
        ...packageInitialState,
        credentials: {
          value: null,
          success: null,
          loading: true,
        },
      },
      action: PackageActions.packageApiGetCredentialsError(),
      expectedFinalState: {
        ...packageInitialState,
        credentials: {
          value: null,
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
        ...packageInitialState,
        specs: {
          specInfos: SPEC_INFOS,
          success: true,
          loading: false,
        },
      },
      action: PackageActions.specsComponentRefresh(),
      expectedFinalState: {
        ...packageInitialState,
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
