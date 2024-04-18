# SNS 토픽 생성
resource "aws_sns_topic" "crawler_info_topic" {
  name = "cralwer_info"
}

# 이메일 구독 생성
resource "aws_sns_topic_subscription" "cralwer_info_subscription" {
  topic_arn = aws_sns_topic.crawler_info_topic.arn
  protocol  = "email"
  endpoint  = "kyh99910@gmail.com"
}
