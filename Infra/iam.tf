# resource "aws_iam_access_key" "s3_access_key" {
#   user = "silla_ai_bucket_user" // IAM 사용자 이름을 입력하세요.
# }

# data "aws_iam_policy_document" "s3_access_policy" {
#   statement {
#     effect = "Allow"
#     actions = [
#       "s3:PutObject",
#       "s3:GetObject",
#       "s3:ListBucket"
#     ]
#     resources = ["arn:aws:s3:::silla.lab.ai.dataset/*"]
#   }
# }

# resource "aws_iam_policy" "s3_access_policy" {
#   name   = "silla-ai-s3-access-policy"
#   path   = "/"
#   policy = data.aws_iam_policy_document.s3_access_policy.json
# }

# resource "aws_iam_policy_attachment" "attach_s3_access_policy" {
#   name       = "attach-s3-access-policy"
#   roles      = ["ai_bucket_access"] // IAM 역할 이름을 입력하세요.
#   policy_arn = aws_iam_policy.s3_access_policy.arn
# }

# output "access_key" {
#   value     = aws_iam_access_key.s3_access_key.id
#   sensitive = true
# }

# output "secret_key" {
#   value     = aws_iam_access_key.s3_access_key.secret
#   sensitive = true

# }

resource "aws_iam_role" "ecs_task_role" {
  name               = "ecs-task-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_s3_access_attachment" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess" # 또는 필요한 S3 액세스 정책을 지정하세요.
}