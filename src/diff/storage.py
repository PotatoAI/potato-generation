from diff.schema import Request, Task, Image
from sqlalchemy import desc
from logging import info


def schedule_request(sess, rid: int, priority: int, kind: str = "diffusion"):
    task = Task(
        request_id=rid,
        priority=priority,
        kind=kind,
    )
    sess.add(task)
    sess.commit()
    info(f"Scheduled new task {task.id}")


def add_new_request(sess, prompt: str, kind: str = "diffusion", priority=0):
    if not prompt:
        prompt = input("Enter prompt: ")

    req = Request(
        prompt=prompt,
        priority=priority,
        approved=True,
        kind=kind,
    )
    sess.add(req)
    sess.commit()
    info(f"Created new request {req.id}")
    schedule_request(sess, req.id, priority, kind=kind)


def query_top_tasks(sess, kind: str):
    return sess.query(
        Task,
        Request).filter(Task.request_id == Request.id, Task.running == False,
                        Task.status == 'new', Request.approved == True,
                        Request.kind == kind, Task.kind == kind).order_by(
                            desc(Task.priority)).order_by(Task.created_on)


def has_top_task(sess, kind: str) -> int:
    return query_top_tasks(sess, kind).count()


def get_top_task(sess, kind) -> Task:
    return query_top_tasks(sess, kind).limit(1).one()


def save_image(sess, fname: str, rid: int, tid: int):
    img = Image(
        request_id=rid,
        task_id=tid,
        filename=fname,
    )
    sess.add(img)
    sess.commit()
    info(f"Saved img {img.id} -> {img.filename}")
