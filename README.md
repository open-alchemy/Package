# OpenAlchemy Package

Offers OpenAlchemy models packages to be installed via pip. For example:

<!-- markdownlint-disable line-length -->

```bash
pip install --index-url https://{public_key}:{secret_key}@index.package.openalchemy.io --extra-index-url https://pypi.org/simple "{specId}=={version}"
```

<!-- markdownlint-enable line-length -->

The web application at <https://package.openalchemy.io> provides a web
interface to manage your packages, including providing the `pip install`
command for your own package.

This service is based on the OpenAlchemy package you can find out more about
here: <https://github.com/jdkandersson/OpenAlchemy>

---

## NOTE

This service has been engineered with a lot of care (which you can verify
yourself as all the code, infrastructure and tests are open source in this
repository). However, a lot of bugs are discovered by operating software over
time. This service was first made available in January 2020.

---

## Pricing

A free tier is available which covers up to 10 models across any number of
packages. No credit card is required to use the free tier.

Whilst a paid version of the service is not yet available, for transparency,
the following is the proposed pricing for the service: $0.1 per model above the
free tier per month (pro rata) charged monthly.

## Terms of Service

The Australian company Open Alchemy Pty Ltd owns and operates this service.

By using this service, you agree to the terms available here:
[TERMS.md](TERMS.md).

## Web

Front end for the service. Defined here: [./web](./web).

## API

Serves requests for the front end. Defined here: [./api](./api).

## SDK

Wraps the API to make it easier to consume in the front end. Defined here:
[./sdk](./sdk).

## Database

Personalizes API responses vy exposing an interface to the database as well as
fixtures for testing. Defined here: [./database](./database).

## Security

Facade for security operations, such as generating public and private keys.
Exposes fixtures for testing. Defined here: [./security](./security).

## Build

When a new spec is uploaded, builds a package from th spec and uploads it to
the storage. Defined here: [./build](./build).

## Index

Implements the packaging index to enable pip installing the model packages.
Defined here: [./index](./index).

## Infrastructure

Shared CloudFormation stacks for application components. Defined here:
[./infrastructure](./infrastructure).

## Test

Execute tests against production for application components. Defined here:
[./test](./test).
