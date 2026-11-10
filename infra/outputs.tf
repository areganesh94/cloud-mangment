output "ecr_repository_url" {
  description = "ECR repository URI for application images."
  value       = aws_ecr_repository.app.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.app.name
}

output "app_service_name" {
  description = "ECS service name, if the service is enabled."
  value       = var.deploy_app_service ? aws_ecs_service.app[0].name : null
}

output "app_log_group" {
  description = "CloudWatch log group for the application."
  value       = aws_cloudwatch_log_group.app.name
}