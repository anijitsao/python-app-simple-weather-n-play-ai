from ingestion import start_ingestion
from tests import ingestion_error, parsed_chunks


def test_start_ingestion_success(mocker):
    mocked_parse_service = mocker.patch(
        "ingestion.parse_file_get_chunks", return_value=parsed_chunks
    )
    mocked_db_service = mocker.patch(
        "ingestion.insert_chunks_to_vector_db", return_value=len(parsed_chunks)
    )

    start_ingestion()
    mocked_parse_service.assert_called_once()
    mocked_db_service.assert_called()


def test_start_ingestion_failure(mocker):
    mocked_parse_service = mocker.patch(
        "ingestion.parse_file_get_chunks", return_value=parsed_chunks
    )
    mocked_db_service = mocker.patch(
        "ingestion.insert_chunks_to_vector_db",
    )

    mocked_db_service.side_effect = Exception(ingestion_error)
    start_ingestion()
    mocked_parse_service.assert_called_once()
    mocked_db_service.assert_called_once()
