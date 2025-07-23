import functions_framework

# CloudEvent function to be triggered by an Eventarc Cloud Audit Logging trigger
# Note: this is NOT designed for second-party (Cloud Audit Logs -> Pub/Sub) triggers!
@functions_framework.cloud_event
def hello_auditlog(cloudevent):
    # Print out the CloudEvent's (required) `type` property
    # See https://github.com/cloudevents/spec/blob/v1.0.1/spec.md#type
    print(f"Event type: {cloudevent['type']}")

    # Print out the CloudEvent's (optional) `subject` property
    # See https://github.com/cloudevents/spec/blob/v1.0.1/spec.md#subject
    if 'subject' in cloudevent:
        # CloudEvent objects don't support `get` operations.
        # Use the `in` operator to verify `subject` is present.
        print(f"Subject: {cloudevent['subject']}")

    # Print out details from the `protoPayload`
    # This field encapsulates a Cloud Audit Logging entry
    # See https://cloud.google.com/logging/docs/audit#audit_log_entry_structure

    payload = cloudevent.data.get("protoPayload")
    if payload:
        print(f"API method: {payload.get('methodName')}")
        print(f"Resource name: {payload.get('resourceName')}")
        print(f"Principal: {payload.get('authenticationInfo', dict()).get('principalEmail')}")




{
  "bucket": "some-bucket",
  "contentType": "text/plain",
  "crc32c": "rTVTeQ==",
  "etag": "CNHZkbuF/ugCEAE=",
  "generation": "1587627537231057",
  "id": "some-bucket/folder/Test.cs/1587627537231057",
  "kind": "storage#object",
  "md5Hash": "kF8MuJ5+CTJxvyhHS1xzRg==",
  "mediaLink": "https://www.googleapis.com/download/storage/v1/b/some-bucket/o/folder%2FTest.cs?generation=1587627537231057&alt=media",
  "metageneration": "1",
  "name": "folder/Test.cs",
  "selfLink": "https://www.googleapis.com/storage/v1/b/some-bucket/o/folder/Test.cs",
  "size": "352",
  "storageClass": "MULTI_REGIONAL",
  "timeCreated": "2020-04-23T07:38:57.230Z",
  "timeStorageClassUpdated": "2020-04-23T07:38:57.230Z",
  "updated": "2020-04-23T07:38:57.230Z"
}