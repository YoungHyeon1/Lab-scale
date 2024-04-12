####
# Terraform Configuration
# This file is used to configure the Terraform state file and the DynamoDB table to lock the state file.
####
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
  backend "s3" {
    bucket         = "silla.lab.terraform.state"
    key            = "terraform.tfstate"
    region         = "ap-northeast-2"
    encrypt        = true
    dynamodb_table = "TerraformStateLock"
    acl            = "bucket-owner-full-control"
  }
}

resource "aws_dynamodb_table" "terraform_state_lock" {
  name           = "TerraformStateLock"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}


resource "aws_s3_bucket" "terraform-state" {
  bucket = "silla.lab.terraform.state"

  lifecycle {
    prevent_destroy = true
  }
}
