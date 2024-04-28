variable "vpc_id" {
  description = "The ID of the VPC"
  type        = string
}

variable "region" {
  description = "The region of the VPC"
  type        = string
}

variable "subnet_ids" {
  description = "The IDs of the subnets"
  type        = list(string)
}


variable "route_table_id" {
  description = "The ID of the route table"
  type        = string
}


variable "account_id" {
  description = "The ID of the AWS account"
  type        = string

}

variable "secrets_id" {
  description = "The ID of the secret"
  type        = string

}
