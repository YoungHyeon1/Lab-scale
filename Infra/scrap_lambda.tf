# data "archive_file" "script_lambda_zip" {
#   type        = "zip"
#   source_file = "lambda_file/scraper.py"
#   output_path = "lambda_file/ScraperHandler.zip"
# }


# resource "aws_lambda_function" "scraper_handler" {
#   filename      = "lambda_file/ScraperHandler.zip"
#   function_name = "ScraperHandler"
#   role          = aws_iam_role.scraper_role.arn
#   handler       = "scraper.scraper_handler"
#   runtime       = "python3.11"
#   timeout       = 90
#   memory_size   = 2048

#   vpc_config {
#     subnet_ids         = var.public_subnet_ids
#     security_group_ids = [aws_security_group.sg_fastapi.id]
#   }

#   source_code_hash = filebase64sha256(data.archive_file.script_lambda_zip.output_path)
#   layers = [aws_lambda_layer_version.riot_layer.arn]
# }

# data "aws_iam_policy_document" "scraper_role_document" {
#   statement {
#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["lambda.amazonaws.com"]
#     }

#     actions = ["sts:AssumeRole"]
#   }
# }

# data "aws_iam_policy_document" "scraper_policy_document" {
#   statement {
#     effect = "Allow"

#     actions = [
#       "sqs:DeleteMessage",
#       "dynamodb:PutItem",
#       "dynamodb:DeleteItem",
#       "sqs:ReceiveMessage",
#       "dynamodb:Scan",
#       "dynamodb:Query",
#       "dynamodb:UpdateItem",
#       "sqs:GetQueueAttributes",
#       "logs:CreateLogGroup",
#       "logs:PutLogEvents",
#       "s3:PutObject",
#       "logs:CreateLogStream",
#       "dynamodb:GetItem",
#       "ec2:CreateNetworkInterface",
#       "ec2:DescribeNetworkInterfaces",
#       "ec2:DescribeNetworkInterfacePermissions",
#       "ec2:DeleteNetworkInterfacePermission",
#       "ec2:DeleteNetworkInterface"
#     ]

#     resources = [
#       "*",
#       "arn:aws:sqs:ap-northeast-2:${var.account_id}:*"
#     ]
#   }
# }


# resource "aws_iam_policy" "scraper_policy_iam" {
#   name        = "riot_lambda_policy"
#   path        = "/"
#   description = "IAM policy for logging from a lambda"
#   policy      = data.aws_iam_policy_document.scraper_policy_document.json
# }

# resource "aws_iam_role" "scraper_role" {
#   name               = "ScraperLambda"
#   assume_role_policy = data.aws_iam_policy_document.scraper_role_document.json
# }

# resource "aws_iam_role_policy_attachment" "scraper_handler_policy_attachment" {
#   role       = aws_iam_role.scraper_role.name
#   policy_arn = aws_iam_policy.scraper_policy_iam.arn
# }

# resource "aws_cloudwatch_log_group" "scraper_riot_group" {
#   name              = "/aws/lambda/${aws_lambda_function.scraper_handler.function_name}"
#   retention_in_days = 14
# }

# # Lambda function Layer
# resource "aws_lambda_layer_version" "riot_layer" {
#   layer_name = "riot_layer"
#   compatible_runtimes = ["python3.11"]

#   filename = "labda_layer/python.zip"

#   source_code_hash = filebase64sha256("labda_layer/python.zip")
# }


# # SQS 트리거
# resource "aws_lambda_event_source_mapping" "lambda_sqs_trigger" {
#   event_source_arn = aws_sqs_queue.riot_server_queue.arn
#   function_name    = aws_lambda_function.scraper_handler.arn

#   batch_size       = 10
#   enabled          = true
# }