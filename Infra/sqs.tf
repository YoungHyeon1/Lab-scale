resource "aws_sqs_queue" "riot_server_queue" {
  name                      = "riot-queue"  # 큐의 이름, 유니크해야 합니다.
  delay_seconds             = 0           # 메시지가 전송된 후 대기하는 시간(초)
  max_message_size          = 262144      # 메시지 최대 크기(바이트)
  message_retention_seconds = 345600      # 메시지 보관 시간(초)
  receive_wait_time_seconds = 0           # 롱 폴링 설정, 0은 롱 폴링을 사용하지 않음을 의미
  visibility_timeout_seconds = 90         # 메시지를 처리하는 동안 보이지 않게 하는 시간(초)
}
