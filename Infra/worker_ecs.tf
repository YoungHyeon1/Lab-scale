

resource "aws_ecs_task_definition" "riot_worker_task" {
  family                   = "riot-worker-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_exec_role.arn
  task_role_arn            = aws_iam_role.ecs_exec_role.arn

  container_definitions = jsonencode([
    {
      name      = "riot-worker-container"
      image     = "${aws_ecr_repository.riot_worker_repository.repository_url}:latest"
      cpu       = 256
      memory    = 512
      essential = true
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/riot-worker",
          "awslogs-region"        = var.region,
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}
