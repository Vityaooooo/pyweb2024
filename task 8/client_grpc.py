from fastapi import FastAPI
from pydantic import BaseModel
import grpc
import glossary_pb2
import glossary_pb2_grpc
from typing import List  # Добавляем импорт List из typing

# Создание экземпляра FastAPI
app = FastAPI()

# Определение Pydantic моделей для запросов
class TermCreateRequest(BaseModel):
    term: str
    definition: str
    priority: int
    relation: int = 0
    author: str = "Vityaooooo"

class TermResponse(BaseModel):
    id: int
    term: str
    definition: str
    priority: int
    relation: int
    author: str

    class Config:
        orm_mode = True

# gRPC клиент
def get_grpc_stub():
    channel = grpc.insecure_channel('localhost:50051')
    stub = glossary_pb2_grpc.GlossaryServiceStub(channel)
    return stub

@app.post("/terms/", response_model=TermResponse)
async def create_term(term: TermCreateRequest):
    stub = get_grpc_stub()

    # Создание запроса на создание термина
    create_request = glossary_pb2.CreateTermRequest(
        term=term.term,
        definition=term.definition,
        priority=term.priority,
        relation=term.relation,
        author=term.author
    )

    # Вызов gRPC метода для создания термина
    create_response = stub.CreateTerm(create_request)

    # Возвращаем ответ, преобразованный в модель Pydantic
    return TermResponse(
        id=create_response.id,
        term=create_response.term,
        definition=create_response.definition,
        priority=create_response.priority,
        relation=create_response.relation,
        author=create_response.author
    )

@app.get("/terms/", response_model=List[TermResponse])  # Используем List вместо list
async def get_terms():
    stub = get_grpc_stub()

    # Создаем запрос для получения всех терминов
    response = stub.GetTerms(glossary_pb2.GetTermsRequest())

    # Преобразуем ответ gRPC в список Pydantic моделей
    return [
        TermResponse(
            id=term.id,
            term=term.term,
            definition=term.definition,
            priority=term.priority,
            relation=term.relation,
            author=term.author
        )
        for term in response.terms
    ]

@app.get("/terms/{term_id}", response_model=TermResponse)
async def get_term(term_id: int):
    stub = get_grpc_stub()

    # Создаем запрос для получения термина по ID
    get_request = glossary_pb2.GetTermRequest(term_id=term_id)
    response = stub.GetTerm(get_request)

    # Возвращаем термин как Pydantic модель
    return TermResponse(
        id=response.id,
        term=response.term,
        definition=response.definition,
        priority=response.priority,
        relation=response.relation,
        author=response.author
    )

@app.put("/terms/{term_id}", response_model=TermResponse)
async def update_term(term_id: int, term: TermCreateRequest):
    stub = get_grpc_stub()

    # Создаем запрос на обновление термина
    update_request = glossary_pb2.UpdateTermRequest(
        term_id=term_id,
        term=term.term,
        definition=term.definition,
        priority=term.priority,
        relation=term.relation,
        author=term.author
    )

    # Вызов gRPC метода для обновления термина
    update_response = stub.UpdateTerm(update_request)

    # Возвращаем обновленный термин
    return TermResponse(
        id=update_response.id,
        term=update_response.term,
        definition=update_response.definition,
        priority=update_response.priority,
        relation=update_response.relation,
        author=update_response.author
    )

@app.delete("/terms/{term_id}", response_model=dict)
async def delete_term(term_id: int):
    stub = get_grpc_stub()

    # Создаем запрос на удаление термина
    delete_request = glossary_pb2.DeleteTermRequest(term_id=term_id)
    response = stub.DeleteTerm(delete_request)

    # Возвращаем сообщение об успешном удалении
    return {"message": response.message}
