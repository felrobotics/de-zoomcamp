
resource "google_storage_bucket" "de-bucket" {
  name          = "de-zoomcamp-felipe-bucket"
  location      = "US"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}
