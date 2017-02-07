# -*- coding: utf-8 -*-

from models.user import User


class Authenticator(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self):
        return True


class StudentAuthenticator(Authenticator):

    def __init__(self,
                 student_grade=0,
                 student_class=0,
                 student_number=0,
                 # student_name='',
                 password='',
                 **kwargs):

        # 年級
        self.student_grade = student_grade
        # 班級
        self.student_class = student_class
        # 座號
        self.student_number = student_number
        # 學生姓名
        ''' omit the name field
        self.username = student_name
        '''
        self.username = "%02s_%02s_%02s" % (student_grade, student_class, student_number)
        # 密碼
        self.password = password

        super(StudentAuthenticator, self).__init__(
            self.username, self.password, **kwargs)

    def authenticate(self):
        try:
            # unique key
            user = User.query.filter_by(
                student_grade=self.student_grade,
                student_class=self.student_class,
                student_number=self.student_number
            ).first()

            # user not found
            if user is None:
                return False
            else:
                ''' omit the name field
                # password are 'student_name' and 'default_password'
                if (user.student_name == self.username) and (user.default_password == self.password):
                '''
                if user.default_password == self.password:
                    return True
                else:
                    return False
        except:
            return False
