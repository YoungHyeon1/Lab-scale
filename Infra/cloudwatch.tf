resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/riot-crawler"
  retention_in_days = 30
}
