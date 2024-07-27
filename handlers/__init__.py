from .issues import Issue
from .ping import Ping
from .issueComment import issueComment
from .meta import Meta

handlers = {
    "ping": Ping,
    "issues": Issue,
    "issue_comment": issueComment,
    "meta": Meta,
}
