

resource "aws_s3_bucket" "a" {
  bucket = "jono-test-489284-a"
  acl    = "private"

}


resource "aws_s3_bucket" "b" {
  bucket = "jono-test-fsf34-b"
  acl    = "private"

}
