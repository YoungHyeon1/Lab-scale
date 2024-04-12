####
# Create an S3 bucket to store the Terraform state file
####
resource "aws_s3_bucket" "terraform_bucket" {
  bucket = "silla.lab.terraform.state"

  tags = {
    Name        = "Terrform State Bucket"
    Environment = "Production"
  }
}


####
# Create AI DataSet S3 bucket
####

resource "aws_s3_bucket" "ai_dataset_bucket" {
  bucket = "silla.lab.ai.dataset"

  tags = {
    Name        = "AI Dataset Bucket"
    Environment = "Production"
  }
}
