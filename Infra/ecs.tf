resource "aws_ecs_cluster" "riot_crawler_cluster" {
  name = "riot-crawler-cluster"
}


resource "aws_ecs_task_definition" "task" {
  family                   = "riot-api-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_exec_role.arn
  task_role_arn            = aws_iam_role.ecs_exec_role.arn
  container_definitions = jsonencode([
    {
      name      = "riot-cralwer-task"
      image     = "${aws_ecr_repository.riot_crawler.repository_url}:latest"
      cpu       = 256
      memory    = 512
      essential = true
      environment = [
        {
          name  = "BUCKET_NAME",
          value = "silla.lab.ai.dataset"
        },
        {
          name  = "QUEUE",
          value = "RANKED_SOLO_5x5"
        },
        {
          name  = "TIER",
          value = "IRON"
        },
        {
          name  = "DIVISION",
          value = "I"
        }
      ],
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/riot-crawler",
          "awslogs-region"        = var.region,
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}


# ECS 서비스 생성

resource "aws_ecs_service" "service" {
  name            = "riot-api-service"
  cluster         = aws_ecs_cluster.riot_crawler_cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [var.subnet_ids[0]]
    security_groups  = [aws_security_group.sg.id]
    assign_public_ip = true
  }
  lifecycle {
    ignore_changes = [
      desired_count
    ]
  }
}

resource "aws_security_group" "sg" {
  name        = "allow_traffic"
  description = "Allow all inbound traffic"
  vpc_id      = var.vpc_id

}

resource "aws_security_group_rule" "allow_http" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  security_group_id = aws_security_group.sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "allow_https" {
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}
