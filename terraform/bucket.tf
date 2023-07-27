resource "aws_s3_bucket" "bucket" {
  bucket = format("%s", var.project)

  tags = {
    LastUpdatedAt = timestamp()
    ManagedBy     = "Terraform"
    Project       = var.project
    Organization  = var.organization
  }
}

resource "aws_s3_bucket_ownership_controls" "ownership" {
  bucket = aws_s3_bucket.bucket.id
  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_acl" "acl" {
  bucket     = aws_s3_bucket.bucket.id
  acl        = "private"
  depends_on = [aws_s3_bucket_ownership_controls.ownership]
}

resource "aws_s3_object" "production_folder" {
  bucket = aws_s3_bucket.bucket.id
  key    = format("%s/", var.folder_prod)
}

resource "aws_s3_object" "developer_folder" {
  bucket = aws_s3_bucket.bucket.id
  key    = format("%s/", var.folder_test)
}
