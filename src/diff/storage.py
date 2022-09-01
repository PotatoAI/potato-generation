from diff.schema import Request, Task, Image
from sqlalchemy import desc
from logging import info
from sqlalchemy.orm import scoped_session
from diff.config import DBConfig
from typing import List
import diff.db

db_session: scoped_session


def init_db_session(cfg: DBConfig):
    global db_session
    db_session = diff.db.init_session(cfg)


def commit():
    db_session.commit()


def schedule_request(rid: int, priority: int, kind: str = "diffusion"):
    task = Task(
        request_id=rid,
        priority=priority,
        kind=kind,
    )
    db_session.add(task)
    db_session.commit()
    info(f"Scheduled new task {task.id}")


def add_new_request(prompt: str, kind: str = "diffusion", priority=0):
    if not prompt:
        prompt = input("Enter prompt: ")

    req = Request(
        prompt=prompt,
        priority=priority,
        approved=True,
        kind=kind,
    )
    db_session.add(req)
    db_session.commit()
    info(f"Created new request {req.id}")
    schedule_request(req.id, priority, kind=kind)
    return req


def approve_requests(ids: List[int]):
    reqs = db_session.query(Request).filter(Request.id.in_(ids)).all()
    print(reqs)
    for req in reqs:
        req.approved = True
    db_session.commit()


def delete_requests(ids: List[int]):
    print(ids)
    reqs = db_session.query(Request).filter(Request.id.in_(ids)).delete()
    print(reqs)
    db_session.commit()


def query_top_tasks(kind: str):
    return db_session.query(Task, Request).filter(
        Task.request_id == Request.id, Task.running == False,
        Task.status == 'new', Request.approved == True, Request.kind == kind,
        Task.kind == kind).order_by(desc(Task.priority)).order_by(
            Task.created_on)


def has_top_task(kind: str) -> int:
    return query_top_tasks(kind).count()


def get_top_task(kind) -> Task:
    return query_top_tasks(kind).limit(1).one()


def save_image(fname: str, rid: int, tid: int):
    img = Image(
        request_id=rid,
        task_id=tid,
        filename=fname,
    )
    db_session.add(img)
    db_session.commit()
    info(f"Saved img {img.id} -> {img.filename}")
