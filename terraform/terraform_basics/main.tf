# It will create a new ec2_instance in the default vpc with ssh connection and internet access.

resource "aws_instance" "my_ec2" {

  ami           = var.ec2_ami
  instance_type = var.ec2_type

  vpc_security_group_ids = [aws_security_group.sg_ssh.id]

  key_name = var.ec2_key_name

  associate_public_ip_address = true

  tags = {
    Name = var.ec2_name_tag
  }


}

resource "aws_security_group" "sg_ssh" {

  name = "allow ssh connection"
}


resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.sg_ssh.id
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_egress_rule" "allow_all_outbound" {
  security_group_id = aws_security_group.sg_ssh.id
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}


resource "aws_vpc_security_group_ingress_rule" "allow_icmp" {
  security_group_id = aws_security_group.sg_ssh.id
  from_port = -1
  to_port = -1
  ip_protocol = "icmp"
  cidr_ipv4 = "0.0.0.0/0"
}

