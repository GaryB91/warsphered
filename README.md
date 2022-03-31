# warsphered

Run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload


# alembic 
Run: alembic revision --autogenerate -m "Added table comments"  // auto generate your mig
Run: alembic upgrade head  // upgrade to the latest revision
Run: alembic downgrade <revision_id>  // downgrade to the specified revision