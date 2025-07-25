# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""REST Controller"""

from __future__ import annotations
from typing import Annotated

from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.core.schema import PageResult
from src.main.app.mapper.new_word_mapper import newWordMapper
from src.main.app.model.new_word_model import NewWordModel
from src.main.app.schema.new_word_schema import (
    ListNewWordsRequest,
    NewWord,
    CreateNewWordRequest,
    NewWordDetail,
    UpdateNewWordRequest,
    BatchDeleteNewWordsRequest,
    BatchUpdateNewWordsRequest,
    BatchUpdateNewWordsResponse,
    BatchCreateNewWordsRequest,
    BatchCreateNewWordsResponse,
    ExportNewWordsRequest,
    ImportNewWordsResponse,
    BatchGetNewWordsResponse,
    ImportNewWordsRequest,
    ImportNewWord,
    BatchPatchNewWordsRequest,
)
from src.main.app.service.impl.new_word_service_impl import NewWordServiceImpl
from src.main.app.service.new_word_service import NewWordService

new_word_router = APIRouter()
new_word_service: NewWordService = NewWordServiceImpl(mapper=newWordMapper)


@new_word_router.get("/newWords/{id}")
async def get_new_word(id: int) -> NewWordDetail:
    """
    Retrieve new_word details.

    Args:

        id: Unique ID of the new_word resource.

    Returns:

        NewWordDetail: The new_word object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested new_word does not exist.
    """
    new_word_record: NewWordModel = await new_word_service.get_new_word(id=id)
    return NewWordDetail(**new_word_record.model_dump())


@new_word_router.get("/newWords")
async def list_new_words(
    req: Annotated[ListNewWordsRequest, Query()],
) -> PageResult[NewWord]:
    """
    List new_words with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        PageResult: Paginated list of new_words and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    new_word_records, total = await new_word_service.list_new_words(req=req)
    return PageResult(records=new_word_records, total=total)


@new_word_router.post("/newWords")
async def creat_new_word(
    req: CreateNewWordRequest,
) -> NewWord:
    """
    Create a new new_word.

    Args:

        req: Request object containing new_word creation data.

    Returns:

         NewWord: The new_word object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    new_word: NewWordModel = await new_word_service.create_new_word(req=req)
    return NewWord(**new_word.model_dump())


@new_word_router.put("/newWords")
async def update_new_word(
    req: UpdateNewWordRequest,
) -> NewWord:
    """
    Update an existing new_word.

    Args:

        req: Request object containing new_word update data.

    Returns:

        NewWord: The updated new_word object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the new_word to update doesn't exist.
    """
    new_word: NewWordModel = await new_word_service.update_new_word(req=req)
    return NewWord(**new_word.model_dump())


@new_word_router.delete("/newWords/{id}")
async def delete_new_word(
    id: int,
) -> None:
    """
    Delete new_word by ID.

    Args:

        id: The ID of the new_word to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the new_word with given ID doesn't exist.
    """
    await new_word_service.delete_new_word(id=id)


@new_word_router.get("/newWords:batchGet")
async def batch_get_new_words(
    ids: list[int] = Query(..., description="List of new_word IDs to retrieve"),
) -> BatchGetNewWordsResponse:
    """
    Retrieves multiple new_words by their IDs.

    Args:

        ids (list[int]): A list of new_word resource IDs.

    Returns:

        list[NewWordDetail]: A list of new_word objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested new_words does not exist.
    """
    new_word_records: list[
        NewWordModel
    ] = await new_word_service.batch_get_new_words(ids)
    new_word_detail_list: list[NewWordDetail] = [
        NewWordDetail(**new_word_record.model_dump())
        for new_word_record in new_word_records
    ]
    return BatchGetNewWordsResponse(new_words=new_word_detail_list)


@new_word_router.post("/newWords:batchCreate")
async def batch_create_new_words(
    req: BatchCreateNewWordsRequest,
) -> BatchCreateNewWordsResponse:
    """
    Batch create new_words.

    Args:

        req (BatchCreateNewWordsRequest): Request body containing a list of new_word creation items.

    Returns:

        BatchCreateNewWordsResponse: Response containing the list of created new_words.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any new_word creation data already exists.
    """

    new_word_records = await new_word_service.batch_create_new_words(req=req)
    new_word_list: list[NewWord] = [
        NewWord(**new_word_record.model_dump())
        for new_word_record in new_word_records
    ]
    return BatchCreateNewWordsResponse(new_words=new_word_list)


@new_word_router.post("/newWords:batchUpdate")
async def batch_update_new_words(
    req: BatchUpdateNewWordsRequest,
) -> BatchUpdateNewWordsResponse:
    """
    Batch update multiple new_words with the same changes.

    Args:

        req (BatchUpdateNewWordsRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated new_words.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify new_words
        HTTPException 404 (Not Found): If any specified new_word ID doesn't exist
    """
    new_word_records: list[
        NewWordModel
    ] = await new_word_service.batch_update_new_words(req=req)
    new_word_list: list[NewWord] = [
        NewWord(**new_word.model_dump()) for new_word in new_word_records
    ]
    return BatchUpdateNewWordsResponse(new_words=new_word_list)


@new_word_router.post("/newWords:batchPatch")
async def batch_patch_new_words(
    req: BatchPatchNewWordsRequest,
) -> BatchUpdateNewWordsResponse:
    """
    Batch update multiple new_words with individual changes.

    Args:

        req (BatchPatchNewWordsRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated new_words.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify new_words
        HTTPException 404 (Not Found): If any specified new_word ID doesn't exist
    """
    new_word_records: list[
        NewWordModel
    ] = await new_word_service.batch_patch_new_words(req=req)
    new_word_list: list[NewWord] = [
        NewWord(**new_word.model_dump()) for new_word in new_word_records
    ]
    return BatchUpdateNewWordsResponse(new_words=new_word_list)


@new_word_router.post("/newWords:batchDelete")
async def batch_delete_new_words(
    req: BatchDeleteNewWordsRequest,
) -> None:
    """
    Batch delete new_words.

    Args:
        req (BatchDeleteNewWordsRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the new_words do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await new_word_service.batch_delete_new_words(req=req)


@new_word_router.get("/newWords:exportTemplate")
async def export_new_words_template() -> StreamingResponse:
    """
    Export the Excel template for new_word import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await new_word_service.export_new_words_template()


@new_word_router.get("/newWords:export")
async def export_new_words(
    req: ExportNewWordsRequest = Query(...),
) -> StreamingResponse:
    """
    Export new_word data based on the provided new_word IDs.

    Args:
        req (ExportNewWordsRequest): Query parameters specifying the new_words to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching new_words are found.
    """
    return await new_word_service.export_new_words(
        req=req,
    )


@new_word_router.post("/newWords:import")
async def import_new_words(
    req: ImportNewWordsRequest = Form(...),
) -> ImportNewWordsResponse:
    """
    Import new_words from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing new_word data to import.

    Returns:
        ImportNewWordsResponse: List of successfully parsed new_word data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_new_words_resp: list[
        ImportNewWord
    ] = await new_word_service.import_new_words(req=req)
    return ImportNewWordsResponse(new_words=import_new_words_resp)
