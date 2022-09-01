from diff.schema import Request, Task, Image, Video
from sqlalchemy import desc
from logging import info, error
from sqlalchemy.orm import scoped_session
from sqlalchemy.engine import Engine
from diff.config import DBConfig
from typing import List
import diff.db

db_engine: Engine
db_session: scoped_session


def save_binary_file(fname: str) -> int:
    conn = db_engine.raw_connection()
    l_obj = conn.lobject(0, 'wb', 0)
    with open(fname, 'rb') as f:
        l_obj.write(f.read())
    conn.commit()
    conn.close()
    return l_obj.oid


def read_binary_file(oid: int) -> bytearray:
    conn = db_engine.raw_connection()
    l_obj = conn.lobject(oid, 'rb')
    return l_obj.read()


def delete_binary_file(oid: int) -> bytearray:
    conn = db_engine.raw_connection()
    l_obj = conn.lobject(oid, 'n')
    l_obj.unlink()
    conn.commit()
    conn.close()


def init_db_session(cfg: DBConfig):
    global db_engine
    db_engine = diff.db.connect(cfg)
    global db_session
    db_session = diff.db.init_session(db_engine)


def commit():
    db_session.commit()


def schedule_request(rid: int, priority: int = 0, kind: str = "diffusion"):
    task = Task(
        request_id=rid,
        priority=priority,
        kind=kind,
    )
    db_session.add(task)
    db_session.commit()
    info(f"Scheduled new task {task.id}")


def add_new_request(prompt: str,
                    count: int = 1,
                    kind: str = "diffusion",
                    priority=0):
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
    for _ in range(count):
        schedule_request(req.id, priority, kind=kind)
    return req


def reschedule_tasks(ids: List[int]):
    tasks = db_session.query(Task).filter(Task.id.in_(ids)).all()
    for task in tasks:
        schedule_request(task.request_id)
    db_session.commit()


def select_images(ids: List[int]):
    imgs = db_session.query(Image).filter(Image.id.in_(ids)).all()
    for img in imgs:
        img.selected = True
    db_session.commit()


def approve_requests(ids: List[int]):
    reqs = db_session.query(Request).filter(Request.id.in_(ids)).all()
    for req in reqs:
        req.approved = True
    db_session.commit()


def delete_requests(ids: List[int]):
    db_session.query(Request).filter(Request.id.in_(ids)).delete()
    db_session.commit()


def delete_tasks(ids: List[int]):
    db_session.query(Task).filter(Task.id.in_(ids)).delete()
    db_session.commit()


def delete_images(ids: List[int]):
    images = db_session.query(Image).filter(Image.id.in_(ids)).all()
    for img in images:
        try:
            delete_binary_file(img.oid)
        except Exception as e:
            error(e)
        finally:
            db_session.delete(img)
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
    oid = save_binary_file(fname)
    img = Image(
        request_id=rid,
        task_id=tid,
        filename=fname,
        oid=oid,
    )
    db_session.add(img)
    db_session.commit()
    info(f"Saved img {img.id} -> {img.filename}")


def save_video(fname: str, rid: int):
    oid = save_binary_file(fname)
    vid = Video(
        request_id=rid,
        filename=fname,
        oid=oid,
    )
    db_session.add(vid)
    db_session.commit()
    info(f"Saved vid {vid.id} -> {vid.filename}")


def get_request(id: int) -> Request:
    return db_session.query(Request).filter(Request.id == id).one()
