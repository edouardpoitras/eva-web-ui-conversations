import os
import datetime
import gossip
from flask import abort, render_template_string
from bson.json_util import dumps
from eva import conf
from eva import log

dir_path = os.path.dirname(os.path.realpath(__file__))
conversations_markup = open(dir_path + '/templates/conversations.html').read()
conversation_markup = open(dir_path + '/templates/conversation.html').read()
interaction_markup = open(dir_path + '/templates/interaction.html').read()

@gossip.register('eva.web_ui.start', provides=['web_ui_conversations'])
def web_ui_start(app):
    app.add_url_rule('/conversations', 'conversations', conversations)
    app.add_url_rule('/conversations/<conversation_id>', 'conversation_view', conversation_view)
    app.add_url_rule('/conversations/<conversation_id>/interaction/<interaction_id>', 'interaction_view', interaction_view)

@gossip.register('eva.web_ui.menu_items', provides=['web_ui_conversations'])
def web_ui_menu_items():
    menu_item = {'path': '/conversations', 'title': 'Conversations'}
    conf['plugins']['web_ui']['config']['menu_items'].append(menu_item)

def conversations():
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    conversations = conf['plugins']['conversations']['module'].Conversation.objects().order_by('-id')
    return render_template_string(conversations_markup, menu_items=menu_items, conversations=conversations)

def conversation_view(conversation_id):
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    conversation = conf['plugins']['conversations']['module'].Conversation.objects(id=conversation_id).first()
    return render_template_string(conversation_markup, menu_items=menu_items, conversation=conversation)

def interaction_view(conversation_id, interaction_id):
    menu_items = conf['plugins']['web_ui']['module'].ready_menu_items()
    conversation = conf['plugins']['conversations']['module'].Conversation.objects(id=conversation_id).first()
    for inter in conversation.interactions:
        if str(inter.id) == interaction_id:
            return render_template_string(interaction_markup, menu_items=menu_items, interaction=inter)
    abort(404)
