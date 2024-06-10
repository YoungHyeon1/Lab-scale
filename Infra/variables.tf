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

variable "db_subnet_id" {
  description = "The ID of the subnet in the availability zone 2b"
  type       = list(string)
}

variable "riot_db_username" {
  description = "riot DB username"
  type       = string
}

variable "riot_db_password" {
  description = "roptr_db_password"
  type       = string
}

variable "subnet_id_2b" {
  description = "The ID of the subnet in the availability zone 2b"
  type        = string
}


variable "cidr_private_subnet" {
  description = "CIDR block for the private subnet"
  default     = "172.31.0.0/16" # 예시 CIDR, 필요에 따라 변경
}


variable "availability_zone" {
  description = "Availability Zone to create the resources"
  default     = "ap-northeast-2a" # 예시 AZ, 필요에 따라 변경
}
