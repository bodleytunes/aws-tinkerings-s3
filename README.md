#### Processing exif data for images.

###### End state/goal

* Server would be running in AWS
* Server would have both "A bucket" and "B bucket" mounted to local filesystem with s3fs-fuse and fstab for persistence.
* Ideally a docker container with the embedded python service would run and process files it sees in bucket A and then re-upload to bucket B, basically all code would be containerized and tagged for versioning/release.
* Terraform to be used to deploy the VM, ansible would configure the container to use image version x.xx to run and also would be used to deploy the buckets.

![Alt Text](aws-s3-exif-processing.gif)