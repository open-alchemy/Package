// import { Observable } from 'rxjs';
// import { TestScheduler } from 'rxjs/testing';

// import { Action } from '@ngrx/store';
// import { OAuthService } from 'angular-oauth2-oidc';
// import { SpecsService, SpecInfo } from '@open-alchemy/package-sdk';

// import { PackageEffects } from './package.effects';
// import * as PackageActions from './package.actions';

// const testScheduler = new TestScheduler((actual, expected) => {
//   expect(actual).toEqual(expected);
// });

// const SPEC_INFOS: SpecInfo[] = [
//   {
//     spec_id: 'spec id 1',
//     version: 'version 1',
//     model_count: 1,
//   },
// ];

// describe('PackageEffects', () => {
//   let actions$: Observable<Action>;
//   let effects: PackageEffects;
//   let oAuthServiceSpy: jasmine.SpyObj<OAuthService>;
//   let specsServiceSpy: jasmine.SpyObj<SpecsService>;

//   const accessToken = 'token 1';

//   beforeEach(() => {
//     oAuthServiceSpy = jasmine.createSpyObj('OAuthService', ['getAccessToken']);
//     oAuthServiceSpy.getAccessToken.and.returnValue(accessToken);
//     specsServiceSpy = jasmine.createSpyObj('SpecsService', ['list']);
//   });

//   describe('listSpecs$', () => {
//     ([
//       {
//         description: 'empty actions',
//         expectation: 'should return empty actions',
//         actionsMarbles: '',
//         actionsValues: {},
//         specsServiceListReturnValues: [],
//         expectedMarbles: '',
//         expectedValues: {},
//       },
//       {
//         description: 'different action actions',
//         expectation: 'should return empty actions',
//         actionsMarbles: 'a',
//         actionsValues: { a: PackageActions.packageApiListSpecsError() },
//         specsServiceListReturnValues: [],
//         expectedMarbles: '',
//         expectedValues: {},
//       },
//       {
//         description: 'single specs component on init action actions',
//         expectation: 'should return empty actions',
//         actionsMarbles: 'a',
//         actionsValues: { a: PackageActions.specsComponentOnInit() },
//         specsServiceListReturnValues: [
//           { marbles: '-b', values: { b: SPEC_INFOS } },
//         ],
//         expectedMarbles: '-b',
//         expectedValues: { b: SPEC_INFOS },
//       },
//     ] as {
//       description: string;
//       expectation: string;
//       actionsMarbles: string;
//       actionsValues: { [key: string]: Action };
//       specsServiceListReturnValues: {
//         marbles: string;
//         values: { [key: string]: SpecInfo[] };
//       }[];
//       expectedMarbles: string;
//       expectedValues: { [key: string]: Action };
//     }[]).forEach(
//       ({
//         description,
//         expectation,
//         actionsMarbles,
//         actionsValues,
//         specsServiceListReturnValues,
//         expectedMarbles,
//         expectedValues,
//       }) => {
//         describe(description, () => {
//           it(expectation, () => {
//             testScheduler.run((helpers) => {
//               // GIVEN actions
//               actions$ = helpers.cold(actionsMarbles, actionsValues);
//               // AND SpecsService list that returns values
//               specsServiceSpy.list.and.returnValues(
//                 ...specsServiceListReturnValues.map(({ marbles, values }) =>
//                   helpers.cold(marbles, values).toPromise()
//                 )
//               );

//               // WHEN listSpecs$ is called
//               effects = new PackageEffects(
//                 actions$,
//                 oAuthServiceSpy,
//                 specsServiceSpy
//               );
//               const returnedActions = effects.listSpecs$;

//               // THEN the expected actions are returned
//               helpers
//                 .expectObservable(returnedActions)
//                 .toBe(expectedMarbles, expectedValues);
//             });
//           });
//         });
//       }
//     );
//   });
// });
