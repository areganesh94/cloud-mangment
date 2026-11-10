variable "aws_region" {
  description = "AWS region for the stack."
  type        = string
  default     = "us-east-1"
}

variable "name" {
  description = "Prefix used for AWS resource names."
  type        = string
  default     = "cloud-management"
}

variable "deploy_app_service" {
  description = "Create the Fargate service after the container image and database secret are ready."
  type        = bool
  default     = false
}

variable "vpc_id" {
  description = "ID of the existing VPC; required when deploying the app service."
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "Existing subnet IDs for Fargate tasks; required when deploying the app service."
  type        = list(string)
  default     = []
}

variable "container_image" {
  description = "Image URI to run, including an immutable tag or digest."
  type        = string
  default     = ""
}

variable "database_url_secret_arn" {
  description = "Secrets Manager ARN containing the DATABASE_URL value."
  type        = string
  default     = ""
}

variable "allowed_ingress_cidrs" {
  description = "CIDR blocks allowed to reach the task on port 5000. Keep this limited to trusted networks."
  type        = list(string)
  default     = []
}

variable "assign_public_ip" {
  description = "Assign public IPs to tasks; only enable when using public subnets and deliberate public ingress rules."
  type        = bool
  default     = false
}

variable "desired_count" {
  description = "Number of running Fargate tasks when the app service is enabled."
  type        = number
  default     = 1
}