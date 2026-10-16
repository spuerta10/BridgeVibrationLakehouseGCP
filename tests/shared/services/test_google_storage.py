from shared.services.google_storage import (
    GoogleStorage,
    NotExistingBucketError,
    NotExistingDataInStoragePathError,
    NotExistingStoragePathError
)
from unittest.mock import MagicMock

import pytest
from google.cloud.storage import (
    Client,
    Bucket,
    Blob
)


class MockedIterator:
    """
    A mock iterator class to simulate iteration over a list of pages (blobs).
    """
    def __init__(self, blobs):
        """
        Initialize the MockedIterator with a list of pages containing blobs.

        :param blobs: list: List of blobs representing pages.
        """
        self.pages = [blobs]

    def __iter__(self) -> iter:
        """
        Return an iterator over the pages.

        :return: iterator: Iterator over the pages.
        """
        return iter(self.pages)

    def __len__(self) -> int:
        """
        Return the number of pages.

        :return: int: Number of pages.
        """
        return len(self.pages)


@pytest.fixture
def service_account_json_path() -> str:
    """
    Fixture to provide the path to the Google Cloud service account JSON file.

    :return: str: Path to the service account JSON file.
    """
    return "C:\\Users\\Admin\\DataspellProjects\\dpLakeHouseWorkflow\\src\\config\\service-account.json"


@pytest.fixture
def mock_storage_client() -> MagicMock:
    """
    Fixture to provide a mocked Google Cloud Storage Client instance.

    :return: MagicMock: Mocked Google Cloud Storage Client.
    """
    client = MagicMock(spec=Client)
    return client


@pytest.fixture
def mock_bucket() -> Bucket:
    """
    Fixture to provide a mocked Google Cloud Storage Bucket instance.

    :return: Bucket: Mocked Google Cloud Storage Bucket.
    """
    return Bucket(client=MagicMock(), name="test_bucket")


@pytest.fixture
def mock_google_storage(service_account_json_path: str,
                        mock_storage_client: MagicMock) -> GoogleStorage:
    """
    Fixture to provide a GoogleStorage instance with a mocked client.

    :param service_account_json_path: str: Path to the service account JSON file.
    :param mock_storage_client: MagicMock: Mocked Google Cloud Storage Client.
    :return: GoogleStorage: GoogleStorage instance with mocked client.
    """
    storage = GoogleStorage(service_account_json_path)
    storage._client = mock_storage_client
    return storage 


def test_check_existing_bucket_bucket_exists(mock_storage_client: MagicMock,
                                             mock_bucket: Bucket,
                                             mock_google_storage: GoogleStorage):
    """
    Test to check if a bucket exists in Google Cloud Storage.

    :param mock_storage_client: MagicMock: Mocked Google Cloud Storage Client.
    :param mock_bucket: Bucket: Mocked Google Cloud Storage Bucket.
    :param mock_google_storage: GoogleStorage: GoogleStorage instance.
    :return: None
    """
    mock_storage_client.get_bucket.return_value = mock_bucket

    result = mock_google_storage.check_existing_bucket("gs://existing_bucket")
    assert result is mock_google_storage


def test_check_existing_bucket_bucket_not_exists(mock_storage_client: MagicMock,
                                                 mock_google_storage: GoogleStorage):
    """
    Test to check behavior when a bucket does not exist in Google Cloud Storage.

    :param mock_storage_client: MagicMock: Mocked Google Cloud Storage Client.
    :param mock_google_storage: GoogleStorage: GoogleStorage instance.
    :return: None
    """
    mock_storage_client.get_bucket.side_effect = Exception("Bucket not found")

    with pytest.raises(NotExistingBucketError) as exc_info:
        mock_google_storage.check_existing_bucket("gs://non_existing_bucket")

    assert exc_info.type is NotExistingBucketError


def test_check_existing_data_in_storage_path_with_data(mock_storage_client: MagicMock,
                                                       mock_google_storage: GoogleStorage):
    """
    Test to check if data exists in a storage path.

    :param mock_storage_client: MagicMock: Mocked Google Cloud Storage Client.
    :param mock_google_storage: GoogleStorage: GoogleStorage instance.
    :return: None
    """
    mock_storage_client.bucket().list_blobs.return_value = MockedIterator([MagicMock(spec=Blob)])

    result = mock_google_storage.check_existing_data_in_storage_path("gs://existing_bucket")
    assert result is mock_google_storage


def test_check_existing_data_in_storage_path_empty(mock_storage_client: MagicMock,
                                                   mock_google_storage: GoogleStorage):
    """
    Test to check behavior when a storage path is empty.

    :param mock_storage_client: MagicMock: Mocked Google Cloud Storage Client.
    :param mock_google_storage: GoogleStorage: GoogleStorage instance.
    :return: None
    """
    mock_storage_client.bucket().return_value = MagicMock(spec=Bucket)
    mock_storage_client.list_blobs.return_value = MockedIterator([])

    with pytest.raises(NotExistingDataInStoragePathError) as exc_info:
        mock_google_storage.check_existing_data_in_storage_path("gs://existing_bucket")

    assert exc_info.type is NotExistingDataInStoragePathError


def test_check_existing_data_in_storage_path_error(mock_storage_client: MagicMock,
                                                   mock_google_storage: GoogleStorage):
    """
    Test to check behavior when an error occurs listing blobs in a storage path.

    :param mock_storage_client: MagicMock: Mocked Google Cloud Storage Client.
    :param mock_google_storage: GoogleStorage: GoogleStorage instance.
    :return: None
    """
    mock_storage_client.bucket().list_blobs.side_effect = Exception("Error listing blobs")

    with pytest.raises(NotExistingStoragePathError) as exc_info:
        mock_google_storage.check_existing_data_in_storage_path("gs://existing_bucket/not-existing-path")

    assert exc_info.type is NotExistingStoragePathError
