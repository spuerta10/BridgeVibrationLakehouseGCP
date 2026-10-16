from shared.stages.transform import (
    TransformStage,
    EmptyBatchError
)
from random import uniform

import pytest
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, DoubleType
from pyspark.sql.functions import collect_list
from numpy.fft import ifft
from numpy import array


@pytest.fixture
def spark_session() -> SparkSession:
    """
    Fixture to provide a SparkSession object.

    :return: SparkSession: SparkSession instance.
    """
    session = SparkSession.builder.getOrCreate()
    return session


@pytest.fixture()
def batch_schema() -> StructType:
    """
    Fixture that defines the schema for a batch DataFrame containing vibration data.

    :return: StructType representing the schema of the batch DataFrame
    """
    return (
        StructType()
        .add("vib_x", DoubleType())
        .add("vib_y", DoubleType())
        .add("vib_z", DoubleType())
    )


def test_get_frequencies_with_empty_batch(spark_session: SparkSession,
                                          batch_schema: StructType):
    """
    Test function to verify behavior of get_frequencies method with an empty batch DataFrame.

    :param spark_session: PySpark SparkSession object
    :param batch_schema: StructType representing the schema of the batch DataFrame
    :return: None
    """
    empty_dataframe = spark_session.createDataFrame([], batch_schema)
    transform = TransformStage(spark_session)

    with pytest.raises(EmptyBatchError) as exc_info:
        transform.get_frequencies(empty_dataframe)

    assert exc_info.type is EmptyBatchError


@pytest.mark.parametrize(
    "batch_data",
    [
        (
            [(uniform(10.0, 20.0), uniform(10.0, 20.0), uniform(10.0, 20.0))
             for _ in range(3)]
        ),
        (
            [(uniform(10.0, 20.0), uniform(10.0, 20.0), uniform(10.0, 20.0))
             for _ in range(3)]
        ),
        (
            [(uniform(10.0, 20.0), uniform(10.0, 20.0), uniform(10.0, 20.0))
             for _ in range(3)]
        )
    ]
)
def test_get_frequencies_with_non_empty_batch(spark_session: SparkSession,
                                              batch_data: list[tuple],
                                              batch_schema: StructType):
    """
    Test function to verify behavior of get_frequencies method with a non-empty batch DataFrame.

    Assertion 1: Check if the result is of type DataFrame
    Assertion 2: Check if the result DataFrame is not empty
    Assertion 3: Check if all expected frequency columns are present in the result DataFrame
    Assertion 4: Validate frequency calculation for 'freq_vib_x'
    Assertion 5: Validate frequency calculation for 'freq_vib_y'
    Assertion 6: Validate frequency calculation for 'freq_vib_z'

    :param spark_session: PySpark SparkSession object
    :param batch_data: List of tuples representing data for the batch DataFrame
    :param batch_schema: StructType representing the schema of the batch DataFrame
    :return: None
    """
    batch = spark_session.createDataFrame(batch_data, batch_schema)
    transform = TransformStage(spark_session)

    result = transform.get_frequencies(batch)

    assert isinstance(result, DataFrame)
    assert not result.isEmpty()
    assert all(col in result.columns for col in ["freq_vib_x", "freq_vib_y", "freq_vib_z"])
    assert all(
        value in ifft(array(batch.select(collect_list("vib_x")).first()[0])).real.tolist()
        for value in result.select(collect_list("freq_vib_x")).first()[0]
    )
    assert all(
        value in ifft(array(batch.select(collect_list("vib_y")).first()[0])).real.tolist()
        for value in result.select(collect_list("freq_vib_y")).first()[0]
    )
    assert all(
        value in ifft(array(batch.select(collect_list("vib_z")).first()[0])).real.tolist()
        for value in result.select(collect_list("freq_vib_z")).first()[0]
    )
