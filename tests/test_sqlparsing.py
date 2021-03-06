from unittest import TestCase, mock

from logging import getLogger, DEBUG, StreamHandler
from pymongo import MongoClient
from djongo.sql2mongo import Parse

sql = [
    'UPDATE "auth_user" SET "password" = %s, "last_login" = NULL, "is_superuser" = %s, "username" = %s, "first_name" = %s, "last_name" = %s, "email" = %s, "is_staff" = %s, "is_active" = %s, "date_joined" = %s WHERE "auth_user"."id" = %s',

'CREATE TABLE "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" char NOT NULL, "name" char NOT NULL, "applied" datetime NOT NULL)',

'SELECT "django_migrations"."app", "django_migrations"."trial" '
'FROM  "django_migrations" '
'WHERE ("django_migrations"."app" <=%s '
      'AND "django_migrations"."trial" >=%s '
      'AND "django_migrations"."app" >=%s) '
      'OR ("django_migrations"."app" <=%s '
      'AND "django_migrations"."app">%s)',

'SELECT "auth_permission"."content_type_id", "auth_permission"."codename" \
FROM "auth_permission" INNER JOIN "django_content_type" \
    ON ("auth_permission"."content_type_id" = "django_content_type"."id") \
WHERE "auth_permission"."content_type_id" IN (%(0)s, %(1)s) \
ORDER BY "django_content_type"."app_label" ASC,\
"django_content_type"."model" ASC, "auth_permission"."codename" ASC',

'SELECT "django_content_type"."id", "django_content_type"."app_label",\
"django_content_type"."model" FROM "django_content_type" \
WHERE ("django_content_type"."model" = %s AND "django_content_type"."app_label" = %s)',

'SELECT (1) AS "a" FROM "django_session" WHERE "django_session"."session_key" = %(0)s LIMIT 1',

'SELECT COUNT(*) AS "__count" FROM "auth_user"',

'DELETE FROM "django_session" WHERE "django_session"."session_key" IN (%(0)s)',

'UPDATE "django_session" SET "session_data" = %(0)s, "expire_date" = %(1)s WHERE "django_session"."session_key" = %(2)s',

'SELECT "django_admin_log"."id", "django_admin_log"."action_time",\
    "django_admin_log"."user_id", "django_admin_log"."content_type_id",\
    "django_admin_log"."object_id", "django_admin_log"."object_repr", \
    "django_admin_log"."action_flag", "django_admin_log"."change_message",\
    "auth_user"."id", "auth_user"."password", "auth_user"."last_login", \
    "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name",\
    "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff",\
    "auth_user"."is_active", "auth_user"."date_joined", "django_content_type"."id",\
    "django_content_type"."app_label", "django_content_type"."model" \
FROM "django_admin_log" \
INNER JOIN "auth_user" \
    ON ("django_admin_log"."user_id" = "auth_user"."id") \
LEFT OUTER JOIN "django_content_type" \
    ON ("django_admin_log"."content_type_id" = "django_content_type"."id") \
WHERE "django_admin_log"."user_id" = %(0)s ORDER BY "django_admin_log"."action_time" DESC LIMIT 10',

'SELECT "auth_permission"."id", "auth_permission"."name", "auth_permission"."content_type_id", "auth_permission"."codename" '
'FROM "auth_permission" '
'INNER JOIN "auth_user_user_permissions" '
    'ON ("auth_permission"."id" = "auth_user_user_permissions"."permission_id") '
'INNER JOIN "django_content_type" '
    'ON ("auth_permission"."content_type_id" = "django_content_type"."id") '
'WHERE "auth_user_user_permissions"."user_id" = %s '
'ORDER BY "django_content_type"."app_label" ASC, "django_content_type"."model" ASC, "auth_permission"."codename" ASC',

'SELECT "auth_permission"."id", "auth_permission"."name", "auth_permission"."content_type_id", '
    '"auth_permission"."codename", "django_content_type"."id", "django_content_type"."app_label", "django_content_type"."model" '
'FROM "auth_permission" '
'INNER JOIN "django_content_type" '
    'ON ("auth_permission"."content_type_id" = "django_content_type"."id") '
'ORDER BY "django_content_type"."app_label" ASC, "django_content_type"."model" ASC, "auth_permission"."codename" ASC',

'SELECT "django_admin_log"."id", "django_admin_log"."action_time", "django_admin_log"."user_id", "django_admin_log"."content_type_id", "django_admin_log"."object_id", "django_admin_log"."object_repr", "django_admin_log"."action_flag", "django_admin_log"."change_message", "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined", "django_content_type"."id", "django_content_type"."app_label", "django_content_type"."model" FROM "django_admin_log" INNER JOIN "auth_user" ON ("django_admin_log"."user_id" = "auth_user"."id") LEFT OUTER JOIN "django_content_type" ON ("django_admin_log"."content_type_id" = "django_content_type"."id") WHERE "django_admin_log"."user_id" = %(0)s ORDER BY "django_admin_log"."action_time" DESC LIMIT 10',

'SELECT "auth_permission"."id" FROM "auth_permission" INNER JOIN "auth_group_permissions" ON ("auth_permission"."id" = "auth_group_permissions"."permission_id") INNER JOIN "django_content_type" ON ("auth_permission"."content_type_id" = "django_content_type"."id") WHERE "auth_group_permissions"."group_id" = %s ORDER BY "django_content_type"."app_label" ASC, "django_content_type"."model" ASC, "auth_permission"."codename" ASC',

'SELECT "auth_group_permissions"."permission_id" FROM "auth_group_permissions" WHERE ("auth_group_permissions"."group_id" = %s AND "auth_group_permissions"."permission_id" IN (%s))',

'SELECT (1) AS "a" FROM "auth_group" WHERE ("auth_group"."name" = %(0)s AND NOT ("auth_group"."id" = %(1)s)) LIMIT 1'

       ]

root_logger = getLogger()
root_logger.setLevel(DEBUG)
root_logger.addHandler(StreamHandler())


class TestParse(TestCase):

    def test_with_db(self):
        conn = MongoClient()['djongo-test']
        for i, s in enumerate(sql):
            result = Parse(conn, s, [1, 2, 3, 4, 5]).result()
            print(i)
            try:
                doc = result.next()
            except StopIteration:
                pass

    def _mock(self):
        result = Parse(self.conn, self.sql, self.params).result()
        doc = next(result)

    def test_where(self):
        conn = self.conn = mock.MagicMock()
        find = self.conn.__getitem__().find

        where = 'SELECT "table"."col" FROM "table" WHERE'
        filt_col1 = '"table"."col1"'

        find_args = {
            'projection': ['col'],
            'filter': {}
        }

        self.sql = f'{where} {filt_col1} = %s'
        find_args['filter'] = {
            'col1': {
                '$eq': 1
            }
        }
        self.params = [1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} {filt_col1} <= %s'
        find_args['filter'] = {
            'col1': {
                '$lte': 1
            }
        }
        self.params = [1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} {filt_col1} = NULL'
        find_args['filter'] = {
            'col1': {
                '$eq': None
            }
        }
        self.params = []
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} NOT ({filt_col1} <= %s)'
        find_args['filter'] = {
            'col1': {
                '$not': {
                    '$lte': 1
                }
            }
        }
        self.params = [1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} NOT {filt_col1} <= %s'
        find_args['filter'] = {
            'col1': {
                '$not': {
                    '$lte': 1
                }
            }
        }
        self.params = [1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} NOT {filt_col1} = NULL'
        find_args['filter'] = {
            'col1': {
                '$not': {
                    '$eq': None
                }
            }
        }
        self.params = []
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} {filt_col1} IN (%s)'
        find_args['filter'] = {
            'col1': {
                '$in': [1]
            }
        }
        self.params = [1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        # TODO: This is not the right SQL syntax
        self.sql = f'{where} {filt_col1} IN (NULL, %s)'
        find_args['filter'] = {
            'col1': {
                '$in': [None, 1]
            }
        }
        self.params = [1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} {filt_col1} NOT IN (%s)'
        find_args['filter'] = {
            'col1': {
                '$nin': [1]
            }
        }
        self.params = [1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} {filt_col1} NOT IN (%s, %s)'
        find_args['filter'] = {
            'col1': {
                '$nin': [1, 2]
            }
        }
        self.params = [1, 2]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} ({filt_col1} = %s AND {filt_col1} <= %s)'
        find_args['filter'] = {
            '$and': [
                {
                    'col1': {
                        '$eq': 1
                    }
                },
                {
                    'col1': {
                        '$lte': 2
                    }
                }
            ]
        }
        self.params = [1, 2]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} (NOT ({filt_col1} = %s) AND {filt_col1} <= %s)'
        find_args['filter'] = {
            '$and': [
                {
                    'col1': {
                        '$not': {
                            '$eq': 1
                        }
                    }
                },
                {
                    'col1': {
                        '$lte': 2
                    }
                }
            ]
        }
        self.params = [1, 2]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} {filt_col1} <= %s AND NOT ({filt_col1} = %s)'
        find_args['filter'] = {
            '$and': [
                {
                    'col1': {
                        '$lte': 2
                    }
                },
                {
                    'col1': {
                        '$not': {
                            '$eq': 1
                        }
                    }
                }
            ]
        }
        self.params = [2, 1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} NOT ({filt_col1} <= %s AND {filt_col1} = %s)'
        find_args['filter'] = {
            '$or': [
                {
                    'col1': {
                        '$not': {
                            '$lte': 2
                        }
                    }
                },
                {
                    'col1': {
                        '$not': {
                            '$eq': 1
                        }
                    }
                }
            ]
        }
        self.params = [2, 1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} NOT ({filt_col1} <= %s OR {filt_col1} = %s)'
        find_args['filter'] = {
            '$and': [
                {
                    'col1': {
                        '$not': {
                            '$lte': 2
                        }
                    }
                },
                {
                    'col1': {
                        '$not': {
                            '$eq': 1
                        }
                    }
                }
            ]
        }
        self.params = [2, 1]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()

        self.sql = f'{where} NOT ({filt_col1} <= %s OR {filt_col1} = %s) AND {filt_col1} >= %s'
        find_args['filter'] = {
            '$and': [
                {
                    '$and': [
                        {
                            'col1': {
                                '$not': {
                                    '$lte': 2
                                }
                            }
                        },
                        {
                            'col1': {
                                '$not': {
                                    '$eq': 1
                                }
                            }
                        }
                    ]
                },
                {
                    'col1': {
                        '$gte': 0
                    }
                },
            ]
        }
        self.params = [2, 1, 0]
        self._mock()
        find.assert_any_call(**find_args)
        conn.reset_mock()