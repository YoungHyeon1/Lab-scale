

# NAT Gateway (Elastic IP 필요)
resource "aws_eip" "nat" {
  vpc = true
}
resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat.id
  subnet_id     = var.db_subnet_id[0]
  tags = {
    Name = "NAT Gateway"
  }
}
# NAT Gateway를 사용하는 라우팅 테이블
resource "aws_route_table" "private_route_table" {
  vpc_id     = var.vpc_id
  depends_on = [aws_nat_gateway.nat_gateway]

  # route {
  #   cidr_block = "0.0.0.0/0"
  #   gateway_id = aws_nat_gateway.nat_gateway.id
  # }
}

resource "aws_route_table_association" "private_subnet_association" {
  subnet_id      = var.db_subnet_id[0]
  route_table_id = aws_route_table.private_route_table.id
}

resource "aws_route_table_association" "private_subnet_association_2b" {
  subnet_id      = var.db_subnet_id[1]
  route_table_id = aws_route_table.private_route_table.id
}
