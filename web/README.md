# Package

Web interface to manage OpenAlchemy packages. It is available here:
[https://package.openalchemy.io](https://package.openalchemy.io)

## Infrastructure

The CloudFormation stack is defined here:
[../infrastructure/lib/web-stack.ts](../infrastructure/lib/web-stack.ts).

## CI-CD

The workflow for the CI-CD is defined here:
[../.github/workflows/ci-cd-web.yaml](../.github/workflows/ci-cd-web.yaml).

## Production Tests

The tests against the deployed web application are defined here:
[../test/web/](../test/web/).

The workflow that periodically executes the tests is defined here:
[../.github/workflows/production-test-web.yaml](../.github/workflows/production-test-web.yaml).
