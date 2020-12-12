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
