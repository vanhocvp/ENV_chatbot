import configparser
class Graph:
    def __init__(self):  
        self.node = self.build_graph()
        self.mess = self.load_mess_response()
    def get_next_node(self, action_pre, intent):
        # print (action_pre, intent)
        print ('pre_action: ', action_pre)
        print ('final_intent: ', intent)
        if action_pre == None:
            return 'action_start'
        try:
            return self.node[action_pre][intent]
        except:
            return 'action_fallback'
    def get_mess_response(self, action):
        print (action)
        return self.mess[action]
    def build_graph(self):
        config = configparser.ConfigParser()
        config.read('/home/vanhocvp/Code/SmartCall/training/api/graph/config.ini')
        action_node = dict(config.items('ACTION'))
        intent_condition = dict(config.items('INTENT'))
        node = {}
        for action in action_node.keys():
            try:
                node[action] = dict(config.items(action))
            except:
                pass
        return node
    def load_mess_response(self):
        config = configparser.ConfigParser()
        config.read('/home/vanhocvp/Code/SmartCall/training/api/graph/config.ini')
        messenger = dict(config.items('MESS_RESPONSE'))
        return messenger
# graph = Graph()
# print (graph.get_next_node('action_start', 'fall_back'))