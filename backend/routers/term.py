from fastapi import APIRouter
from controllers.term_controller import create_term, list_term, get_term, update_term, delete_term

term_router = APIRouter()

term_router.post("/")(create_term)
term_router.get("/")(list_term)
term_router.get("/{term_id}")(get_term)
term_router.put("/{term_id}")(update_term)
term_router.delete("/{term_id}")(delete_term)