terraform {

  required_version = ">=1.3.8"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.54.0"
    }
  }
  backend "s3" {
    encrypt = true
    bucket  = "052937280793-tfstate"
    region  = "us-east-1"
    profile = "programmatic-user"
  }

}