from app import db, graph, model

import io, random

class Conver(db.Model):
    __table__args__ = {'extend_existing': True}
    sender_id = db.Column(db.Integer, primary_key = True)
    pre_action = db.Column(db.String(50))
    pre_context = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    user_address = db.Column(db.String(50))
    def __repr__(self):
        return '<Conver {}>'.format(self.intent)
def process_request(args):
    sender_id = args['sender_id']
    mess = args['message']
    print (sender_id, mess)
    intent, score = model.intent.get_intent(mess)
    if score < 0.9:
        intent = 'fall_back'
    # GET NER
    entities = []
    entity  = {'start':1, 'end':5, 'value': 'Ha Noi'}
    entities.append(entity)

    pre_conv = Conver.query.get(sender_id)
    pre_action = pre_conv.pre_action
    pre_context = pre_conv.pre_context
    #  PROCESS FIANL INTENT - POLICY
    if pre_action == 'action_get_schedule': # CALL API TO GET SCHEDULE:
        schedule = ['have_schedule', 'havent_schedule']
        intent = schedule[random.randint(0,1)]
    if pre_action == 'action_get_user':     # CALL API TO GET USER:
        user = ['have_user', 'havent_user']
        intent = user[random.randint(0,1)]
    #  GET ACTION - NODE IN GRAPH
    action = graph.get_next_node(pre_action, intent) ### GET ACTION
    context = intent
    if pre_context != 'recall' and action == 'action_fallback' and pre_context != None:
        action = pre_action
        context = 'recall'
    elif pre_action == None:
        action = 'action_start'
        context = 'start'
    # SAVE TO SQL
    pre_conv.pre_action = action
    pre_conv.pre_context = context
    db.session.commit()    
    mess_response = graph.get_mess_response(action) # GET TEXT

    response = {}
    response['intent'] = intent
    response['action'] = action
    response['entities'] = entities
    response['text'] = mess_response
    return response

