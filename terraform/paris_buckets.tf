

resource "aws_s3_bucket" "a" {
  bucket = "jon-skyline-r33-fxnoqijf-location-a"
  acl    = "private"

}


resource "aws_s3_bucket" "b" {
  bucket = "jon-skyline-r33-fwoid3dd-location-b"
  acl    = "private"

}
