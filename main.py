#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
    <head>
    <title>SignUp</title>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
"""

# html boilerplate for the bottom of every page
page_footer = """
    </body>
</html>
"""

signup_form = """
<h1>Signup</h1>
    <form method="post">
        <table>
            <tr>
                <td><label for="username">Username</label></td>
                <td>
                    <input name="username" type="text" value ="%(username)s" required>
                    <span class="error">%(username_error)s</span>
                </td>
            </tr>
            <tr>
                <td><label for="password">Password</label></td>
                <td>
                    <input name="password" type="password" required>
                    <span class="error">%(password_error)s</span>
                </td>
            </tr>
            <tr>
                <td><label for="verify">Verify Password</label</td>
                <td>
                    <input name="verify" type="password" required>
                    <span class="error">%(verify_error)s</span>
                </td>
            </tr>
            <tr>
                <td><label for="email">Email (optional)</label></td>
                <td>
                    <input name="email" type="email" value="%(email)s">
                    <span class="error">%(email_error)s</span>
                </td>
            </tr>
        </table>
        <input type="submit">
    </form>
"""

welcome_form = """
    <h1>Welcome, %s!</h1>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class SignUp(webapp2.RequestHandler):
    def write_signup_form(self, username="", username_error="", password_error="", verify_error="", email="", email_error=""):
        self.response.out.write(page_header + signup_form % {"username": username, "username_error": username_error, "password_error": password_error, "verify_error": verify_error, "email": email, "email_error": email_error} + page_footer)

    def get(self):
        self.write_signup_form()

    def post(self):
        have_error = False
        username = self.request.get('username')
        username_error = ""
        password = self.request.get('password')
        password_error = ""
        verify = self.request.get('verify')
        verify_error = ""
        email = self.request.get('email')
        email_error = ""

        if not valid_username(username):
            username_error = "Invalid Username"
            have_error = True

        if not valid_password(password):
            password_error = "Invalid Password"
            have_error = True

        if verify != password:
            verify_error = "Passwords Don't Match"
            have_error = True

        if not valid_email(email):
            email_error = "Invalid Email"
            have_error = True

        if have_error:
            self.write_signup_form(username, username_error, password_error, verify_error, email, email_error)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write(welcome_form % username)

app = webapp2.WSGIApplication([
    ('/', SignUp),
    ('/welcome', Welcome)
], debug=True)
