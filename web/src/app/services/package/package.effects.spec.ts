import { Observable } from 'rxjs';
import { TestScheduler } from 'rxjs/testing';

import { Action } from '@ngrx/store';
import { OAuthService } from 'angular-oauth2-oidc';
import { SpecsService, SpecService, SpecInfo } from '@open-alchemy/package-sdk';

import { PackageEffects } from './package.effects';
import * as PackageActions from './package.actions';

const SPEC_INFOS_1: SpecInfo[] = [
  {
    spec_id: 'spec id 1',
    version: 'version 1',
    model_count: 1,
  },
];
const SPEC_INFOS_2: SpecInfo[] = [
  {
    spec_id: 'spec id 2',
    version: 'version 2',
    model_count: 2,
  },
];

describe('PackageEffects', () => {
  let actions$: Observable<Action>;
  let effects: PackageEffects;
  let oAuthServiceSpy: jasmine.SpyObj<OAuthService>;
  let specsServiceSpy: jasmine.SpyObj<SpecsService>;
  let specServiceSpy: jasmine.SpyObj<SpecService>;
  let testScheduler: TestScheduler;

  const accessToken = 'access token 1';

  beforeEach(() => {
    oAuthServiceSpy = jasmine.createSpyObj('OAuthService', ['getAccessToken']);
    oAuthServiceSpy.getAccessToken.and.returnValue(accessToken);
    specsServiceSpy = jasmine.createSpyObj('SpecsService', ['list$']);
    specServiceSpy = jasmine.createSpyObj('SpecService', ['delete$']);

    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).toEqual(expected);
    });
  });

  describe('listSpecs$', () => {
    ([
      {
        description: 'empty actions',
        expectation: 'should return empty actions',
        actionsMarbles: '',
        actionsValues: {},
        specsServiceListReturnValues: [],
        expectedMarbles: '',
        expectedValues: {},
      },
      {
        description: 'different action actions',
        expectation: 'should return empty actions',
        actionsMarbles: 'a',
        actionsValues: { a: PackageActions.packageApiListSpecsError() },
        specsServiceListReturnValues: [],
        expectedMarbles: '',
        expectedValues: {},
      },
      {
        description:
          'single specs component on init action actions list$ returns spec infos',
        expectation: 'should return single success action actions',
        actionsMarbles: 'a',
        actionsValues: { a: PackageActions.specsComponentOnInit() },
        specsServiceListReturnValues: [
          { marbles: '-b|', values: { b: SPEC_INFOS_1 } },
        ],
        expectedMarbles: '-b',
        expectedValues: {
          b: PackageActions.packageApiListSpecsSuccess({
            specInfos: SPEC_INFOS_1,
          }),
        },
      },
      {
        description:
          'single specs component on refresh action actions list$ returns spec infos',
        expectation: 'should return single success action actions',
        actionsMarbles: 'a',
        actionsValues: { a: PackageActions.specsComponentRefresh() },
        specsServiceListReturnValues: [
          { marbles: '-b|', values: { b: SPEC_INFOS_1 } },
        ],
        expectedMarbles: '-b',
        expectedValues: {
          b: PackageActions.packageApiListSpecsSuccess({
            specInfos: SPEC_INFOS_1,
          }),
        },
      },
      {
        description:
          'single package api delete specs spec id success action actions list$ returns spec infos',
        expectation: 'should return single success action actions',
        actionsMarbles: 'a',
        actionsValues: {
          a: PackageActions.packageApiDeleteSpecsSpecIdSuccess(),
        },
        specsServiceListReturnValues: [
          { marbles: '-b|', values: { b: SPEC_INFOS_1 } },
        ],
        expectedMarbles: '-b',
        expectedValues: {
          b: PackageActions.packageApiListSpecsSuccess({
            specInfos: SPEC_INFOS_1,
          }),
        },
      },
      {
        description:
          'single specs component on init action actions list$ throws error',
        expectation: 'should return single error action actions',
        actionsMarbles: 'a',
        actionsValues: { a: PackageActions.specsComponentOnInit() },
        specsServiceListReturnValues: [{ marbles: '-#|' }],
        expectedMarbles: '-b',
        expectedValues: {
          b: PackageActions.packageApiListSpecsError(),
        },
      },
      {
        description:
          'multiple specs component on init action actions list$ returns spec infos before next',
        expectation: 'should return multiple success action actions',
        actionsMarbles: 'a--d',
        actionsValues: {
          a: PackageActions.specsComponentOnInit(),
          d: PackageActions.specsComponentOnInit(),
        },
        specsServiceListReturnValues: [
          { marbles: '-b|', values: { b: SPEC_INFOS_1 } },
          { marbles: '-e|', values: { e: SPEC_INFOS_2 } },
        ],
        expectedMarbles: '-b--e',
        expectedValues: {
          b: PackageActions.packageApiListSpecsSuccess({
            specInfos: SPEC_INFOS_1,
          }),
          e: PackageActions.packageApiListSpecsSuccess({
            specInfos: SPEC_INFOS_2,
          }),
        },
      },
      {
        description:
          'multiple specs component on init action actions list$ returns spec infos after next',
        expectation: 'should return single success actions',
        actionsMarbles: 'a--d',
        actionsValues: {
          a: PackageActions.specsComponentOnInit(),
          d: PackageActions.specsComponentOnInit(),
        },
        specsServiceListReturnValues: [
          { marbles: '----e|', values: { e: SPEC_INFOS_1 } },
          { marbles: '-e|', values: { e: SPEC_INFOS_2 } },
        ],
        expectedMarbles: '----e',
        expectedValues: {
          b: PackageActions.packageApiListSpecsSuccess({
            specInfos: SPEC_INFOS_1,
          }),
          e: PackageActions.packageApiListSpecsSuccess({
            specInfos: SPEC_INFOS_2,
          }),
        },
      },
    ] as {
      description: string;
      expectation: string;
      actionsMarbles: string;
      actionsValues: { [key: string]: Action };
      specsServiceListReturnValues: {
        marbles: string;
        values: { [key: string]: SpecInfo[] };
      }[];
      expectedMarbles: string;
      expectedValues: { [key: string]: Action };
    }[]).forEach(
      ({
        description,
        expectation,
        actionsMarbles,
        actionsValues,
        specsServiceListReturnValues,
        expectedMarbles,
        expectedValues,
      }) => {
        describe(description, () => {
          it(expectation, () => {
            testScheduler.run((helpers) => {
              // GIVEN actions
              actions$ = helpers.cold(actionsMarbles, actionsValues);
              // AND SpecsService list that returns values
              specsServiceSpy.list$.and.returnValues(
                ...specsServiceListReturnValues.map(({ marbles, values }) =>
                  helpers.cold(marbles, values)
                )
              );

              // WHEN listSpecs$ is called
              effects = new PackageEffects(
                actions$,
                oAuthServiceSpy,
                specsServiceSpy,
                specServiceSpy
              );
              const returnedActions = effects.listSpecs$;

              // THEN the expected actions are returned
              helpers
                .expectObservable(returnedActions)
                .toBe(expectedMarbles, expectedValues);
            });

            // AND specsService list$ has been called
            expect(specsServiceSpy.list$).toHaveBeenCalledTimes(
              specsServiceListReturnValues.length
            );
            if (specsServiceListReturnValues.length > 0) {
              expect(specsServiceSpy.list$).toHaveBeenCalledWith({
                accessToken,
              });
            }
          });
        });
      }
    );
  });

  describe('deleteSpecsSpecId$', () => {
    ([
      {
        description: 'empty actions',
        expectation: 'should return empty actions',
        actionsMarbles: '',
        actionsValues: {},
        specsServiceListReturnValues: [],
        expectedMarbles: '',
        expectedValues: {},
        expectedCalls: [],
      },
      {
        description: 'different action actions',
        expectation: 'should return empty actions',
        actionsMarbles: 'a',
        actionsValues: { a: PackageActions.packageApiListSpecsError() },
        specsServiceListReturnValues: [],
        expectedMarbles: '',
        expectedValues: {},
        expectedCalls: [],
      },
      {
        description:
          'single specs component delete specs spec id action actions delete$ succeeds',
        expectation: 'should return single success action actions',
        actionsMarbles: 'a',
        actionsValues: {
          a: PackageActions.specsComponentDeleteSpecId({ specId: 'spec id 1' }),
        },
        specsServiceListReturnValues: [
          { marbles: '-b|', values: { b: undefined } },
        ],
        expectedMarbles: '-b',
        expectedValues: {
          b: PackageActions.packageApiDeleteSpecsSpecIdSuccess(),
        },
        expectedCalls: [{ accessToken, id: 'spec id 1' }],
      },
      {
        description:
          'single specs component on init action actions delete$ throws error',
        expectation: 'should return single error action actions',
        actionsMarbles: 'a',
        actionsValues: {
          a: PackageActions.specsComponentDeleteSpecId({ specId: 'spec id 1' }),
        },
        specsServiceListReturnValues: [{ marbles: '-#|' }],
        expectedMarbles: '-b',
        expectedValues: {
          b: PackageActions.packageApiDeleteSpecsSpecIdError(),
        },
        expectedCalls: [{ accessToken, id: 'spec id 1' }],
      },
      {
        description:
          'multiple specs component on init action actions delete$ returns before next',
        expectation: 'should return multiple success action actions',
        actionsMarbles: 'a--d',
        actionsValues: {
          a: PackageActions.specsComponentDeleteSpecId({ specId: 'spec id 1' }),
          d: PackageActions.specsComponentDeleteSpecId({ specId: 'spec id 2' }),
        },
        specsServiceListReturnValues: [
          { marbles: '-b|', values: { b: undefined } },
          { marbles: '-e|', values: { e: undefined } },
        ],
        expectedMarbles: '-b--e',
        expectedValues: {
          b: PackageActions.packageApiDeleteSpecsSpecIdSuccess(),
          e: PackageActions.packageApiDeleteSpecsSpecIdSuccess(),
        },
        expectedCalls: [
          { accessToken, id: 'spec id 1' },
          { accessToken, id: 'spec id 2' },
        ],
      },
      {
        description:
          'multiple specs component on init action actions delete$ returns after next',
        expectation: 'should return single success actions',
        actionsMarbles: 'a--d',
        actionsValues: {
          a: PackageActions.specsComponentDeleteSpecId({ specId: 'spec id 1' }),
          d: PackageActions.specsComponentDeleteSpecId({ specId: 'spec id 2' }),
        },
        specsServiceListReturnValues: [
          { marbles: '-----f|', values: { f: undefined } },
          { marbles: '-e|', values: { e: undefined } },
        ],
        expectedMarbles: '----ef',
        expectedValues: {
          e: PackageActions.packageApiDeleteSpecsSpecIdSuccess(),
          f: PackageActions.packageApiDeleteSpecsSpecIdSuccess(),
        },
        expectedCalls: [
          { accessToken, id: 'spec id 1' },
          { accessToken, id: 'spec id 2' },
        ],
      },
    ] as {
      description: string;
      expectation: string;
      actionsMarbles: string;
      actionsValues: { [key: string]: Action };
      specsServiceListReturnValues: {
        marbles: string;
        values: { [key: string]: undefined };
      }[];
      expectedMarbles: string;
      expectedValues: { [key: string]: Action };
      expectedCalls: { accessToken: string; id: string }[];
    }[]).forEach(
      ({
        description,
        expectation,
        actionsMarbles,
        actionsValues,
        specsServiceListReturnValues,
        expectedMarbles,
        expectedValues,
        expectedCalls,
      }) => {
        describe(description, () => {
          it(expectation, () => {
            testScheduler.run((helpers) => {
              // GIVEN actions
              actions$ = helpers.cold(actionsMarbles, actionsValues);
              // AND SpecsService delete that returns values
              specServiceSpy.delete$.and.returnValues(
                ...specsServiceListReturnValues.map(({ marbles, values }) =>
                  helpers.cold(marbles, values)
                )
              );

              // WHEN deleteSpecsSpecId$ is called
              effects = new PackageEffects(
                actions$,
                oAuthServiceSpy,
                specsServiceSpy,
                specServiceSpy
              );
              const returnedActions = effects.deleteSpecsSpecId$;

              // THEN the expected actions are returned
              helpers
                .expectObservable(returnedActions)
                .toBe(expectedMarbles, expectedValues);
            });

            // AND specsService delete$ has been called
            expect(specServiceSpy.delete$).toHaveBeenCalledTimes(
              expectedCalls.length
            );
            expectedCalls.forEach((expectedCall) =>
              expect(specServiceSpy.delete$).toHaveBeenCalledWith(expectedCall)
            );
          });
        });
      }
    );
  });
});
