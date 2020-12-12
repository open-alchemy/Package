import { decodeResponse } from '../src/helpers';

describe('decodeResponse', () => {
  [
    {
      description: 'base64',
      expectation: 'should return the decoded string',
      value: btoa('value 1'),
      expectedValue: 'value 1',
    },
    {
      description: 'not base64',
      expectation: 'should return the string',
      value: 'value{} 1',
      expectedValue: '"value{} 1"',
    },
  ].forEach(({ description, expectation, value, expectedValue }) => {
    describe(description, () => {
      test(expectation, () => {
        expect(decodeResponse(value)).toEqual(expectedValue);
      });
    });
  });
});
