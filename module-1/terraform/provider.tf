terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  # Configuration options    
  project = "de-zoomcamp-412714"
  region  = "us-central1"
  #   credentials = xxx # BETTER! use export GOOGLE_CREDENTIALS="path_to_key.json"
}
