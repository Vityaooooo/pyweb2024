import grpc
from concurrent import futures
from sqlalchemy.orm import Session
import models, schemas
from database import engine, Base, get_db
import glossary_pb2
import glossary_pb2_grpc


class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def __init__(self, db: Session):
        self.db = db

    def GetTerms(self, request, context):
        terms = self.db.query(models.Term).all()
        response = glossary_pb2.GetTermsResponse()
        for term in terms:
            term_response = glossary_pb2.TermResponse(
                id=term.id,
                term=term.term,
                definition=term.definition,
                priority=term.priority,
                relation=term.relation,
                author=term.author
            )
            response.terms.append(term_response)
        return response

    def GetTerm(self, request, context):
        term = self.db.query(models.Term).filter(models.Term.id == request.term_id).first()
        if not term:
            context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
        return glossary_pb2.TermResponse(
            id=term.id,
            term=term.term,
            definition=term.definition,
            priority=term.priority,
            relation=term.relation,
            author=term.author
        )

    def CreateTerm(self, request, context):
        new_term = models.Term(
            term=request.term,
            definition=request.definition,
            priority=request.priority,
            relation=request.relation,
            author=request.author
        )
        self.db.add(new_term)
        self.db.commit()
        self.db.refresh(new_term)
        return glossary_pb2.TermResponse(
            id=new_term.id,
            term=new_term.term,
            definition=new_term.definition,
            priority=new_term.priority,
            relation=new_term.relation,
            author=new_term.author
        )

    def UpdateTerm(self, request, context):
        term = self.db.query(models.Term).filter(models.Term.id == request.term_id).first()
        if not term:
            context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
        term.term = request.term
        term.definition = request.definition
        term.priority = request.priority
        term.relation = request.relation
        term.author = request.author
        self.db.commit()
        self.db.refresh(term)
        return glossary_pb2.TermResponse(
            id=term.id,
            term=term.term,
            definition=term.definition,
            priority=term.priority,
            relation=term.relation,
            author=term.author
        )

    def DeleteTerm(self, request, context):
        term = self.db.query(models.Term).filter(models.Term.id == request.term_id).first()
        if not term:
            context.abort(grpc.StatusCode.NOT_FOUND, "Term not found")
        self.db.delete(term)
        self.db.commit()
        return glossary_pb2.DeleteTermResponse(message=f"Term with ID {request.term_id} deleted successfully")


def serve():
    # Инициализация базы данных и создание всех таблиц
    Base.metadata.create_all(bind=engine)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    db_session = next(get_db())
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryService(db_session), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
