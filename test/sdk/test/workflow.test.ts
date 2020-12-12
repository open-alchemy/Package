import assert from 'assert';

import AWS from 'aws-sdk';
import { specs, spec, errors } from '@open-alchemy/package-sdk';

describe('create spec', () => {
  let accessToken: string;
  const specId = 'sdk spec id 1';

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

  afterEach(async () => {
    await spec.delete_({ accessToken, id: specId });
  });

  test('should create the spec as requested', async () => {
    // Check that the specs are empty
    await expect(specs.list({ accessToken })).resolves.toEqual([]);

    // Try to create invalid spec
    await spec.put({
      accessToken,
      id: specId,
      value: 'invalid',
      language: 'JSON',
    });
    await expect(
      spec.put({ accessToken, id: specId, value: 'invalid', language: 'JSON' })
    ).rejects.toEqual(errors.SpecError);

    // Create valid spec
    const title = 'title 1';
    const description = 'title 1';
    const version = 'version 1';
    const specValue = {
      info: {
        title: title,
        description: description,
        version: version,
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
    expect(
      spec.put({
        accessToken,
        id: specId,
        value: JSON.stringify(specValue),
        language: 'JSON',
      })
    ).resolves.toEqual(undefined);
  });
});
