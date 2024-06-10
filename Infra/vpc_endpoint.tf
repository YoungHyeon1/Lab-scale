# ECR Endpoint

resource "aws_vpc_endpoint" "ecr_api_endpoint" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.${var.region}.ecr.api"
  vpc_endpoint_type = "Interface"

  subnet_ids          = var.subnet_ids
  private_dns_enabled = true
  security_group_ids  = [aws_security_group.sg.id]
}

resource "aws_vpc_endpoint" "ecr_dkr_endpoint" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type = "Interface"

  subnet_ids          = var.subnet_ids
  private_dns_enabled = true
  security_group_ids  = [aws_security_group.sg.id]
}


# S3 Endpoint
resource "aws_vpc_endpoint" "s3_endpoint" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"

  route_table_ids = [var.route_table_id]
}

# Secrets Manager Endpoint
resource "aws_vpc_endpoint" "secrets_manager_endpoint" {
  vpc_id            = var.vpc_id
  service_name      = "com.amazonaws.${var.region}.secretsmanager"
  vpc_endpoint_type = "Interface"

  subnet_ids          = var.subnet_ids
  private_dns_enabled = true
  security_group_ids  = [aws_security_group.sg.id]
}


# Private Subnet
resource "aws_subnet" "private_subnet" {
  vpc_id            = var.vpc_id
  cidr_block        = var.cidr_private_subnet
  availability_zone = var.availability_zone
  map_public_ip_on_launch = false

  tags = {
    Name = "Private Subnet"
  }
}

