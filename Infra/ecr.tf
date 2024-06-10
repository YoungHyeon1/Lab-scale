
resource "aws_ecr_repository" "riot_crawler" {
  name = "riot_crawler-repo"
}

resource "aws_ecr_repository" "riot_api_repository" {
  name = "riot-api-server-repo"
}
