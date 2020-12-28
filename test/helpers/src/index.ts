import assert from 'assert';

import AWS from 'aws-sdk';

export async function getAccessToken(): Promise<string> {
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
  return response.AuthenticationResult?.AccessToken;
}
