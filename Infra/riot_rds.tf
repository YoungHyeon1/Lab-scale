
# Postrese Subnet Group
resource "aws_db_subnet_group" "riot_db_subnet_group" {
  name       = "riot-db-subnet-group"
  subnet_ids = var.db_subnet_id
}


resource "aws_security_group" "riot_rds_sg" {
  name        = "rds-sg"
  description = "Security group for RDS PostgreSQL instance"
  vpc_id      = var.vpc_id
  # ingress {
  #   from_port   = 5432
  #   to_port     = 5432
  #   protocol    = "tcp"
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  # egress {
  #   from_port   = 0
  #   to_port     = 0
  #   protocol    = "-1"
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  tags = {
    Name = "rds-security-group"
  }
}
# RDB free tier DB (PostgreSQL)
resource "aws_db_instance" "riot_db" {
  identifier             = "riot-db"
  engine                 = "postgres"
  instance_class         = "db.t3.micro"
  allocated_storage      = 80
  storage_type           = "gp2"
  storage_encrypted      = false
  engine_version         = "16.2"
  publicly_accessible    = true
  skip_final_snapshot    = false
  username               = var.riot_db_username
  password               = var.riot_db_password
  vpc_security_group_ids = [aws_security_group.riot_rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.riot_db_subnet_group.name
  tags = {
    Name = "riot-db"
  }
}
