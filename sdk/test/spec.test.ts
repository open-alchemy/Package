import axios from 'axios';
import MockAdaptor from 'axios-mock-adapter';

import { get, put, delete_, getVersions } from '../src/spec';
import { SpecError } from '../src/errors';

describe('spec', () => {
  let mockAdaptor: MockAdaptor;

  beforeEach(() => {
    mockAdaptor = new MockAdaptor(axios);
  });

  describe('get', () => {
    test('should return spec value when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const responseData = 'spec 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN get is called
      const returnedSpecPromise = get({ accessToken, id: specId });

      // THEN the spec value is returned
      expect(returnedSpecPromise).resolves.toEqual(responseData);
    });

    test('should return the spec value for a version when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const responseData = 'spec 1';
      const version = 'version 1';
      mockAdaptor
        .onGet(
          `https://package.api.openalchemy.io/v1/specs/${specId}/versions/${version}`
        )
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN get is called
      const returnedSpecPromise = get({ accessToken, id: specId, version });

      // THEN the spec value is returned
      expect(returnedSpecPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const message = 'message 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(400, btoa(message));

      // WHEN get is called
      const returnedSpecPromise = get({ accessToken, id: specId });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst loading the spec: ${message}`
      );
      expect(returnedSpecPromise).rejects.toEqual(expectedError);
    });
  });

  describe('getVersions', () => {
    test('should return specs when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const responseData = [{ key: 'value' }];
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specId}/versions`)
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN getVersions is called
      const returnedSpecPromise = getVersions({ accessToken, id: specId });

      // THEN the spec versions are returned
      expect(returnedSpecPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const message = 'message 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specId}/versions`)
        .replyOnce(400, btoa(message));

      // WHEN getVersions is called
      const returnedSpecPromise = getVersions({ accessToken, id: specId });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst loading the versions for the spec: ${message}`
      );
      expect(returnedSpecPromise).rejects.toEqual(expectedError);
    });
  });

  describe('put', () => {
    test('should create or update spec when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const specValue = 'spec value 1';
      mockAdaptor
        .onPut(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [204];
        });

      // WHEN put is called
      const returnedSpecPromise = put({
        accessToken,
        id: specId,
        value: specValue,
      });

      // THEN the promise resolves
      expect(returnedSpecPromise).resolves.toEqual(undefined);
    });

    test('should create or update specific version of a spec spec when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const specVersion = 'version 1';
      const specValue = 'spec value 1';
      mockAdaptor
        .onPut(
          `https://package.api.openalchemy.io/v1/specs/${specId}/versions/${specVersion}`
        )
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [204];
        });

      // WHEN put is called
      const returnedSpecPromise = put({
        accessToken,
        id: specId,
        value: specValue,
        version: specVersion,
      });

      // THEN the promise resolves
      expect(returnedSpecPromise).resolves.toEqual(undefined);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const specValue = 'spec value 1';
      const message = 'message 1';
      mockAdaptor
        .onPut(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(400, btoa(message));

      // WHEN put is called
      const returnedSpecPromise = put({
        accessToken,
        id: specId,
        value: specValue,
      });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst creating or updating the spec: ${message}`
      );
      expect(returnedSpecPromise).rejects.toEqual(expectedError);
    });
  });

  describe('delete', () => {
    test('should return specs when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      mockAdaptor
        .onDelete(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(config => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [204];
        });

      // WHEN delete is called
      const returnedSpecPromise = delete_({ accessToken, id: specId });

      // THEN the promise resolves
      expect(returnedSpecPromise).resolves.toEqual(undefined);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const specId = 'spec id 1';
      const message = 'message 1';
      mockAdaptor
        .onDelete(`https://package.api.openalchemy.io/v1/specs/${specId}`)
        .replyOnce(400, btoa(message));

      // WHEN delete is called
      const returnedSpecPromise = delete_({ accessToken, id: specId });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst deleting the spec: ${message}`
      );
      expect(returnedSpecPromise).rejects.toEqual(expectedError);
    });
  });
});
