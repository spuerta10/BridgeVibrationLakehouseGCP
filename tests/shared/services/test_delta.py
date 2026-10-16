from unittest.mock import MagicMock
from shared.services.delta import DeltaTable

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    IntegerType,
    FloatType,
    StringType
)


@pytest.fixture
def mock_spark_session() -> MagicMock:
    """
    Fixture to provide a mocked SparkSession object.

    :return: MagicMock: Mocked SparkSession instance.
    """
    session = MagicMock(spec=SparkSession)
    return session


@pytest.fixture
def table_name() -> str:
    """
    Fixture to provide a table name.

    :return: str: Name of the test table.
    """
    return "test_table"


@pytest.fixture(params=[
    (
        StructType().add("id", IntegerType()),
        """
        CREATE TABLE IF NOT EXISTS test_table (
            id INT
        )
        USING DELTA
        LOCATION 'path/to/test_table'
        """
    ),
    (
        StructType().add("id", IntegerType()).add("datetime", StringType()),
        """
        CREATE TABLE IF NOT EXISTS test_table (
            id INT,
            datetime STRING
        )
        USING DELTA
        LOCATION 'path/to/test_table'
        """
    ),
    (
        StructType().add("id", IntegerType()).add("datetime", StringType()).add("vib_x", FloatType()),
        """
        CREATE TABLE IF NOT EXISTS test_table (
            id INT,
            datetime STRING,
            vib_x FLOAT
        )
        USING DELTA
        LOCATION 'path/to/test_table'
        """
    ),
])
def data_schema_n_expected_query(request) -> tuple[StructType, str]:
    """
    Fixture to provide data schema and the expected SQL query string for table creation.

    :param request: Fixture request object.
    :return: tuple[StructType, str]: Tuple containing data schema and expected SQL query string.
    """
    return request.param


@pytest.fixture
def table_path() -> str:
    """
    Fixture to provide the path to the test table.

    :return: str: Path to the test table.
    """
    return "path/to/test_table"


def test_create_table(mock_spark_session: MagicMock,
                      table_name: str,
                      data_schema_n_expected_query: tuple[StructType, str],
                      table_path: str):
    """
    Test to verify table creation SQL query generation and execution.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param table_name: str: Name of the test table.
    :param data_schema_n_expected_query: tuple[StructType, str]: Tuple containing data schema and expected SQL query string.
    :param table_path: str: Path to the test table.
    :return: None
    """
    data_schema, expected_query = data_schema_n_expected_query

    delta = DeltaTable(mock_spark_session)
    delta.create(table_name, data_schema, table_path)

    delta_create_method_call_result = mock_spark_session.sql.call_args_list[0][0][0]
    filtered_call = delta_create_method_call_result.replace("\n", "").replace(" ", "")

    filtered_expected_query = expected_query.replace("\n", "").replace(" ", "")

    assert filtered_call == filtered_expected_query
