
data "aws_iam_policy_document" "ecs_task_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "ecs_exec_policy_doc" {
  statement {
    actions = [
      "ecr:GetAuthorizationToken",
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:GetRepositoryPolicy",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:CreateLogGroup",
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
      "sns:Publish",
      "sqs:ReceiveMessage",
      "sqs:sendmessage",
      "s3:*"
    ]
    resources = [
      "*",
      "arn:aws:s3:::silla.lab.ai.dataset/*",
      "arn:aws:secretsmanager:ap-northeast-2:652832981770:secret:riot-crawler-api-VXE4BF"

    ]
    effect = "Allow"
  }
}


resource "aws_iam_role" "ecs_exec_role" {
  name               = "ecs_task_execution_role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_policy.json
}

resource "aws_iam_policy" "ecs_exec_policy" {
  name        = "ecs-exec-policy"
  description = "Allows ECS tasks to interact with Logs."
  policy      = data.aws_iam_policy_document.ecs_exec_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy_attach" {
  role       = aws_iam_role.ecs_exec_role.id
  policy_arn = aws_iam_policy.ecs_exec_policy.arn
}
