class BaseError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'BaseError';
  }
}

export class SpecsError extends BaseError {
  constructor(message: string) {
    super(message);
    this.name = 'SpecsError';
  }
}

export class SpecError extends BaseError {
  constructor(message: string) {
    super(message);
    this.name = 'SpecError';
  }
}
