import {
  SpecsService,
  SpecService,
  CredentialsService,
  SpecError,
} from '@open-alchemy/package-sdk';

import { getAccessToken } from './helper';

const VERSION = '1';
const TITLE = 'title 1';
const DESCRIPTION = 'description 1';
const SPEC_VALUE = {
  info: {
    title: TITLE,
    description: DESCRIPTION,
    version: VERSION,
  },
  components: {
    schemas: {
      Schema: {
        type: 'object',
        'x-tablename': 'schema',
        properties: { id: { type: 'integer' } },
      },
    },
  },
};
const SPEC_VALUE_STRING = JSON.stringify(SPEC_VALUE);

describe('create spec', () => {
  let accessToken: string;
  const specName = 'sdkSpec1';
  let specsService: SpecsService;
  let specService: SpecService;

  beforeAll(async () => {
    accessToken = await getAccessToken();
  });

  beforeEach(() => {
    specsService = new SpecsService();
    specService = new SpecService();
  });

  afterEach(async () => {
    await specService.delete({ accessToken, name: specName });
  });

  [
    {
      description: 'without version',
      expectation: 'should create, retrieve and delete the spec as requested',
      paramsBase: { name: specName },
    },
    {
      description: 'with version',
      expectation: 'should create, retrieve and delete the spec as requested',
      paramsBase: { name: specName, version: VERSION },
    },
  ].forEach(({ description, expectation, paramsBase }) => {
    describe(description, () => {
      test(expectation, async () => {
        // Check that the specs are empty
        await expect(specsService.list({ accessToken })).resolves.toEqual([]);

        // Try to create invalid spec
        await expect(
          specService.put({
            ...paramsBase,
            accessToken,
            value: 'invalid',
            language: 'JSON',
          })
        ).rejects.toBeInstanceOf(SpecError);

        // Create valid spec
        await expect(
          specService.put({
            ...paramsBase,
            accessToken,
            value: SPEC_VALUE_STRING,
            language: 'JSON',
          })
        ).resolves.toEqual(undefined);

        // Check that the spec is now listed
        const returnedSpecInfos = await specsService.list({ accessToken });
        expect(returnedSpecInfos.length).toEqual(1);
        const returnedSpecInfo = returnedSpecInfos[0];
        expect(returnedSpecInfo.name).toEqual(specName);
        expect(returnedSpecInfo.id).toEqual(specName.toLowerCase());
        expect(returnedSpecInfo.version).toEqual(VERSION);
        expect(returnedSpecInfo.title).toEqual(TITLE);
        expect(returnedSpecInfo.description).toEqual(DESCRIPTION);
        expect(returnedSpecInfo.model_count).toEqual(1);
        expect(returnedSpecInfo.updated_at).toBeDefined();

        // Check that the spec can be retrieved
        const returnedSpecValue = await specService.get({
          ...paramsBase,
          accessToken,
        });
        expect(returnedSpecValue).toContain(VERSION);
        expect(returnedSpecValue).toContain(TITLE);
        expect(returnedSpecValue).toContain(DESCRIPTION);
        expect(returnedSpecValue).toContain('Schema:');
        expect(returnedSpecValue).toContain('x-tablename:');
        expect(returnedSpecValue).toContain(': schema');

        // Delete the spec
        await specService.delete({ name: specName, accessToken });

        // Check that the spec can no longer be retrieved
        await expect(
          specService.get({ name: specName, accessToken })
        ).rejects.toBeInstanceOf(SpecError);

        // Check that the specs are empty
        await expect(specsService.list({ accessToken })).resolves.toEqual([]);
      });
    });
  });
});

describe('get delete credentials', () => {
  let accessToken: string;
  let credentialsService: CredentialsService;

  beforeAll(async () => {
    accessToken = await getAccessToken();
  });

  beforeEach(() => {
    credentialsService = new CredentialsService();
  });

  afterEach(async () => {
    await credentialsService.delete({ accessToken });
  });

  describe('get delete get', () => {
    it('should retrieve the credentials, delete and the retrieve different credentials', async () => {
      // Retrieve credentials
      const firstCredentials = await credentialsService.get({ accessToken });
      expect(firstCredentials.public_key).toBeTruthy();
      expect(firstCredentials.secret_key).toBeTruthy();

      // Delete credentials
      await credentialsService.delete({ accessToken });

      // Retrieve credentials again, should be different now
      const secondCredentials = await credentialsService.get({ accessToken });
      expect(secondCredentials.public_key).not.toEqual(
        firstCredentials.public_key
      );
      expect(secondCredentials.secret_key).not.toEqual(
        firstCredentials.secret_key
      );
    });
  });
});
