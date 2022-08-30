from diff.schema import Request, Task, Image
from sqlalchemy import desc


def schedule_request(sess, rid: int, priority: int):
    task = Task(
        request_id=rid,
        priority=priority,
    )
    sess.add(task)
    sess.commit()
    print(f"Scheduled new task {task.id}")


def add_new_request(sess, prompt: str, priority=0):
    if prompt:
        req = Request(
            prompt=prompt,
            priority=priority,
        )
        sess.add(req)
        sess.commit()
        print(f"Created new request {req.id}")
        schedule_request(sess, req.id, priority)
    else:
        print('Empty prompt, skipping')


def query_top_tasks(sess):
    return sess.query(
        Task, Request).filter(Task.request_id == Request.id).filter(
            Task.running == False).filter(Task.status == 'new').order_by(
                desc(Task.priority)).order_by(Task.created_on)


def has_top_task(sess) -> int:
    return sess.query(Task).filter(Task.running == False).filter(
        Task.status == 'new').count()


def get_top_task(sess) -> Task:
    return query_top_tasks(sess).limit(1).one()


def save_image(sess, fname: str, rid: int, tid: int):
    img = Image(
        request_id=rid,
        task_id=tid,
        filename=fname,
    )
    sess.add(img)
    sess.commit()
    print(f"Saved img {img.id} -> {img.filename}")
