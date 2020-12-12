import { isNotNullUndefined } from './filters';

describe('isNotNullUndefined', () => {
  [
    {
      description: 'undefined',
      expectation: 'it should return false',
      value: undefined,
      expectedResult: false,
    },
    {
      description: 'null',
      expectation: 'it should return false',
      value: null,
      expectedResult: false,
    },
    {
      description: 'defined',
      expectation: 'it should return true',
      value: '',
      expectedResult: true,
    },
  ].forEach(({ description, expectation, value, expectedResult }) => {
    describe(description, () => {
      it(expectation, () => {
        // GIVEN value

        // WHEN isNotNullUndefined is called with the value
        const returnedResult = isNotNullUndefined(value);

        expect(returnedResult).toEqual(expectedResult);
      });
    });
  });
});
