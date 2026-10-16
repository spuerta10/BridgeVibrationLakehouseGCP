from unittest.mock import MagicMock
from shared.services.google_storage import GoogleStorage
from shared.services.pipeline import (
    Pipeline,
    NotExistingDeltaTableError,
    MissingExtractStageError,
    MissingTransformStageError,
    MissingLoadStageError
)

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StringType,
    FloatType
)


@pytest.fixture
def mock_spark_session() -> MagicMock:
    """
    Fixture for creating a mocked SparkSession instance.

    :return: MagicMock: A MagicMock object representing a SparkSession.
    """
    session = MagicMock(spec=SparkSession)
    return session


@pytest.fixture
def mock_storage_client() -> MagicMock:
    """
    Fixture for creating a mocked StorageInterface instance.

    :return: MagicMock: A MagicMock object representing a StorageInterface.
    """
    client = MagicMock(spec=GoogleStorage)
    return client


@pytest.fixture
def input_data_schema() -> StructType:
    """
    Fixture for generating a sample StructType input data schema.

    :return: StructType: A StructType schema.
    """
    return (
        StructType()
        .add("datetime", StringType())
        .add("vib_x", FloatType())
        .add("vib_y", FloatType())
        .add("vib_z", FloatType())
    )


@pytest.fixture
def output_data_schema() -> StructType:
    """
    Fixture for generating a sample StructType output data schema.

    :return: StructType: A StructType schema.
    """
    return (
        StructType()
        .add("datetime", StringType())
        .add("vib_x", FloatType())
        .add("vib_y", FloatType())
        .add("vib_z", FloatType())
        .add("freq_vib_x", FloatType())
        .add("freq_vib_y", FloatType())
        .add("freq_vib_z", FloatType())
    )


def test_build_delta_table_non_existing_table_path(mock_spark_session: MagicMock,
                                                   mock_storage_client: MagicMock,
                                                   output_data_schema: StructType):
    """
    Test to build a Delta table when the table path does not exist.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :param output_data_schema: StructType: Sample StructType schema.
    :return: None
    """
    mock_spark_session.catalog.tableExists.return_value = False

    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    with pytest.raises(NotExistingDeltaTableError) as exc_info:
        pipeline.build_delta_table("test_table", output_data_schema, "non_existing_table_path")

    assert exc_info.type is NotExistingDeltaTableError


def test_build_delta_table_existing_table_path(mock_spark_session: MagicMock,
                                               mock_storage_client: MagicMock,
                                               output_data_schema: StructType):
    """
    Test to build a Delta table when the table path already exists.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :param output_data_schema: StructType: Sample StructType schema.
    :return: None
    """
    mock_spark_session.catalog.tableExists.return_value = True

    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    result = pipeline.build_delta_table("test_table", output_data_schema, "existing_table_path")

    assert isinstance(result, Pipeline)
    assert result is pipeline


def test_build_extract_stage(mock_spark_session: MagicMock,
                             mock_storage_client: MagicMock,
                             input_data_schema: StructType):
    """
    Test to build the extract stage of the pipeline.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :param input_data_schema: StructType: Sample StructType schema.
    :return: None
    """
    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    pipeline.build_extract_stage(input_data_schema, "data_extraction_path")
    assert pipeline._extract_stage is not None


def test_build_transform_stage(mock_spark_session: MagicMock,
                               mock_storage_client: MagicMock):
    """
    Test to build the transform stage of the pipeline.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :return: None
    """
    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    pipeline.build_transform_stage()
    assert pipeline._transform_stage is not None


def test_build_load_stage(mock_spark_session: MagicMock,
                          mock_storage_client: MagicMock):
    """
    Test to build the load stage of the pipeline.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :return: None
    """
    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    pipeline.build_load_stage("data_load_path")
    assert pipeline._load_stage is not None


def test_execute(mock_spark_session: MagicMock,
                 mock_storage_client: MagicMock,
                 input_data_schema: StructType):
    """
    Test to execute the ETL pipeline.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :param input_data_schema: StructType: Sample StructType schema.
    :return: None
    """
    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    (
        pipeline
        .build_extract_stage(input_data_schema, "data_extract_path")
        .build_transform_stage()
        .build_load_stage("data_load_path")
    )
    result = pipeline.execute("test_table")

    assert result is None


def test_execute_with_missing_extract_stage(mock_spark_session: MagicMock,
                                            mock_storage_client: MagicMock):
    """
    Test to execute the ETL pipeline with a missing extract stage.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :return: None
    """
    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    (
        pipeline
        .build_transform_stage()
        .build_load_stage("data_load_path")
    )

    with pytest.raises(MissingExtractStageError) as exc_info:
        pipeline.execute("test_table")

    assert exc_info.type is MissingExtractStageError


def test_execute_with_missing_transform_stage(mock_spark_session: MagicMock,
                                              mock_storage_client: MagicMock,
                                              input_data_schema: StructType):
    """
    Test to execute the ETL pipeline with a missing transform stage.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :param input_data_schema: StructType: Sample StructType schema.
    :return: None
    """
    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    (
        pipeline
        .build_extract_stage(input_data_schema, "data_extract_path")
        .build_load_stage("test_table")
    )

    with pytest.raises(MissingTransformStageError) as exc_info:
        pipeline.execute("test_table")

    assert exc_info.type is MissingTransformStageError


def test_execute_with_missing_load_stage(mock_spark_session: MagicMock,
                                         mock_storage_client: MagicMock,
                                         input_data_schema: StructType):
    """
    Test to execute the ETL pipeline with a missing load stage.

    :param mock_spark_session: MagicMock: Mocked SparkSession instance.
    :param mock_storage_client: MagicMock: Mocked StorageInterface instance.
    :param input_data_schema: StructType: Sample StructType schema.
    :return: None
    """
    pipeline = Pipeline(mock_spark_session, mock_storage_client)
    (
        pipeline
        .build_extract_stage(input_data_schema, "data_extract_path")
        .build_transform_stage()
    )

    with pytest.raises(MissingLoadStageError) as exc_info:
        pipeline.execute("data_load_path")

    assert exc_info.type is MissingLoadStageError
