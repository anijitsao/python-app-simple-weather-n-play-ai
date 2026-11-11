from ingestion import start_ingestion
from tests import ingestion_error


def test_start_ingestion_success(mocker):
    mocked_chunks = ["chunk1", "chunk2"]
    mocked_service = mocker.patch(
        "ingestion.parse_file_get_chunks", return_value=mocked_chunks
    )
    mocked_db_service = mocker.patch(
        "ingestion.insert_chunks_to_vector_db", return_value=len(mocked_chunks)
    )

    result = start_ingestion()
    mocked_service.assert_called_once()
    mocked_db_service.assert_called()
    print("result", result)


def test_start_ingestion_failure(mocker):
    mocked_chunks = ["chunk1", "chunk2"]
    mocked_service = mocker.patch(
        "ingestion.parse_file_get_chunks", return_value=mocked_chunks
    )
    mocked_db_service = mocker.patch(
        "ingestion.insert_chunks_to_vector_db", return_value=len(mocked_chunks)
    )

    mocked_db_service.side_effect = Exception(ingestion_error)
    start_ingestion()
    mocked_service.assert_called_once()
    mocked_db_service.assert_called()
