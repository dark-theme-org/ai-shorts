variable "folder_prod" {
  type        = string
  description = "The folder name inside bucket for production environment"
  default     = "prod"
}

variable "folder_test" {
  type        = string
  description = "The folder name inside bucket for test environment"
  default     = "test"
}

variable "organization" {
  type        = string
  description = "GitHub organization"
  default     = "Dark Theme"
}

variable "project" {
  type        = string
  description = "GitHub project name for Terraform"
  default     = "ai-shorts"
}

variable "region" {
  type        = string
  description = "AWS region name"
  default     = "us-east-1"
}
