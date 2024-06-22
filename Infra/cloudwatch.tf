resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/riot-crawler"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "riot_logs" {
  name              = "/ecs/riot-server"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "riot_logs_worker" {
  name              = "/ecs/riot-worker"
  retention_in_days = 30
}
