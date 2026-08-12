# deckwatch-plugin-aws

**Version:** 0.2.4 &nbsp;|&nbsp; **Author:** [alexconrey](https://github.com/alexconrey) &nbsp;|&nbsp; **Trust:** verified

A deckwatch plugin that provisions **IAM roles, RDS instances, and S3 buckets**
for Kubernetes workloads using a single unified IAM role per workload.

Source: [github.com/alexconrey/deckwatch-plugin-aws](https://github.com/alexconrey/deckwatch-plugin-aws)

---

## What it does

Each workload gets exactly one IAM role. Policies for RDS and S3 are attached as
inline policies on that role, keeping IAM state minimal and auditable. The plugin
creates or verifies the role first, then applies whatever resource policies are
needed — operators never have to manage cross-service IAM wiring manually.

### Capabilities provided

| Capability ID | Description |
|---|---|
| `aws:iam-role` | IAM role created for this workload |
| `aws:service-account` | ServiceAccount with IRSA annotation applied |
| `aws:rds-connection` | RDS instance provisioned |
| `aws:s3-bucket` | S3 bucket provisioned |

Downstream plugins can declare `depends_on: ["aws:iam-role"]` to run after this
plugin and read its outputs.

---

## Prerequisites

- deckwatch operator running in your cluster
- AWS credentials configured in `PluginConfig.config` (see [Configuration](#configuration))
- For RDS IAM auth: an OIDC provider configured for your EKS cluster
- For AWS Backup snapshots: an IAM role that `backup.amazonaws.com` can assume

---

## Installing via the deckwatch Marketplace

1. In the deckwatch UI, go to **Settings → Plugins → Marketplace**
2. Find the **AWS** plugin and click **Install**
3. deckwatch will prompt you to confirm the `allowed_hosts` list
4. After install, navigate to **Settings → Plugins → AWS** and fill in the
   required configuration keys (see below)

### Installing via Settings (direct)

1. Go to **Settings → Plugins → Add**
2. Set source type to **GitHub**
3. Repo: `alexconrey/deckwatch-plugin-aws`, Ref: `v0.2.4`, Path: `plugin.wasm`

---

## Configuration

Set the following keys in your `PluginConfig.config`:

| Key | Required | Description |
|---|---|---|
| `AWS_ACCESS_KEY_ID` | Yes | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Yes | AWS secret key |
| `AWS_SESSION_TOKEN` | No | Session token (for temporary credentials) |
| `AWS_REGION` | No | Default AWS region (falls back to `us-east-1`) |
| `BUCKET_PREFIX` | No | Prepended to every bucket name, e.g. `"myorg-"` |

---

## Annotation reference

### Global — `aws.deckwatch.io/`

| Annotation | Example | Notes |
|---|---|---|
| `aws.deckwatch.io/enabled` | `"true"` | Master opt-in. Also implied by any rds/s3 annotation. |
| `aws.deckwatch.io/role-name` | `"myapp-role"` | Optional. Defaults to `<namespace>-<deployment>-role`. |

### RDS — `rds.deckwatch.io/`

| Annotation | Example | Notes |
|---|---|---|
| `rds.deckwatch.io/enabled` | `"true"` | Must be set to provision an RDS instance. |
| `rds.deckwatch.io/engine` | `"postgres"` | `"postgres"` (default) or `"mysql"`. |
| `rds.deckwatch.io/instance-class` | `"db.t3.micro"` | Default: `db.t3.micro`. |
| `rds.deckwatch.io/allocated-storage` | `"20"` | GiB. Default: 20. |
| `rds.deckwatch.io/identifier` | `"myapp-db"` | RDS instance identifier. Defaults to `<ns>-<deploy>-db`. |
| `rds.deckwatch.io/db-name` | `"app"` | Initial database name. Default: `"app"`. |
| `rds.deckwatch.io/multi-az` | `"false"` | Enable Multi-AZ. Default: false. |
| `rds.deckwatch.io/subnet-group` | `"my-subnet-group"` | Optional DB subnet group. |
| `rds.deckwatch.io/security-groups` | `"sg-abc,sg-def"` | Comma-separated VPC security group IDs. |
| `rds.deckwatch.io/iam-auth` | `"true"` | Use IAM database authentication. Injects `DB_IAM_AUTH=true`. |
| `rds.deckwatch.io/snapshot-schedule` | `"cron(0 3 * * ? *)"` | AWS EventBridge cron for AWS Backup. |
| `rds.deckwatch.io/snapshot-retention` | `"7"` | AWS Backup retention days. Default: 7. |
| `rds.deckwatch.io/backup-role-arn` | `"arn:aws:iam::…:role/backup"` | IAM role for `backup.amazonaws.com`. |

### S3 — `s3.deckwatch.io/`

| Annotation | Example | Notes |
|---|---|---|
| `s3.deckwatch.io/enabled` | `"true"` | Must be set to provision a bucket. |
| `s3.deckwatch.io/bucket-name` | `"assets"` | Name suffix. Final name is `{BUCKET_PREFIX}{bucket-name}`. |
| `s3.deckwatch.io/region` | `"us-east-1"` | Bucket region. Default: `us-east-1`. |
| `s3.deckwatch.io/versioning` | `"true"` | Enable object versioning. Default: false. |
| `s3.deckwatch.io/public-access-block` | `"true"` | Block all public access. Default: true. |
| `s3.deckwatch.io/lifecycle-days` | `"90"` | Expire objects after N days. |

---

## Plugin outputs

Downstream plugins can read the following keys from `ctx.plugin_outputs["aws"]`:

| Key | Description |
|---|---|
| `role_arn` | Full ARN of the workload IAM role |
| `service_account_name` | Name of the created ServiceAccount |
| `rds_endpoint` | RDS hostname (empty while instance is provisioning) |
| `s3_bucket` | Full bucket name (prefix applied) |

---

## Changelog

### v0.2.4
- Partition-aware IAM endpoint with configurable override

### v0.2.3
- Configurable IAM role path via `ROLE_PATH` plugin config key

### v0.2.2
- Scoped `CreateRole` to `/deckwatch-plugin/` path

### v0.2.1
- Fixed clock: replaced `SystemTime::now()` with HTTP Date header for WASM compatibility

### v0.2.0
- Added STS `AssumeRoleWithWebIdentity` for IRSA/OIDC credential exchange
