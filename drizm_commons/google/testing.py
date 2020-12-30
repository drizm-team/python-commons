import uuid
from pathlib import Path
from typing import Optional, Union

from google.cloud import storage
from google.oauth2.credentials import Credentials

PathLike = Union[Path, str]


class TestStorageBucket:
    """ A class that exposes a simple API for testing buckets. """

    def __init__(
        self,
        credentials: Union[Credentials, PathLike],
        project_id: str,
        *,
        bucket_name: Optional[str] = None,
        bucket_region: Optional[str] = "EU",
        default_acl: Optional[str] = "projectPrivate",
    ) -> None:
        self.credentials = credentials
        self.project_id = project_id
        self.default_acl = default_acl

        self.bucket_name = bucket_name or self._autogenerate_bucket_name()
        self.bucket_region = bucket_region
        self.bucket = None

        if isinstance(self.credentials, Path) or type(self.credentials) == str:
            self.client = storage.Client.from_service_account_json(
                str(self.credentials)
            )
        else:
            self.client = storage.Client(
                project=project_id, credentials=self.credentials
            )

    @staticmethod
    def _autogenerate_bucket_name() -> str:
        """
        Automatically generates a generic bucket name,
        in case none was provided by the user.
        """
        return f"{uuid.uuid4().hex}__test_bucket"

    def create(self, obtain_existing: Optional[bool] = False) -> storage.Bucket:
        """
        Obtain the testing bucket.

        If a bucket already exists under this name,
        you can pass 'obtain_existing = True' to retrieve it.

        If no parameters are provided,
        this method will create a new bucket with the given name.
        """
        if obtain_existing:
            self.bucket = self.client.get_bucket(self.bucket_name)
        else:
            self.bucket = self.client.create_bucket(
                bucket_or_name=self.bucket_name,
                project=self.client.project,
                location=self.bucket_region,
            )

        return self.bucket

    def destroy(self) -> None:
        """
        Delete the testing bucket and all items in it.

        As per the limitations of the Python GCS API,
        this will only work on buckets with 256 blobs or less.
        """
        if not self.bucket:
            raise RuntimeError(
                "Bucket has been instantiated yet or is already deleted."
            )
        self.bucket.delete(force=True, client=self.client)
