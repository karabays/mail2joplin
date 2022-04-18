from dataclasses import asdict, dataclass, field
from xmlrpc.client import boolean
from joppy.api import Api
from loguru import logger

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
        note_dict = asdict(self)
        logger.debug(note_dict)
        if len(self.attachments)==0:
            note_id = joplin.add_note(**note_dict)
        else:
            # attachments can be a risk. better not download them at the moment
            note_id = joplin.add_note(**note_dict)
        logger.info(f"Note created. id:{note_id}, title:{self.title}")
        return note_id

