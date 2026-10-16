from shared.services.session import Session

import pytest
from pyspark.sql import SparkSession


@pytest.fixture
def session() -> SparkSession:
    """
    Fixture to provide a SparkSession instance.

    :return: SparkSession: SparkSession instance.
    """
    session = Session.get()
    return session


def test_singleton(session: SparkSession):
    """
    Test to verify the singleton behavior of the SparkSession.

    :param session: SparkSession: SparkSession instance.
    :return: None
    """
    session2 = Session.get()
    assert session2 is session
