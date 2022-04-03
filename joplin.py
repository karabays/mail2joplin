from dataclasses import asdict, dataclass, field
from xmlrpc.client import boolean
from joppy.api import Api

from config import joplinConf

joplin = Api(joplinConf.token,joplinConf.server)
notebook_id = joplinConf.notebook

@dataclass
class JoplinNote:
    title: str = None
    body: str = None
    body_html: str = None
    is_todo: boolean = False
    parent_id: str = notebook_id
    attachments: list = field(default_factory=list)
    
    def post_note(self):
        if len(self.attachments)==0:
            note_id = joplin.add_note(**asdict(self))
        else:
            # attachments can be a risk. better not download them at the moment
            note_id = joplin.add_note(**asdict(self))
        return note_id

