from flask import Flask, session
import os

app=Flask(__name__)
app.secret_key = 'onQkQTS68XybxwFLV6cF'

from app import routes,errors,form_post
