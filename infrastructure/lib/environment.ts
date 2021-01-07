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

  private getValue(value: string | null, envKey: string): string {
    if (value === null) {
      const envValue = process.env[envKey];
      assert.ok(
        typeof envValue === 'string',
        `${STACK_KEY} missing or not a string`
      );
      value = envValue;
    }
    return value;
  }

  get stack(): IStack {
    this._stack = this.getValue(this._stack, STACK_KEY);
    return this._stack;
  }

  get awsAccount(): IAwsAccount {
    this._awsAccount = this.getValue(this._awsAccount, AWS_ACCOUNT_KEY);
    return this._awsAccount;
  }

  get awsDefaultRegion(): IAwsDefaultRegion {
    this._awsDefaultRegion = this.getValue(
      this._awsDefaultRegion,
      AWS_DEFAULT_REGION_KEY
    );
    return this._awsDefaultRegion;
  }

  get awsOpenAlchemyCertificateArn(): IAwsOpenAlchemyCertificateArn {
    this._awsOpenAlchemyCertificateArn = this.getValue(
      this._awsOpenAlchemyCertificateArn,
      AWS_OPEN_ALCHEMY_CERTIFICATE_ARN_KEY
    );
    return this._awsOpenAlchemyCertificateArn;
  }

  get awsIdentityProviderArn(): IAwsIdentityProviderArn {
    this._awsIdentityProviderArn = this.getValue(
      this._awsIdentityProviderArn,
      AWS_IDENTITY_PROVIDER_ARN_KEY
    );
    return this._awsIdentityProviderArn;
  }

  get alarmEmailAddress(): IAlarmEmailAddress {
    this._alarmEmailAddress = this.getValue(
      this._alarmEmailAddress,
      ALARM_EMAIL_ADDRESS_KEY
    );
    return this._alarmEmailAddress;
  }
}

export const ENVIRONMENT = new Environment();
