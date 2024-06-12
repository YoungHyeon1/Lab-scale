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
  type        = list(string)
}

variable "riot_db_username" {
  description = "riot DB username"
  type        = string
}

variable "riot_db_password" {
  description = "roptr_db_password"
  type        = string
}

variable "subnet_id_2b" {
  description = "The ID of the subnet in the availability zone 2b"
  type        = string
}


variable "cidr_private_subnet_2b" {
  description = "CIDR block for the private subnet"
  default     = "172.31.32.0/24"
}

variable "cird_private_subnet_2a" {
  description = "CIDR block for the private subnet"
  default     = "172.31.33.0/24"
}

variable "availability_2a_zone" {
  description = "value of the availability zone"
  default     = "ap-northeast-2a"
}


variable "availability_2b_zone" {
  description = "Availability Zone to create the resources"
  default     = "ap-northeast-2b"
}

