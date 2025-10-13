variable "ec2_ami" {
  type        = string
  description = "ec2 instance AMI ID"
  default     = "ami-0360c520857e3138f"
}

variable "ec2_type" {
  type        = string
  description = "ec2 instance type ex. t2.micro, t3.large etc"
  default     = "t2.micro"
}

variable "ec2_name_tag" {
  type        = string
  description = "name tag to the ec2 instance"
  default     = "My ec2 instance"
}

# output variables

output "ec2_ip" {
  value       = aws_instance.my_ec2.public_ip
  description = "IP address of my_ec2 instance"
}

output "ec2_instance_id" {
  value       = aws_instance.my_ec2.id
  description = "Instance ID"
}