from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

promos = {
    1: {'id': 1, 'name': 'cinema', 'description': 'new event', 'participant': [],
                    'prize': []},

}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in promos:
        abort(404, message="promo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('participant')
parser.add_argument('prize')


class promo(Resource):
    def get(self):
        dict_get_all_promos = {}
        for id_promo in promos.keys():
            id_promo = int(id_promo)
            task = {'id': promos[id_promo]['id'], 'name': promos[id_promo]['name'],
                    'description': promos[id_promo]['description']}
            dict_get_all_promos[id_promo] = task
        return dict_get_all_promos

    def post(self):
        args = parser.parse_args()
        print(args)
        id = int(max(promos.keys())) + 1
        if args['name'] is None:
            abort(404, message="name is not defined")
        elif args['description'] is None:
            task = {'id': id, 'name': args['name'], 'description': None, 'participant': [],
                    'prizes': []}
        else:
            task = {'id': id, 'name': args['name'], 'description': args['description'], 'participant': [],
                    'prizes': []}
        promos[int(id)] = task
        return id, 201


class promo_id(Resource):
    def get(self, id_promo):
        id_promo = int(id_promo)
        abort_if_todo_doesnt_exist(id_promo)
        return promos[id_promo]

    def delete(self, id_promo):
        id_promo = int(id_promo)
        abort_if_todo_doesnt_exist(id_promo)
        del promos[id_promo]
        return '', 204

    def put(self, id_promo):
        args = parser.parse_args()
        id_promo = int(id_promo)
        if id_promo in promos.keys() and args['name'] is not None and args['description'] is not None:
            task = {'id': id_promo, 'name': args['name'], 'description': args['description'],
                    'participant': promos[id_promo]['participant'],
                    'prize': promos[id_promo]['prize']}
        elif id_promo in promos.keys() and args['name'] is not None:
            task = {'id': id_promo, 'name': args['name'], 'description': None,
                    'participant': promos[id_promo]['participant'],
                    'prize': promos[id_promo]['prize']}
        else:
            abort(404, message="name is not defined")
        promos[id_promo] = task
        return task, 201


class participant(Resource):
    def post(self, id_promo):
        args = parser.parse_args()
        id_promo = int(id_promo)
        if id_promo in promos.keys():
            if len(promos[id_promo]['participant']) >= 1:
                id_participant = int(promos[id_promo]['participant'][-1]['id']) + 1
            else:
                id_participant = 1
            promos[id_promo]['participant'].append({'id': id_participant, 'name': args['name']})
            return id_participant
        else:
            abort(404, message="name is not defined")


class participant_delete(Resource):
    def delete(self, id_promo, id_participant):
        id_promo = int(id_promo)
        id_participant = int(id_participant)
        abort_if_todo_doesnt_exist(id_promo)
        flag_del = False
        for i, participant in enumerate(promos[id_promo]['participant']):
            if id_participant == participant['id']:
                flag_del = True
                del promos[id_promo]['participant'][i]

        return '', 204


api.add_resource(promo, '/promo')
api.add_resource(promo_id, '/promo/<id_promo>')
api.add_resource(participant, '/promo/<id_promo>/participant')
api.add_resource(participant_delete, '/promo/<id_promo>/participant/<id_participant>')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
