import * as assert from 'assert';

const STACK_KEY = 'STACK';
const AWS_ACCOUNT_KEY = 'AWS_ACCOUNT';
const AWS_DEFAULT_REGION_KEY = 'AWS_DEFAULT_REGION';
const AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY = 'AWS_OPEN_ALCHEMY_CERTIFICATE_ARN';
const AWS_IDENTITY_PROVIDER_ARN_KEY = 'AWS_IDENTITY_PROVIDER_ARN';
const ALARM_EMAIL_ADDRESS_KEY = 'ALARM_EMAIL_ADDRESS';

type IStack = string;
type IAwsAccount = string;
type IAwsDefaultRegion = string;
type IAwsOpenAlchemyCertificateArn = string;
type IAwsIdentityProviderArn = string;
type IAlarmEmailAddress = string;

class Environment {
  private _stack: IStack | null = null;
  private _awsAccount: IAwsAccount | null = null;
  private _awsDefaultRegion: IAwsDefaultRegion | null = null;
  private _awsOpenAlchemyCertificateArn: IAwsOpenAlchemyCertificateArn | null = null;
  private _awsIdentityProviderArn: IAwsIdentityProviderArn | null = null;
  private _alarmEmailAddress: IAlarmEmailAddress | null = null;

  get stack(): IStack {
    if (this._stack === null) {
      const stack = process.env[STACK_KEY];
      assert.ok(
        typeof stack === 'string',
        `${STACK_KEY} missing or not a string`
      );
      this._stack = stack;
    }
    return this._stack;
  }

  get awsAccount(): IAwsAccount {
    if (this._awsAccount === null) {
      const awsAccount = process.env[AWS_ACCOUNT_KEY];
      assert.ok(
        typeof awsAccount === 'string',
        `${AWS_ACCOUNT_KEY} missing or not a string`
      );
      this._awsAccount = awsAccount;
    }
    return this._awsAccount;
  }

  get awsDefaultRegion(): IAwsDefaultRegion {
    if (this._awsDefaultRegion === null) {
      const awsDefaultRegion = process.env[AWS_DEFAULT_REGION_KEY];
      assert.ok(
        typeof awsDefaultRegion === 'string',
        `${AWS_DEFAULT_REGION_KEY} missing or not a string`
      );
      this._awsDefaultRegion = awsDefaultRegion;
    }
    return this._awsDefaultRegion;
  }

  get awsOpenAlchemyCertificateArn(): IAwsOpenAlchemyCertificateArn {
    if (this._awsOpenAlchemyCertificateArn === null) {
      const awsOpenAlchemyCertificateArn =
        process.env[AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY];
      assert.ok(
        typeof awsOpenAlchemyCertificateArn === 'string',
        `${AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY} missing or not a string`
      );
      this._awsOpenAlchemyCertificateArn = awsOpenAlchemyCertificateArn;
    }
    return this._awsOpenAlchemyCertificateArn;
  }

  get awsIdentityProviderArn(): IAwsIdentityProviderArn {
    if (this._awsIdentityProviderArn === null) {
      const awsIdentityProviderArn = process.env[AWS_IDENTITY_PROVIDER_ARN_KEY];
      assert.ok(
        typeof awsIdentityProviderArn === 'string',
        `${AWS_IDENTITY_PROVIDER_ARN_KEY} missing or not a string`
      );
      this._awsIdentityProviderArn = awsIdentityProviderArn;
    }
    return this._awsIdentityProviderArn;
  }

  get alarmEmailAddress(): IAlarmEmailAddress {
    if (this._alarmEmailAddress === null) {
      const alarmEmailAddress = process.env[ALARM_EMAIL_ADDRESS_KEY];
      assert.ok(
        typeof alarmEmailAddress === 'string',
        `${ALARM_EMAIL_ADDRESS_KEY} missing or not a string`
      );
      this._alarmEmailAddress = alarmEmailAddress;
    }
    return this._alarmEmailAddress;
  }
}

export const ENVIRONMENT = new Environment();
