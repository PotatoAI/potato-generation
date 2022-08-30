from diff.schema import Request, Task
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
    req = Request(
        prompt=prompt,
        priority=priority,
    )
    sess.add(req)
    sess.commit()
    print(f"Created new request {req.id}")
    schedule_request(sess, req.id, priority)


def get_top_task(sess) -> Task:
    return sess.query(Task).filter(Task.finished == False).order_by(
        desc(Task.priority)).order_by(
            Task.created_on).join(Request).limit(1).one()
