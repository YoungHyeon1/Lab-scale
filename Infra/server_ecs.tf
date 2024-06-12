# FastAPI Service ECS 생성

resource "aws_ecs_cluster" "riot_server_cluster" {
  name = "riot-server-cluster"
}

resource "aws_ecs_task_definition" "riot_server_task" {
  family                   = "riot-server-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"
  memory                   = "512"
  execution_role_arn       = aws_iam_role.ecs_exec_role.arn
  task_role_arn            = aws_iam_role.ecs_exec_role.arn

  container_definitions = jsonencode([
    {
      name      = "riot-server-container"
      image     = "${aws_ecr_repository.riot_api_repository.repository_url}:latest"
      cpu       = 256
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 8000,
          hostPort      = 8000,
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/riot-server",
          "awslogs-region"        = var.region,
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

resource "aws_security_group" "sg_fastapi" {
  name        = "fastapi_traafic"
  description = "Allow all inbound traffic"
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "allow_rdb_from_fastapi" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.sg_fastapi.id
  security_group_id        = aws_security_group.riot_rds_sg.id
  description              = "Allow FastAPI server to access RDB on port 5432"
}

resource "aws_security_group_rule" "fastapi_traafic" {
  type              = "ingress"
  from_port         = 8000
  to_port           = 8000
  protocol          = "tcp"
  security_group_id = aws_security_group.sg_fastapi.id
  cidr_blocks       = ["0.0.0.0/0"]
}
