import * as assert from 'assert';

const STACK_KEY = 'STACK';
const AWS_ACCOUNT_KEY = 'AWS_ACCOUNT';
const AWS_DEFAULT_REGION_KEY = 'AWS_DEFAULT_REGION';
const AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY = 'AWS_OPEN_ALCHEMY_CERTIFICATE_ARN';
const AWS_IDENTITY_PROVIDER_ARN_KEY = 'AWS_IDENTITY_PROVIDER_ARN';

interface IEnvironment {
  [STACK_KEY]: string;
  [AWS_ACCOUNT_KEY]: string;
  [AWS_DEFAULT_REGION_KEY]: string;
  [AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY]: string;
  [AWS_IDENTITY_PROVIDER_ARN_KEY]: string;
}

function getEnvironment(): IEnvironment {
  const stack = process.env[STACK_KEY];
  assert.ok(typeof stack === 'string', `${STACK_KEY} missing or not a string`);

  const awsAccount = process.env[AWS_ACCOUNT_KEY];
  assert.ok(
    typeof awsAccount === 'string',
    `${AWS_ACCOUNT_KEY} missing or not a string`
  );

  const awsDefaultRegion = process.env[AWS_DEFAULT_REGION_KEY];
  assert.ok(
    typeof awsDefaultRegion === 'string',
    `${AWS_DEFAULT_REGION_KEY} missing or not a string`
  );

  const awsOpenAlchemyCertificateArn =
    process.env[AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY];
  assert.ok(
    typeof awsOpenAlchemyCertificateArn === 'string',
    `${AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY} missing or not a string`
  );

  const awsIdentityProviderArn = process.env[AWS_IDENTITY_PROVIDER_ARN_KEY];
  assert.ok(
    typeof awsIdentityProviderArn === 'string',
    `${AWS_IDENTITY_PROVIDER_ARN_KEY} missing or not a string`
  );

  return {
    [STACK_KEY]: stack,
    [AWS_ACCOUNT_KEY]: awsAccount,
    [AWS_DEFAULT_REGION_KEY]: awsDefaultRegion,
    [AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY]: awsOpenAlchemyCertificateArn,
    [AWS_IDENTITY_PROVIDER_ARN_KEY]: awsIdentityProviderArn,
  };
}

export const ENVIRONMENT = getEnvironment();
