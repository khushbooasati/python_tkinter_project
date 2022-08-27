
import db
import json
from psycopg2 import sql

def get_watchlist_table(category):
    if category == 'jobs':
        return "watchlist_ticker"
    if category == 'skills':
        return "watchlist_skill"


def delete_from_watchlist(user, category, w_id):
    table = get_watchlist_table(category)
    if not table:
        return {"ERROR": "invalid category!"}

    qry = sql.SQL("""DELETE FROM public.{table} 
                WHERE uname={user}
                AND id={w_id} """).format(
        table = sql.Identifier(table),
        user = sql.Literal(user),
        w_id = sql.Literal(w_id),
    )
    con, cur = db.get_con()
    cur.execute(qry)
    con.commit()
    return {"STATUS": "OK"}


def add_to_watchlist(user, category, company_name, company_ticker=""):
    table = get_watchlist_table(category)
    if not table:
        return {"ERROR": "invalid category!"}

    if not company_ticker:
        company_ticker = company_name

    con, cur = db.get_con()
    qry = sql.SQL("""SELECT COUNT(*) FROM public.{table} 
                WHERE uname={user}
                AND (company_name={company_name} OR company_ticker={company_ticker}) """).format(
        table = sql.Identifier(table),
        user = sql.Literal(user),
        company_name = sql.Literal(company_name),
        company_ticker = sql.Literal(company_ticker),
    )

    cur.execute(qry)
    count = cur.fetchone()[0]
    if count > 0:
        return {"STATUS": "KO", "message": "Already added!"}

    qry = sql.SQL("""INSERT INTO public.{table} 
                VALUES({user}, {company_ticker}, {company_name}) """).format(
        table = sql.Identifier(table),
        user = sql.Literal(user),
        company_ticker = sql.Literal(company_ticker),
        company_name = sql.Literal(company_name),
    )
    cur.execute(qry)
    con.commit()
    con.close()

    return {"STATUS": "OK", "message": "Created!"}

def get_watchlist(user, category):
    table = get_watchlist_table(category)
    if not table:
        return {}

    con, cur = db.get_con()
    qry = sql.SQL("""SELECT * FROM public.{table} WHERE uname={user} """).format(
        table = sql.Identifier(table),
        user = sql.Literal(user)
    )
    cur.execute(qry)
    query_results = cur.fetchall()
    con.close()

    results = []
    if query_results:
        results = [
            {
                "id": row[3], 
                "company_ticker": row[1].strip(), 
                "company_name": row[2].strip()
            } for row in query_results
        ]
    return {"user": user, "category": category, "results": results}


def handle_watchlist(request, user, category):
    if not user:
        return {"ERROR": "User is not found!"}

    response = {}
    if request.method == "GET":
        response = get_watchlist(user, category)
    elif request.method == "POST":
        data = json.loads(request.data)
        company_name = data.get('company_name')
        company_ticker = data.get('company_ticker')
        if company_name or company_ticker:
            response = add_to_watchlist(user, category, company_name, company_ticker)
        else:
            response = {"ERROR": "Company is missed!"}
    elif request.method == "DELETE":
        w_id = request.args.get('id')
        if w_id:
            response = delete_from_watchlist(user, category, w_id)
        else:
            response = {"ERROR": "Company is missed!"}
    return response