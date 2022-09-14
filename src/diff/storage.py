from diff.schema import Request, Image, Video
from diff.messages import BaseTask
from sqlalchemy import desc
from logging import info, error
from sqlalchemy.orm import scoped_session
from sqlalchemy.engine import Engine
from diff.config import DBConfig, NatsConfig
from typing import List
import diff.db
import nats
import asyncio

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


def delete_binary_file(oid: int):
    conn = db_engine.raw_connection()
    l_obj = conn.lobject(oid, 'n')
    l_obj.unlink()
    conn.commit()
    conn.close()


def init_db_session(cfg: DBConfig):
    info("Initializing db session")
    global db_engine
    db_engine = diff.db.connect(cfg)
    global db_session
    db_session = diff.db.init_session(db_engine)


def commit():
    db_session.commit()


async def schedule_task(nc, kind: str, task):
    queue = f"tasks-{kind}"
    js = nc.jetstream()
    await js.add_stream(name=f"tasks-stream-{queue}", subjects=[queue])
    info(f"Scheduling task {task.json()} to {queue}")
    ack = await js.publish(queue, task.json().encode())
    info(ack)


async def schedule_request(nc, rid: int, kind: str = "diffusion"):
    task = BaseTask(request_id=rid, kind=kind)
    await schedule_task(nc, kind, task)


async def add_new_request(
    nc,
    prompt: str,
    count: int = 1,
    kind: str = "diffusion",
    priority=0,
):
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
        await schedule_request(nc, rid=req.id, kind=kind)
    return req


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


def delete_images(ids: List[int]):
    records = db_session.query(Image).filter(Image.id.in_(ids)).all()
    for rec in records:
        try:
            delete_binary_file(rec.oid)
        except Exception as e:
            error(e)
        finally:
            db_session.delete(rec)
    db_session.commit()


def delete_videos(ids: List[int]):
    records = db_session.query(Video).filter(Video.id.in_(ids)).all()
    for rec in records:
        try:
            delete_binary_file(rec.oid)
        except Exception as e:
            error(e)
        finally:
            db_session.delete(rec)
    db_session.commit()


def save_image(fname: str, rid: int, tid: int):
    oid = save_binary_file(fname)
    img = Image(
        request_id=rid,
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


def get_videos(ids: List[int]) -> List[Video]:
    return db_session.query(Video).filter(Video.id.in_(ids)).all()


def get_selected_images_for_request(rid: int) -> List[Image]:
    return db_session.query(Image).filter(
        Image.request_id == rid,
        Image.selected == True,
    ).all()


def get_image_data(id: int, quality: str = 'best') -> bytearray:
    image = db_session.query(Image).filter(Image.id == id).one()

    oid = image.oid
    if quality == 'best':
        oid = image.hqoid or image.oid
    if quality == 'hq':
        oid = image.hqoid

    return read_binary_file(oid)


def get_video_data(id: int) -> bytearray:
    video = db_session.query(Video).filter(Video.id == id).one()
    return read_binary_file(video.oid)
