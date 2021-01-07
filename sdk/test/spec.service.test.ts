import axios from 'axios';
import MockAdaptor from 'axios-mock-adapter';

import { SpecService } from '../src/spec.service';
import { SpecError } from '../src/errors';

describe('SpecService', () => {
  let mockAdaptor: MockAdaptor;
  let service: SpecService;

  beforeEach(() => {
    mockAdaptor = new MockAdaptor(axios);
    service = new SpecService();
  });

  describe('get', () => {
    test('should return spec value when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const responseData = 'spec 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN get is called
      const returnedPromise = service.get({ accessToken, name: specName });

      // THEN the spec value is returned
      await expect(returnedPromise).resolves.toEqual(responseData);
    });

    test('should return spec value when 200 is returned using the observable method', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const responseData = 'spec 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce(200, responseData);

      // WHEN get is called
      const returnedPromise = service
        .get$({ accessToken, name: specName })
        .toPromise();

      // THEN the spec value is returned
      await expect(returnedPromise).resolves.toEqual(responseData);
    });

    test('should return the spec value for a version when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const responseData = 'spec 1';
      const version = 'version 1';
      mockAdaptor
        .onGet(
          `https://package.api.openalchemy.io/v1/specs/${specName}/versions/${version}`
        )
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN get is called
      const returnedPromise = service.get({
        accessToken,
        name: specName,
        version,
      });

      // THEN the spec value is returned
      await expect(returnedPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const message = 'message 1';
      mockAdaptor
        .onGet(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce(400, btoa(message));

      // WHEN get is called
      const returnedPromise = service.get({ accessToken, name: specName });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst loading the spec: ${message}`
      );
      await expect(returnedPromise).rejects.toEqual(expectedError);
    });
  });

  describe('getVersions', () => {
    test('should return specs when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const responseData = [{ key: 'value' }];
      mockAdaptor
        .onGet(
          `https://package.api.openalchemy.io/v1/specs/${specName}/versions`
        )
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [200, responseData];
        });

      // WHEN getVersions is called
      const returnedPromise = service.getVersions({
        accessToken,
        name: specName,
      });

      // THEN the spec versions are returned
      await expect(returnedPromise).resolves.toEqual(responseData);
    });

    test('should return specs when 200 is returned using observables', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const responseData = [{ key: 'value' }];
      mockAdaptor
        .onGet(
          `https://package.api.openalchemy.io/v1/specs/${specName}/versions`
        )
        .replyOnce(200, responseData);

      // WHEN getVersions is called
      const returnedPromise = service
        .getVersions$({
          accessToken,
          name: specName,
        })
        .toPromise();

      // THEN the spec versions are returned
      await expect(returnedPromise).resolves.toEqual(responseData);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const message = 'message 1';
      mockAdaptor
        .onGet(
          `https://package.api.openalchemy.io/v1/specs/${specName}/versions`
        )
        .replyOnce(400, btoa(message));

      // WHEN getVersions is called
      const returnedPromise = service.getVersions({
        accessToken,
        name: specName,
      });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst loading the versions for the spec: ${message}`
      );
      await expect(returnedPromise).rejects.toEqual(expectedError);
    });
  });

  describe('put', () => {
    test('should create or update spec when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const specValue = 'spec value 1';
      const language = 'JSON';
      mockAdaptor
        .onPut(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );
          expect(config.headers).toHaveProperty('Content-Type');
          expect(config.headers['Content-Type']).toEqual('text/plain');
          expect(config.headers).toHaveProperty('X-LANGUAGE');
          expect(config.headers['X-LANGUAGE']).toEqual(language);

          return [204];
        });

      // WHEN put is called
      const returnedPromise = service.put({
        accessToken,
        name: specName,
        value: specValue,
        language,
      });

      // THEN the promise resolves
      await expect(returnedPromise).resolves.toEqual(undefined);
    });

    test('should create or update spec when 200 is returned using observable', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const specValue = 'spec value 1';
      const language = 'JSON';
      mockAdaptor
        .onPut(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce(204);

      // WHEN put is called
      const returnedPromise = service
        .put$({
          accessToken,
          name: specName,
          value: specValue,
          language,
        })
        .toPromise();

      // THEN the promise resolves
      await expect(returnedPromise).resolves.toEqual(undefined);
    });

    test('should create or update specific version of a spec spec when 200 is returned', async () => {
      // GIVE mocked axios that returns 200
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const specVersion = 'version 1';
      const specValue = 'spec value 1';
      const language = 'JSON';
      mockAdaptor
        .onPut(
          `https://package.api.openalchemy.io/v1/specs/${specName}/versions/${specVersion}`
        )
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );
          expect(config.headers).toHaveProperty('Content-Type');
          expect(config.headers['Content-Type']).toEqual('text/plain');
          expect(config.headers).toHaveProperty('X-LANGUAGE');
          expect(config.headers['X-LANGUAGE']).toEqual(language);

          return [204];
        });

      // WHEN put is called
      const returnedPromise = service.put({
        accessToken,
        name: specName,
        value: specValue,
        version: specVersion,
        language,
      });

      // THEN the promise resolves
      await expect(returnedPromise).resolves.toEqual(undefined);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const specValue = 'spec value 1';
      const message = 'message 1';
      const language = 'JSON';
      mockAdaptor
        .onPut(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce(400, btoa(message));

      // WHEN put is called
      const returnedPromise = service.put({
        accessToken,
        name: specName,
        value: specValue,
        language,
      });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst creating or updating the spec: ${message}`
      );
      await expect(returnedPromise).rejects.toEqual(expectedError);
    });
  });

  describe('delete', () => {
    test('should return when 204 is returned', async () => {
      // GIVE mocked axios that returns 204
      const accessToken = 'token 1';
      const specName = 'spec 1';
      mockAdaptor
        .onDelete(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce((config) => {
          expect(config.headers).toHaveProperty('Authorization');
          expect(config.headers['Authorization']).toEqual(
            `Bearer ${accessToken}`
          );

          return [204];
        });

      // WHEN delete is called
      const returnedPromise = service.delete({ accessToken, name: specName });

      // THEN the promise resolves
      await expect(returnedPromise).resolves.toEqual(undefined);
    });

    test('should return when 204 is returned', async () => {
      // GIVE mocked axios that returns 204
      const accessToken = 'token 1';
      const specName = 'spec 1';
      mockAdaptor
        .onDelete(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce(204);

      // WHEN delete is called
      const returnedPromise = service
        .delete$({ accessToken, name: specName })
        .toPromise();

      // THEN the promise resolves
      await expect(returnedPromise).resolves.toEqual(undefined);
    });

    test('should throw error if a 400 error is returned', async () => {
      // GIVE mocked axios that returns 400
      const accessToken = 'token 1';
      const specName = 'spec 1';
      const message = 'message 1';
      mockAdaptor
        .onDelete(`https://package.api.openalchemy.io/v1/specs/${specName}`)
        .replyOnce(400, btoa(message));

      // WHEN delete is called
      const returnedPromise = service.delete({ accessToken, name: specName });

      // THEN the expected error is thrown
      const expectedError = new SpecError(
        `error whilst deleting the spec: ${message}`
      );
      await expect(returnedPromise).rejects.toEqual(expectedError);
    });
  });
});
