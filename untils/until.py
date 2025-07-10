from datetime import datetime

class logic:
    def make_insert_query(court_no, dt_from, dt_to, yoyaku_jokyou):
        dt_now = datetime.now()
        dt_now = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        return f"""INSERT INTO BUNMORI(COURTNO, FROMDT, TODT, YOYAKUJOKYOU, CREATETIME, UPDATETIME) 
        VALUES('{court_no}', '{dt_from}', '{dt_to}', '{yoyaku_jokyou}', '{dt_now}', '{dt_now}')"""

    def get_insert_query(cnt, court_no, day, yoyaku, query_list):
        query = ''
        if cnt == 0:
            query = logic.make_insert_query(court_no, f'{day} 6:00:00', f'{day} 8:00:00', yoyaku)
            cnt += 1
        elif cnt == 1:
            query = logic.make_insert_query(court_no, f'{day} 8:00:00', f'{day} 10:00:00', yoyaku)
            cnt += 1
        elif cnt == 2:
            query = logic.make_insert_query(court_no, f'{day} 10:00:00', f'{day} 12:00:00', yoyaku)
            cnt += 1
        elif cnt == 3:
            query = logic.make_insert_query(court_no, f'{day} 12:00:00', f'{day} 13:00:00', yoyaku)
            cnt += 1
        elif cnt == 4:
            query = logic.make_insert_query(court_no, f'{day} 13:00:00', f'{day} 15:00:00', yoyaku)
            cnt += 1
        elif cnt == 5:
            query = logic.make_insert_query(court_no, f'{day} 15:00:00', f'{day} 17:00:00', yoyaku)
            cnt += 1
        elif cnt == 6:
            query = logic.make_insert_query(court_no, f'{day} 17:00:00', f'{day} 19:00:00', yoyaku)
            cnt += 1
        elif cnt == 7:
            query = logic.make_insert_query(court_no, f'{day} 19:00:00', f'{day} 21:00:00', yoyaku)
            cnt = 0
        query_list.append(query)
        return cnt
    def concat_query(query_list):
        query = ''
        for q in query_list:
            query += q + ";\n"
        return query