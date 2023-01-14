from flask_restful import Resource, Api, fields, marshal_with, reqparse
from application import app
from application.models import *
from datetime import date, datetime
from flask_security import SQLAlchemySessionUserDatastore, current_user, auth_required, hash_password
from application.validation import *
from flask import jsonify
from application import tasks
from application import cache
from application.data_access import *
from time import perf_counter_ns
api = Api(app)
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)


user_parser = reqparse.RequestParser()
user_parser.add_argument('id')
user_parser.add_argument('fname')
user_parser.add_argument('lname')
user_parser.add_argument('email')
user_parser.add_argument('password')

user_get = {
    'id': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'email': fields.String,
    'password': fields.String,
}

user_resource = {
    'id': fields.Integer,
    'fname': fields.String,
    'lname': fields.String,
    'email': fields.String,
    'password': fields.String,
}


list_resource = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'user_id': fields.Integer
}

card_resource = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'deadline': fields.DateTime,
    'date_completed': fields.DateTime,
    'completed_status': fields.Boolean,
    'list_id': fields.Integer
}


class user(Resource):
    @auth_required("token")
    @marshal_with(user_resource)
    def get(self):
        if current_user:
            print(current_user)
            return current_user, 200
        else:
            raise NotFoundError(status_code=404)

    @marshal_with(user_resource)
    def post(self):
        args = user_parser.parse_args()
        fname = args.get('fname')
        lname = args.get('lname')
        email = args.get('email')
        password = args.get('password')
        if fname is None:
            raise BusinessValidationError(
                status_code=404, error_code="User", error_message="First Name Required")
        if lname is None:
            raise BusinessValidationError(
                status_code=404, error_code="User", error_message="Last Name Required")
        if email is None:
            raise BusinessValidationError(
                status_code=404, error_code="User", error_message="Email Required")
        if password is None:
            raise BusinessValidationError(
                status_code=404, error_code="User", error_message="Password Required")
        hashed_pw = hash_password(password)
        user = user_datastore.create_user(
            fname=fname, lname=lname, email=email, password=hashed_pw)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise SchemaValidationError(
                status_code=404, error_code="User", error_message="Cannot Post User")
        return user, 200

    @auth_required("token")
    @marshal_with(user_resource)
    def put(self):
        args = user_parser.parse_args()
        if args:
            fname = args.get('fname')
            lname = args.get('lname')
            email = args.get('email')
            password = args.get('password')
            if fname:
                current_user.fname = fname
                print(current_user.fname)
            if lname:
                current_user.lname = lname
            if email:
                current_user.email = email
            if password:
                current_user.password = hash_password(password)

            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise SchemaValidationError(
                    status_code=404, error_code="User", error_message="Cannot Put User")
            return current_user, 200

    @auth_required("token")
    def delete(self):
        if current_user:
            try:
                db.session.delete(current_user)
                db.session.commit()
            except:
                db.session.rollback()
                raise SchemaValidationError(
                    status_code=404, error_code="User", error_message="Cannot Delete User")
            return 200
        raise NotFoundError(status_code=404)


list_parser = reqparse.RequestParser()
list_parser.add_argument('id')
list_parser.add_argument('name')
list_parser.add_argument('description')
# list_parser.add_argument('user_id')


class list(Resource):
    @auth_required("token")
    @marshal_with(list_resource)
    def get(self):
        lists = current_user.lists
        return lists

    @auth_required("token")
    @marshal_with(list_resource)
    def post(self):
        args = list_parser.parse_args()
        if args:
            name = args.get('name')
            description = args.get('description')
            list = List(name=name, description=description,
                        user_id=current_user.id)
            if name is None:
                raise BusinessValidationError(
                    status_code=404, error_code="list", error_message="List Name Required")
            if description is None:
                raise BusinessValidationError(
                    status_code=404, error_code="list", error_message="List Description Required")

            try:
                db.session.add(list)
                db.session.commit()
            except:
                db.session.rollback()
                raise SchemaValidationError(
                    status_code=404, error_code="list", error_message="Cannot Post List")
            return list

    @auth_required("token")
    @marshal_with(list_resource)
    def put(self):
        args = list_parser.parse_args()
        if args:
            id = args.get('id')

            list = List.query.filter_by(id=id).first()
            name = args.get('name')
            description = args.get('description')
            if name:
                list.name = name
            if description:
                list.description = description
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise SchemaValidationError(
                    status_code=404, error_code="list", error_message="Cannot Update List")
            return list

    @auth_required("token")
    def delete(self):
        args = list_parser.parse_args()
        id = args.get('id')
        list = List.query.filter_by(id=id).first()
        if list:
            try:
                db.session.delete(list)
                db.session.commit()
                return 200
            except:
                db.session.rollback()
                raise SchemaValidationError(
                    status_code=404, error_code="list", error_message="Cannot Delete List")
        raise NotFoundError(status_code=404)


card_parser = reqparse.RequestParser()
card_parser.add_argument('id')
card_parser.add_argument('title')
card_parser.add_argument('content')
card_parser.add_argument('deadline')
card_parser.add_argument('date_completed')
card_parser.add_argument('completed_status')
card_parser.add_argument('list_id')


class card(Resource):
    @auth_required("token")
    @marshal_with(card_resource)
    def get(self, listid=None):
        if listid is not None:
            # list = List.query.filter_by(id=listid).first()
            # cards = list.cards
            start = perf_counter_ns()
            cards = get_cards(listid)
            stop = perf_counter_ns()
            # print(stop-start)
            return cards
        else:
            cards = Card.query.all()
            return cards

    # def get(self, id):
    #     card = Card.query.filter_by(id=id).first()
    #     return card

    @auth_required("token")
    @marshal_with(card_resource)
    def post(self):
        args = card_parser.parse_args()
        if args:
            title = args.get('title')
            content = args.get('content')
            deadline = args.get('deadline')
            dates = [int(d) for d in deadline.split("-")]
            deadline = date(dates[0], dates[1], dates[2])
            completed_status = args.get('completed_status')
            list_id = args.get('list_id')
            if title is None:
                raise BusinessValidationError(
                    status_code=404, error_code="card", error_message="Card title Required")
            if content is None:
                raise BusinessValidationError(
                    status_code=404, error_code="card", error_message="Card content Required")
            if deadline is None:
                raise BusinessValidationError(
                    status_code=404, error_code="card", error_message="Card deadline Required")
            if completed_status is None:
                raise BusinessValidationError(
                    status_code=404, error_code="card", error_message="Card complete status Required")
            if list_id is None:
                raise BusinessValidationError(
                    status_code=404, error_code="card", error_message="Card list id Required")

            list = List.query.filter_by(id=list_id).first()

            if list:
                if completed_status == 'true':
                    card = Card(title=title, content=content, deadline=deadline, date_completed=date.today(
                    ), completed_status=True, list_id=list_id)
                else:
                    card = Card(title=title, content=content, deadline=deadline,
                                completed_status=False, list_id=list_id)

                try:
                    db.session.add(card)
                    db.session.commit()
                    cache.delete_memoized(get_cards)
                    return card, 200
                except:
                    db.session.rollback()
                    raise SchemaValidationError(
                        status_code=404, error_code="card", error_message="Cannot Post Card")

    @auth_required("token")
    @marshal_with(card_resource)
    def put(self):
        args = card_parser.parse_args()
        if args:
            id = args.get('id')
            card = Card.query.filter_by(id=id).first()
            title = args.get('title')
            content = args.get('content')
            deadline = args.get('deadline')
            completed_status = args.get('completed_status')
            list_id = args.get('list_id')
            print(completed_status)
            if title:
                card.title = title
            if content:
                card.content = content
            if list_id:
                card.list_id = list_id
            if deadline:
                dates = [int(d) for d in deadline.split("-")]
                deadline = date(dates[0], dates[1], dates[2])
                card.deadline = deadline
            if completed_status == 'false':
                card.completed_status = False
            elif completed_status == 'true':
                card.completed_status = True
                card.date_completed = date.today()
            try:
                db.session.commit()
                cache.delete_memoized(get_cards)
                # cache.delete(get_cards)
                return card, 200
            except:
                db.session.rollback()
                raise SchemaValidationError(
                    status_code=404, error_code="card", error_message="Cannot Put Card")

    @auth_required("token")
    def delete(self):
        args = card_parser.parse_args()
        id = args.get('id')
        card = Card.query.filter_by(id=id).first()
        if card:
            card = Card.query.filter_by(id=id).first()
            try:
                db.session.delete(card)
                db.session.commit()
                cache.delete_memoized(get_cards)
                return "Deleted", 200
            except:
                db.session.rollback()
                raise SchemaValidationError(
                    status_code=404, error_code="card", error_message="Cannot Delete Card")


class summary(Resource):
    @auth_required("token")
    def get(self):
        user = current_user
        lists = user.lists
        date_completed = []
        total_count = 0
        completed_count = 0
        completed_after_deadline_count = 0
        completed_before_deadline_count = 0
        uncompleted_deadline_cross_count = 0
        uncompleted_deadline_not_cross_count = 0
        for list in lists:
            for card in list.cards:
                if card.completed_status:
                    completed_count += 1
                    date = card.date_completed.date()
                    date_completed.append(date)
                    if date > card.deadline.date():
                        completed_after_deadline_count += 1
                    else:
                        completed_before_deadline_count += 1
                if card.deadline.date() < datetime.now().date() and not card.completed_status:
                    uncompleted_deadline_cross_count += 1
                total_count += 1
        date_completed.sort()
        uncompleted_count = total_count - completed_count
        uncompleted_deadline_not_cross_count = uncompleted_count - \
            uncompleted_deadline_cross_count
        dates = []
        count = []
        for date in date_completed:  # collect date and corresponding dates count to plot line graph
            if date in dates:
                i = dates.index(date)
                count[i] += 1
            else:
                dates.append(date)
                count.append(1)

        print(dates, count, total_count, completed_count, uncompleted_count,
              uncompleted_deadline_cross_count, uncompleted_deadline_not_cross_count)
        return jsonify({'dates': dates, 'count': count, 'completed': completed_count, 'uncompleted': uncompleted_count, 'completedBeforeDeadline': completed_before_deadline_count,'completedAfterDeadline': completed_after_deadline_count,'uncompletedDeadlineCross': uncompleted_deadline_cross_count,'uncompletedDeadlineNotCross': uncompleted_deadline_not_cross_count})


class exportBoard(Resource):
    @auth_required("token")
    def get(self):
        job = tasks.exportBoard.delay(current_user.id)
        job_id = str(job)
        return jsonify({"job_id" : job_id, 'user_id': current_user.id})
        
class exportList(Resource):
    @auth_required("token")
    def get(self,list_id):
        job = tasks.exportList.delay(list_id)
        job_id = str(job)
        return jsonify({"job_id" : job_id})

class taskboardstatus(Resource):
    @auth_required("token")
    def get(self,job_id):
        id = tasks.exportBoard.AsyncResult(job_id)
        state = str(id.state)
        return jsonify({ 'state' : state})

class taskliststatus(Resource):
    @auth_required("token")
    def get(self,job_id):
        id = tasks.exportList.AsyncResult(job_id)
        state = str(id.state)
        return jsonify({ 'state' : state})

api.add_resource(user, "/api/user", "/api/user/<int:id>")
api.add_resource(list, "/api/list", "/api/list/<int:id>")
api.add_resource(card, "/api/card", "/api/card/<int:listid>")
api.add_resource(summary, "/api/summary")
api.add_resource(exportBoard, "/api/export_board")
api.add_resource(exportList, "/api/export_list/<int:list_id>")
api.add_resource(taskboardstatus, "/api/taskboardstatus/<job_id>")
api.add_resource(taskliststatus, "/api/taskliststatus/<job_id>")