from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Mensagem de erro, caso haja"""
    message: str
