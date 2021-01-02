import assert from 'assert';

import AWS from 'aws-sdk';
import {
  SpecsService,
  SpecService,
  SpecError,
} from '@open-alchemy/package-sdk';

const VERSION = 'version 1';
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
  const specId = 'sdk spec id 1';
  let specsService: SpecsService;
  let specService: SpecService;

  beforeAll(async () => {
    const awsRegion = process.env['AWS_DEFAULT_REGION'] || null;
    assert.ok(
      typeof awsRegion === 'string',
      'AWS_DEFAULT_REGION environment variable not defined'
    );

    const userPoolId = process.env['USER_POOL_ID'] || null;
    assert.ok(
      typeof userPoolId === 'string',
      'USER_POOL_ID environment variable not defined'
    );

    const clientId = process.env['CLIENT_ID'] || null;
    assert.ok(
      typeof clientId === 'string',
      'CLIENT_ID environment variable not defined'
    );

    const testUsername = process.env['TEST_USERNAME'] || null;
    assert.ok(
      typeof testUsername === 'string',
      'TEST_USERNAME environment variable not defined'
    );

    const testPassword = process.env['TEST_PASSWORD'] || null;
    assert.ok(
      typeof testPassword === 'string',
      'TEST_PASSWORD environment variable not defined'
    );

    const authFlow = 'ADMIN_USER_PASSWORD_AUTH';

    const cognitoIdentityServiceProvider = new AWS.CognitoIdentityServiceProvider(
      { region: awsRegion }
    );
    const response = await cognitoIdentityServiceProvider
      .adminInitiateAuth({
        AuthFlow: authFlow,
        ClientId: clientId,
        UserPoolId: userPoolId,
        AuthParameters: { USERNAME: testUsername, PASSWORD: testPassword },
      })
      .promise();
    assert.ok(response.AuthenticationResult !== undefined);
    assert.ok(response.AuthenticationResult.AccessToken !== undefined);
    accessToken = response.AuthenticationResult?.AccessToken;
  });

  beforeEach(() => {
    specsService = new SpecsService();
    specService = new SpecService();
  });

  afterEach(async () => {
    await specService.delete({ accessToken, id: specId });
  });

  [
    {
      description: 'without version',
      expectation: 'should create, retrieve and delete the spec as requested',
      paramsBase: { id: specId },
    },
    {
      description: 'with version',
      expectation: 'should create, retrieve and delete the spec as requested',
      paramsBase: { id: specId, version: VERSION },
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
        expect(returnedSpecInfo.id).toEqual(specId);
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
        await specService.delete({ id: specId, accessToken });

        // Check that the spec can no longer be retrieved
        await expect(
          specService.get({ id: specId, accessToken })
        ).rejects.toBeInstanceOf(SpecError);

        // Check that the specs are empty
        await expect(specsService.list({ accessToken })).resolves.toEqual([]);
      });
    });
  });
});
