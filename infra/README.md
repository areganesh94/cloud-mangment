# AWS infrastructure

This stack creates an ECR repository, an ECS Fargate cluster, task roles, and a
CloudWatch log group in `us-east-1` by default. The application service is
disabled by default because this repository does not yet include a production
container image or a database connection secret.

## GitHub setup

Use GitHub Actions OIDC, not long-lived AWS access keys. Configure an AWS
account OIDC provider for `token.actions.githubusercontent.com` and two IAM
roles:

- The plan role should trust this repository's `pull_request` subject and have
  read-only infrastructure permissions plus access to read and lock the
  Terraform state object.
- The apply role should trust only
  `repo:OWNER/REPOSITORY:ref:refs/heads/main` and have the permissions needed
  to manage this stack and its state.

Configure these GitHub Actions repository variables:

- `TF_STATE_BUCKET`: pre-created, versioned S3 bucket with public access blocked.
- `TF_PLAN_ROLE_ARN` and `TF_APPLY_ROLE_ARN`: the respective OIDC role ARNs.
- `AWS_REGION`: optional; defaults to `us-east-1`.

The workflow validates every pull request. Same-repository pull requests also
run a Terraform plan; fork pull requests do not receive AWS credentials. Merges
to `main` apply the configuration. The S3 bucket must exist before the first
workflow run because Terraform cannot create the backend that stores its own
state.

## Enabling the app service

First build and push a production-ready image to the ECR repository output by
Terraform. Then configure these additional GitHub Actions repository variables:

- `TF_DEPLOY_APP_SERVICE`: `true`.
- `TF_VPC_ID`: ID of the existing VPC.
- `TF_SUBNET_IDS`: JSON array of subnet IDs, for example
  `["subnet-0123456789abcdef0"]`.
- `TF_CONTAINER_IMAGE`: full ECR image URI with an immutable tag.
- `TF_DATABASE_URL_SECRET_ARN`: Secrets Manager ARN containing the
  `DATABASE_URL` value.
- `TF_ALLOWED_INGRESS_CIDRS`: JSON array of trusted CIDRs allowed to connect to
  port 5000; do not use `0.0.0.0/0` unless public access is intentional.

`TF_ASSIGN_PUBLIC_IP` defaults to `false`; use private subnets with outbound
NAT or another egress path in that configuration. Only set it to `true` when
the selected subnets have public routes and the ingress CIDRs are restricted.
`TF_DESIRED_COUNT` defaults to `1`.

The current Flask app still needs a production WSGI/container entry point before
its source can be built and run as an ECS service. Terraform does not create a
database; provide a compatible database URL through Secrets Manager.