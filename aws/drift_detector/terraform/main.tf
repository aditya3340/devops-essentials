terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.18.0"
    }
  }

  backend "s3" {
    
    bucket = "amzn-s3-terraform-backend-adi3340" #s3 bucket name
    key = "terraform/dev/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    # dynamodb_table = "my-terraform-lock-table" for DynamoDB locking
    use_lockfile = true  # Recommeded for s3-native locking
  }
}

provider "aws" {
  region = "us-east-1"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "6.5.0"

  name = "example-vpc"

  cidr = "10.0.0.0/16"

  azs = ["us-east-1a", "us-east-1b"]

  public_subnets  = ["10.0.1.0/24"]
  private_subnets = ["10.0.0.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  tags = {
    Enviroment = "test"
  }

}

resource "aws_instance" "ec2_instance" {
  ami = "ami-0bdd88bd06d16ba03"
  instance_type = "t2.micro"
  # subnet_id = module.vpc.public_subnets[0]
}