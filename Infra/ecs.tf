resource "aws_ecs_cluster" "riot_crawler_cluster" {
  name = "riot-crawler-cluster"
}

# ECS 태스크 정의 생성
resource "aws_ecs_task_definition" "riot_crawler_task" {
  family                   = "riot-cralwer-task"
  container_definitions    = <<DEFINITION
    [
        {
            "name": "riot-crawler-container",
            "image": "${aws_ecr_repository.riot_crawler.repository_url}:latest",
            "cpu": 256,
            "memory": 512,
            "essential": true,
            ]
        }
    ]
DEFINITION
}

# ECS 서비스 생성
resource "aws_ecs_service" "riot_crawler_service" {
  name            = "riot-crawler-service"
  cluster         = aws_ecs_cluster.riot_crawler_cluster.id
  task_definition = aws_ecs_task_definition.riot_crawler_task.arn
  desired_count   = 1

  deployment_minimum_healthy_percent = 0
  deployment_maximum_percent         = 200
}
